import logging
import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import ClientPage
from .serializers import ClientPageSerializer

logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY


class ClientPageViewSet(ReadOnlyModelViewSet):
    queryset = ClientPage.objects.all()
    serializer_class = ClientPageSerializer
    lookup_field = "slug"

    def retrieve(self, request, slug=None, *args, **kwargs):
        client_page = get_object_or_404(ClientPage, slug=slug)
        serializer = self.get_serializer(client_page)
        return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def create_checkout_session(request):
    data = request.data
    slug = data.get("slug")
    option = data.get("option")
    email = data.get("email")
    plan_title = data.get("plan_title") or "Support Plan Subscription"

    if not slug or not option:
        return Response({"error": "Missing slug or option"}, status=400)

    page = get_object_or_404(ClientPage, slug=slug)

    try:
        # --------------------------------------------------------------
        # CASE 1: One-time payment (project_only_price)
        # --------------------------------------------------------------
        if option == "project_only_price":
            project_price = int(page.project_only_price * 100)
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "unit_amount": project_price,
                            "product_data": {
                                "name": f"{page.company_name} Project",
                            },
                        },
                        "quantity": 1,
                    }
                ],
                mode="payment",
                customer_email=email,
                # Ensure Stripe emails a receipt
                payment_intent_data={"receipt_email": email} if email else {},
                success_url=(
                    "https://proposals.thecloudsteward.com/"
                    "success?session_id={CHECKOUT_SESSION_ID}"
                ),
                cancel_url=f"https://proposals.thecloudsteward.com/{slug}",
            )
            return Response({"url": session.url})

        # --------------------------------------------------------------
        # CASE 2: Subscription flow (one-time fee + recurring subscription)
        # --------------------------------------------------------------
        else:
            # Validate that the chosen "option" is a valid attribute on page
            if not hasattr(page, option):
                return Response({"error": f"Invalid option: {option}"}, status=400)

            subscription_price = int(getattr(page, option) * 100)
            project_price = int(page.project_with_subscription_price * 100)

            # Create a one-time Price object
            one_time_price = stripe.Price.create(
                unit_amount=project_price,
                currency="usd",
                product_data={"name": "One-Time Project Fee"},
            )

            # Create a recurring Price object for the subscription
            recurring_price = stripe.Price.create(
                unit_amount=subscription_price,
                currency="usd",
                recurring={"interval": "month"},
                product_data={"name": plan_title},
            )

            # Create a Checkout Session in subscription mode (no trial)
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {"price": one_time_price.id, "quantity": 1},
                    {"price": recurring_price.id, "quantity": 1},
                ],
                mode="subscription",
                customer_email=email,
                success_url=(
                    "https://proposals.thecloudsteward.com/"
                    "success?session_id={CHECKOUT_SESSION_ID}"
                ),
                cancel_url=f"https://proposals.thecloudsteward.com/{slug}",
            )
            return Response({"url": session.url})

    except stripe.error.StripeError as e:
        logger.exception("Stripe error during create_checkout_session")
        return Response({"error": str(e)}, status=400)
    except Exception as e:
        logger.exception("Unhandled exception during create_checkout_session")
        return Response({"error": str(e)}, status=500)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_checkout_session_details(request):
    session_id = request.GET.get("session_id")
    if not session_id:
        return Response({"error": "No session ID provided"}, status=400)

    logger.debug("get_checkout_session_details called with session_id=%s", session_id)
    try:
        # Retrieve the Checkout Session and expand subscription + its latest_invoice
        # Do NOT attempt to expand 'charge' directly, as Stripe won't allow it here.
        session = stripe.checkout.Session.retrieve(
            session_id,
            expand=["subscription.latest_invoice"],
        )
        logger.debug("Retrieved Checkout Session:\n%r", session)

        mode = session.get("mode")
        logger.debug("Session mode: %s", mode)

        amount_total = None
        currency = None
        receipt_url = None

        # ---------------------------------------------------------
        # ONE-TIME PAYMENT MODE
        # ---------------------------------------------------------
        if mode == "payment":
            payment_intent_id = session.get("payment_intent")
            if not payment_intent_id:
                raise Exception("No PaymentIntent for payment-mode session.")

            # Retrieve PaymentIntent and expand charges
            pi = stripe.PaymentIntent.retrieve(
                payment_intent_id,
                expand=["charges"],
            )
            logger.debug("PaymentIntent: %r", pi)

            charges = pi.get("charges", {}).get("data", [])
            if charges:
                receipt_url = charges[0].get("receipt_url")
            else:
                # fallback if no direct charges
                latest_charge_id = pi.get("latest_charge")
                if latest_charge_id:
                    charge_obj = stripe.Charge.retrieve(latest_charge_id)
                    receipt_url = charge_obj.get("receipt_url")

            amount_total = pi.get("amount")
            currency = pi.get("currency")

        # ---------------------------------------------------------
        # SUBSCRIPTION MODE
        # ---------------------------------------------------------
        elif mode == "subscription":
            subscription_info = session.get("subscription")
            if not subscription_info:
                raise Exception("No subscription found in session object.")

            # Because we expanded ["subscription.latest_invoice"], subscription_info
            # should be a dict with "latest_invoice"
            latest_invoice = subscription_info.get("latest_invoice")
            if latest_invoice:
                logger.debug("Subscription latest_invoice: %r", latest_invoice)

                amount_total = latest_invoice.get("amount_paid")
                currency = latest_invoice.get("currency")

                # If there's a separate charge ID on the invoice, we can retrieve it
                invoice_charge_id = latest_invoice.get("charge")
                if invoice_charge_id:
                    charge_obj = stripe.Charge.retrieve(invoice_charge_id)
                    logger.debug(
                        "Retrieved invoice's charge object for subscription: %r",
                        charge_obj,
                    )
                    receipt_url = charge_obj.get("receipt_url")
                else:
                    logger.debug(
                        "No charge reference found in the subscription's invoice. "
                        "Use hosted_invoice_url if needed."
                    )
                    # Fallback: invoice_pdf or hosted_invoice_url can act as a "receipt":
                    # receipt_url = latest_invoice.get("hosted_invoice_url")
                    # or:
                    # receipt_url = latest_invoice.get("invoice_pdf")

        # Retrieve some customer name if available
        customer_name = ""
        if session.get("customer_details"):
            details = session["customer_details"]
            customer_name = details.get("name", "")
        elif session.get("customer"):
            cust = stripe.Customer.retrieve(session["customer"])
            customer_name = cust.get("name", "")

        result = {
            "customer_name": customer_name,
            "amount_total": amount_total,
            "currency": currency,
            "receipt_url": receipt_url,
        }
        logger.debug("Final response data: %r", result)
        return Response(result)

    except stripe.error.StripeError as se:
        logger.exception(
            "Stripe error in get_checkout_session_details for session_id=%s", session_id
        )
        return Response({"error": str(se)}, status=400)
    except Exception as e:
        logger.exception(
            "Unhandled exception in get_checkout_session_details for session_id=%s",
            session_id,
        )
        return Response({"error": str(e)}, status=400)
