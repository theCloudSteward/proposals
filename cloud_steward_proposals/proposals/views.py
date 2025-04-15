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
        # First, fetch the session w/o expansions to see the mode
        base_session = stripe.checkout.Session.retrieve(session_id)
        logger.debug("First retrieval of Checkout Session:\n%r", base_session)

        mode = base_session.get("mode")
        logger.debug("Session mode: %s", mode)

        # Decide expansions
        if mode == "payment":
            # We'll expand the PaymentIntent
            expansions = ["payment_intent"]
        elif mode == "subscription":
            # We'll expand subscription.latest_invoice.charge
            expansions = ["subscription.latest_invoice.charge"]
        else:
            expansions = []

        # Retrieve the session with expansions
        if expansions:
            session = stripe.checkout.Session.retrieve(session_id, expand=expansions)
        else:
            session = base_session

        amount_total = None
        currency = None
        receipt_url = None

        if mode == "payment":
            payment_intent_obj = session.get("payment_intent")
            if isinstance(payment_intent_obj, dict):
                # Already expanded
                charges = payment_intent_obj.get("charges", {}).get("data", [])
                if charges:
                    receipt_url = charges[0].get("receipt_url")
                else:
                    # Fallback: retrieve charge from latest_charge
                    latest_charge_id = payment_intent_obj.get("latest_charge")
                    if latest_charge_id:
                        charge_obj = stripe.Charge.retrieve(latest_charge_id)
                        receipt_url = charge_obj.get("receipt_url")
                amount_total = payment_intent_obj.get("amount")
                currency = payment_intent_obj.get("currency")
            elif isinstance(payment_intent_obj, str):
                # Retrieve PaymentIntent separately
                pi = stripe.PaymentIntent.retrieve(payment_intent_obj, expand=["charges"])
                charges = pi.get("charges", {}).get("data", [])
                if charges:
                    receipt_url = charges[0].get("receipt_url")
                else:
                    latest_charge_id = pi.get("latest_charge")
                    if latest_charge_id:
                        charge_obj = stripe.Charge.retrieve(latest_charge_id)
                        receipt_url = charge_obj.get("receipt_url")
                amount_total = pi.get("amount")
                currency = pi.get("currency")

        elif mode == "subscription":
            # The subscription is expanded with its latest invoice, which may have .charge expanded
            sub = session.get("subscription")  # Might be a dict if expanded
            if not sub or not isinstance(sub, dict):
                raise Exception("No subscription data found in session.")
            invoice = sub.get("latest_invoice")
            if invoice:
                logger.debug("Subscription latest_invoice: %r", invoice)
                amount_total = invoice.get("amount_paid")
                currency = invoice.get("currency")

                # The .charge might be present if it was expanded
                charge_obj = invoice.get("charge")
                if isinstance(charge_obj, dict):
                    # We have the entire Charge object
                    receipt_url = charge_obj.get("receipt_url")
                else:
                    # Maybe it's just an ID or None
                    charge_id = invoice.get("charge")
                    if charge_id:
                        # Retrieve separately
                        ch = stripe.Charge.retrieve(charge_id)
                        receipt_url = ch.get("receipt_url")
            else:
                logger.debug("No latest invoice found on subscription.")

        # Extract customer name
        customer_name = ""
        if "customer_details" in session and session["customer_details"]:
            customer_name = session["customer_details"].get("name", "")
        elif "customer" in session and session["customer"]:
            cust_obj = stripe.Customer.retrieve(session["customer"])
            customer_name = cust_obj.get("name", "")

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
