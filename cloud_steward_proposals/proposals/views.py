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


# ---------------------------------------------------------------------------
#  CHECKOUT ‑ SESSION CREATION
# ---------------------------------------------------------------------------
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
        # -------------------------------------------------------------------
        # 1) ONE‑TIME PAYMENT FLOW
        # -------------------------------------------------------------------
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
                success_url=(
                    "https://proposals.thecloudsteward.com/"
                    "success?session_id={CHECKOUT_SESSION_ID}"
                ),
                cancel_url=f"https://proposals.thecloudsteward.com/{slug}",
            )
            return Response({"url": session.url})

        # -------------------------------------------------------------------
        # 2) SUBSCRIPTION FLOW  – with 30‑day FREE TRIAL
        # -------------------------------------------------------------------
        else:
            if not hasattr(page, option):
                return Response({"error": f"Invalid option: {option}"}, status=400)

            subscription_price = int(getattr(page, option) * 100)
            project_price = int(page.project_with_subscription_price * 100)

            # One‑time project fee
            one_time_price = stripe.Price.create(
                unit_amount=project_price,
                currency="usd",
                product_data={"name": "One‑Time Project Fee"},
            )

            # Recurring monthly price
            recurring_price = stripe.Price.create(
                unit_amount=subscription_price,
                currency="usd",
                recurring={"interval": "month"},
                product_data={"name": plan_title},
            )

            # Checkout Session — subscription mode **with free 30‑day trial**
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {"price": one_time_price.id, "quantity": 1},
                    {"price": recurring_price.id, "quantity": 1},
                ],
                mode="subscription",
                customer_email=email,
                subscription_data={"trial_period_days": 30},
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


# ---------------------------------------------------------------------------
#  CHECKOUT ‑ SESSION DETAILS / RECEIPT LOOK‑UP
# ---------------------------------------------------------------------------
@api_view(["GET"])
@permission_classes([AllowAny])
def get_checkout_session_details(request):
    session_id = request.GET.get("session_id")
    if not session_id:
        return Response({"error": "No session ID provided"}, status=400)

    logger.debug("get_checkout_session_details called with session_id=%s", session_id)
    try:
        # Fetch Session, expand latest invoice for subs
        session = stripe.checkout.Session.retrieve(
            session_id, expand=["subscription.latest_invoice"]
        )
        logger.debug("Retrieved Checkout Session:\n%r", session)

        mode = session.get("mode")
        logger.debug("Session mode: %s", mode)

        amount_total = None
        currency = None
        receipt_url = None

        # -------------------------------------------------------------------
        # ONE‑TIME PAYMENT
        # -------------------------------------------------------------------
        if mode == "payment":
            payment_intent_id = session.get("payment_intent")
            if payment_intent_id:
                pi = stripe.PaymentIntent.retrieve(payment_intent_id, expand=["charges"])
                charges = pi.get("charges", {}).get("data", [])
                if charges:
                    receipt_url = charges[0].get("receipt_url")
                amount_total = pi.get("amount")
                currency = pi.get("currency")

        # -------------------------------------------------------------------
        # SUBSCRIPTION
        # -------------------------------------------------------------------
        elif mode == "subscription":
            subscription_info = session.get("subscription")
            latest_invoice = (
                subscription_info.get("latest_invoice") if subscription_info else None
            )
            if latest_invoice:
                amount_total = latest_invoice.get("amount_paid")
                currency = latest_invoice.get("currency")
                invoice_charge_id = latest_invoice.get("charge")
                if invoice_charge_id:
                    charge_obj = stripe.Charge.retrieve(invoice_charge_id)
                    receipt_url = charge_obj.get("receipt_url")

        # -------------------------------------------------------------------
        # CUSTOMER NAME (optional)
        # -------------------------------------------------------------------
        customer_name = ""
        if session.get("customer_details"):
            customer_name = session["customer_details"].get("name", "")
        elif session.get("customer"):
            customer_name = stripe.Customer.retrieve(session["customer"]).get(
                "name", ""
            )

        # -------------------------------------------------------------------
        #  NEW  ➜  Friendly fallback message when no receipt yet
        # -------------------------------------------------------------------
        fallback_message = None
        if not receipt_url:
            fallback_message = (
                "Thank you for your purchase. You should receive a confirmation "
                "email shortly with your receipt."
            )

        result = {
            "customer_name": customer_name,
            "amount_total": amount_total,
            "currency": currency,
            "receipt_url": receipt_url,
            # Only present when we truly have no receipt link:
            "message": fallback_message,
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
