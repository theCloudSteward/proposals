import logging
import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes, authentication_classes
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
    lookup_field = 'slug'

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
                payment_intent_data={"receipt_email": email} if email else {},
                success_url="https://proposals.thecloudsteward.com/success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=f"https://proposals.thecloudsteward.com/{slug}",
            )
            return Response({"url": session.url})
        else:
            # Validate the subscription attribute:
            if not hasattr(page, option):
                return Response({"error": f"Invalid option: {option}"}, status=400)

            subscription_price = int(getattr(page, option) * 100)
            project_price = int(page.project_with_subscription_price * 100)

            # Create a one-time price
            one_time_price = stripe.Price.create(
                unit_amount=project_price,
                currency="usd",
                product_data={"name": "One-Time Project Fee"},
            )

            # Create a recurring price for the chosen plan
            recurring_price = stripe.Price.create(
                unit_amount=subscription_price,
                currency="usd",
                recurring={"interval": "month"},
                product_data={"name": plan_title},
            )

            # Create Session in subscription mode (no trial)
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {"price": one_time_price.id, "quantity": 1},
                    {"price": recurring_price.id, "quantity": 1},
                ],
                mode="subscription",
                customer_email=email,
                success_url="https://proposals.thecloudsteward.com/success?session_id={CHECKOUT_SESSION_ID}",
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
        # 1) Retrieve the Checkout Session with expansions for subscription & latest_invoice
        #    but do NOT expand 'charge' (since that's unsupported):
        session = stripe.checkout.Session.retrieve(
            session_id,
            expand=["subscription.latest_invoice"]  # only this is allowed
        )
        logger.debug("Retrieved Checkout Session:\n%r", session)

        mode = session.get("mode")
        logger.debug("Session mode: %s", mode)

        amount_total = None
        currency = None
        receipt_url = None

        # -------------------------------------------------------------------
        # CASE 1: One-time 'payment' mode
        # -------------------------------------------------------------------
        if mode == "payment":
            # Normal logic: expand PaymentIntent or retrieve it to find charges
            payment_intent_id = session.get("payment_intent")
            if not payment_intent_id:
                raise Exception("No PaymentIntent for payment-mode session.")

            # Retrieve PaymentIntent & expand charges:
            pi = stripe.PaymentIntent.retrieve(payment_intent_id, expand=["charges"])
            logger.debug("PaymentIntent: %r", pi)
            charges = pi.get("charges", {}).get("data", [])
            if charges:
                # We have at least one charge => get receipt_url
                receipt_url = charges[0].get("receipt_url")
            else:
                # fallback: retrieve charge from latest_charge if needed
                latest_charge_id = pi.get("latest_charge")
                if latest_charge_id:
                    charge_obj = stripe.Charge.retrieve(latest_charge_id)
                    receipt_url = charge_obj.get("receipt_url")

            amount_total = pi.get("amount")
            currency = pi.get("currency")

        # -------------------------------------------------------------------
        # CASE 2: Subscription mode
        # -------------------------------------------------------------------
        elif mode == "subscription":
            subscription_info = session.get("subscription")
            if not subscription_info:
                raise Exception("No subscription found in session object.")

            # subscription_info might be a dict if it was expanded. 
            # (We've done `expand=["subscription.latest_invoice"]`.)
            latest_invoice = subscription_info.get("latest_invoice")
            if not latest_invoice:
                logger.debug("No latest invoice found on subscription.")
            else:
                logger.debug("Subscription latest_invoice: %r", latest_invoice)
                amount_total = latest_invoice.get("amount_paid")
                currency = latest_invoice.get("currency")

                # 2) The .charge is typically just an ID if it exists at all:
                invoice_charge_id = latest_invoice.get("charge")
                if invoice_charge_id:
                    # 3) Retrieve the Charge by ID => get the receipt_url
                    charge_obj = stripe.Charge.retrieve(invoice_charge_id)
                    logger.debug("Retrieved invoice's charge object: %r", charge_obj)
                    receipt_url = charge_obj.get("receipt_url")

        # -------------------------------------------------------------------
        # Extract a "customer name" (if you like)
        # -------------------------------------------------------------------
        customer_name = ""
        # If 'customer_details' exist, that usually has the name:
        if session.get("customer_details"):
            details = session["customer_details"]
            customer_name = details.get("name", "")
        elif session.get("customer"):
            # fallback: retrieve full Customer if you want
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
        logger.exception("Stripe error in get_checkout_session_details for session_id=%s", session_id)
        return Response({"error": str(se)}, status=400)
    except Exception as e:
        logger.exception("Unhandled exception in get_checkout_session_details for session_id=%s", session_id)
        return Response({"error": str(e)}, status=400)
