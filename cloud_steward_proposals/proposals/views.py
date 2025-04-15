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


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def create_checkout_session(request):
    data = request.data
    slug = data.get('slug')
    option = data.get('option')
    email = data.get('email')
    plan_title = data.get('plan_title') or "Support Plan Subscription"

    if not slug or not option:
        return Response({"error": "Missing slug or option"}, status=400)

    page = get_object_or_404(ClientPage, slug=slug)

    try:
        if option == 'project_only_price':
            project_price = int(page.project_only_price * 100)
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': project_price,
                        'product_data': {
                            'name': f"{page.company_name} Project",
                        },
                    },
                    'quantity': 1,
                }],
                mode='payment',
                customer_email=email,
                payment_intent_data={'receipt_email': email} if email else {},
                success_url=f"https://proposals.thecloudsteward.com/success?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"https://proposals.thecloudsteward.com/{slug}",
            )
            return Response({"url": session.url})

        else:
            if not hasattr(page, option):
                return Response({"error": f"Invalid option: {option}"}, status=400)

            subscription_price = int(getattr(page, option) * 100)
            project_price = int(page.project_with_subscription_price * 100)

            one_time_price = stripe.Price.create(
                unit_amount=project_price,
                currency='usd',
                product_data={
                    'name': "One-Time Project Fee",
                },
            )

            recurring_price = stripe.Price.create(
                unit_amount=subscription_price,
                currency='usd',
                recurring={'interval': 'month'},
                product_data={
                    'name': plan_title,
                },
            )

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {'price': one_time_price.id, 'quantity': 1},
                    {'price': recurring_price.id, 'quantity': 1},
                ],
                mode='subscription',
                customer_email=email,
                # No trial => immediate charge for both the project fee + subscription
                success_url=f"https://proposals.thecloudsteward.com/success?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"https://proposals.thecloudsteward.com/{slug}",
            )
            return Response({"url": session.url})

    except stripe.error.StripeError as e:
        logger.exception("Stripe error during create_checkout_session")
        return Response({"error": str(e)}, status=400)
    except Exception as e:
        logger.exception("Unhandled exception during create_checkout_session")
        return Response({"error": str(e)}, status=500)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_checkout_session_details(request):
    session_id = request.GET.get("session_id")
    if not session_id:
        return Response({"error": "No session ID provided"}, status=400)

    logger.debug("get_checkout_session_details called with session_id=%s", session_id)

    try:
        # Step 1: Retrieve the session WITHOUT expansions to see which mode it is.
        base_session = stripe.checkout.Session.retrieve(session_id)
        logger.debug("First retrieval of Checkout Session:\n%r", base_session)

        mode = base_session.get("mode")
        logger.debug("Session mode: %s", mode)

        # Decide which expansions we can safely request:
        expansions = []
        if mode == "payment":
            # We can expand the top-level payment_intent for one-time checks
            expansions = ["payment_intent"]
        elif mode == "subscription":
            # We can expand subscription.latest_invoice.payment_intent for subscription checks
            expansions = ["subscription.latest_invoice.payment_intent"]

        # Step 2: Retrieve the session AGAIN with only the allowed expansions
        if expansions:
            session = stripe.checkout.Session.retrieve(session_id, expand=expansions)
        else:
            # fallback if something unexpected
            session = base_session

        amount_total = None
        currency = None
        receipt_url = None
        customer_name = ""

        # Now handle each mode
        if mode == "payment":
            pi = session.get("payment_intent")
            if pi and isinstance(pi, dict):
                # PaymentIntent is expanded
                charges = pi.get("charges", {}).get("data", [])
                if charges:
                    receipt_url = charges[0].get("receipt_url")
                else:
                    # fallback to latest_charge
                    latest_charge_id = pi.get("latest_charge")
                    if latest_charge_id:
                        charge_obj = stripe.Charge.retrieve(latest_charge_id)
                        receipt_url = charge_obj.get("receipt_url")

                amount_total = pi.get("amount")
                currency = pi.get("currency")

        elif mode == "subscription":
            # subscription might or might not be expanded, but we only expanded subscription.latest_invoice.payment_intent
            sub = session.get("subscription")
            if sub and isinstance(sub, dict):
                # subscription is present
                invoice = sub.get("latest_invoice") or {}
                amount_total = invoice.get("amount_paid")
                currency = invoice.get("currency")

                payment_intent_data = invoice.get("payment_intent")
                if payment_intent_data and isinstance(payment_intent_data, dict):
                    # PaymentIntent is expanded
                    charges = payment_intent_data.get("charges", {}).get("data", [])
                    if charges:
                        receipt_url = charges[0].get("receipt_url")
                    else:
                        latest_charge_id = payment_intent_data.get("latest_charge")
                        if latest_charge_id:
                            charge_obj = stripe.Charge.retrieve(latest_charge_id)
                            receipt_url = charge_obj.get("receipt_url")
                # else: no PaymentIntent => maybe invoice got paid by a different route?

        # Attempt to get the customer name from session
        # session.customer_details might exist, or session.customer is an ID
        if session.get("customer_details"):
            customer_name = session["customer_details"].get("name", "")
        elif session.get("customer"):
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
