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
    plan_title = data.get('plan_title') or "Support Plan Subscription"  # fallback

    if not slug or not option:
        return Response({"error": "Missing slug or option"}, status=400)

    page = get_object_or_404(ClientPage, slug=slug)

    try:
        if option == 'project_only_price':
            project_price = int(page.project_only_price * 100)  # Convert to cents
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
                customer_email=email,  # ensures Stripe can email a receipt
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

            # One-time fee price
            one_time_price = stripe.Price.create(
                unit_amount=project_price,
                currency='usd',
                product_data={
                    'name': "One-Time Project Fee",
                },
            )

            # Recurring fee price (subscription)
            recurring_price = stripe.Price.create(
                unit_amount=subscription_price,
                currency='usd',
                recurring={'interval': 'month'},
                product_data={
                    'name': plan_title,
                },
            )

            # Create Checkout Session in subscription mode
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {'price': one_time_price.id, 'quantity': 1},
                    {'price': recurring_price.id, 'quantity': 1},
                ],
                mode='subscription',
                customer_email=email,
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
        # 1. Retrieve the Checkout Session without expanding payment_intent
        session = stripe.checkout.Session.retrieve(session_id)
        logger.debug("Retrieved Checkout Session object:\n%r", session)

        mode = session.get("mode")
        logger.debug("Session mode: %s", mode)
        amount_total = None
        currency = None
        receipt_url = None

        if mode == "payment":
            # --- One-time Payment ---
            payment_intent_id = session.get("payment_intent")
            if not payment_intent_id:
                raise Exception("No PaymentIntent in one-time mode session.")

            logger.debug("Retrieving PaymentIntent %s with expand=['charges']", payment_intent_id)
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id, expand=["charges"])
            logger.debug("Retrieved PaymentIntent:\n%r", payment_intent)

            charges = payment_intent.get("charges", {}).get("data", [])
            logger.debug("PaymentIntent charges: %r", charges)
            if charges:
                receipt_url = charges[0].get("receipt_url")
            else:
                # fallback if no charges array
                latest_charge_id = payment_intent.get("latest_charge")
                if latest_charge_id:
                    logger.debug("Retrieving Charge %s directly", latest_charge_id)
                    charge_obj = stripe.Charge.retrieve(latest_charge_id)
                    logger.debug("Charge object:\n%r", charge_obj)
                    receipt_url = charge_obj.get("receipt_url")

            amount_total = payment_intent.get("amount")
            currency = payment_intent.get("currency")

        elif mode == "subscription":
            # --- Subscription Payment ---
            sub_id = session.get("subscription")
            if not sub_id:
                raise Exception("No Subscription ID in session.")

            # Expand latest_invoice and its charge
            logger.debug("Retrieving Subscription %s with expand=['latest_invoice.charge']", sub_id)
            subscription = stripe.Subscription.retrieve(
                sub_id,
                expand=["latest_invoice.charge", "latest_invoice.payment_intent"]
            )
            logger.debug("Retrieved Subscription:\n%r", subscription)

            invoice = subscription.get("latest_invoice")
            if not invoice:
                raise Exception("No latest invoice in subscription.")
            logger.debug("Subscription latest_invoice: %r", invoice)

            # Basic invoice amount details
            amount_total = invoice.get("amount_paid")
            currency = invoice.get("currency")

            # 2a. If there's a PaymentIntent on the invoice, use it.
            pi_data = invoice.get("payment_intent")
            if pi_data:
                pi_id = pi_data if isinstance(pi_data, str) else pi_data["id"]
                logger.debug("Retrieving PaymentIntent %s with expand=['charges']", pi_id)
                pi = stripe.PaymentIntent.retrieve(pi_id, expand=["charges"])
                logger.debug("Subscription PaymentIntent:\n%r", pi)
                charges = pi.get("charges", {}).get("data", [])
                if charges:
                    receipt_url = charges[0].get("receipt_url")
                else:
                    # fallback if no charges array
                    latest_charge_id = pi.get("latest_charge")
                    if latest_charge_id:
                        logger.debug("Retrieving Charge %s directly (subscription fallback)", latest_charge_id)
                        charge_obj = stripe.Charge.retrieve(latest_charge_id)
                        logger.debug("Retrieved Charge object:\n%r", charge_obj)
                        receipt_url = charge_obj.get("receipt_url")

            # 2b. If invoice.payment_intent is missing, check invoice.charge (old flow)
            elif "charge" in invoice:
                charge_data = invoice["charge"]  # could be an ID or an expanded object
                if isinstance(charge_data, dict):
                    # Already expanded
                    receipt_url = charge_data.get("receipt_url")
                elif isinstance(charge_data, str):
                    # Retrieve the Charge by ID
                    logger.debug("No payment_intent. Retrieving charge %s directly.", charge_data)
                    charge_obj = stripe.Charge.retrieve(charge_data)
                    receipt_url = charge_obj.get("receipt_url")
                else:
                    logger.debug("Unexpected 'charge' format in invoice.")

        # 3. Retrieve customer details
        customer_name = ""
        if session.get("customer"):
            customer_id = session["customer"]
            logger.debug("session.customer exists: %s", customer_id)
            customer = stripe.Customer.retrieve(customer_id)
            logger.debug("Retrieved customer:\n%r", customer)
            customer_name = customer.get("name", "")
        elif session.get("customer_details"):
            logger.debug("session.customer_details: %r", session["customer_details"])
            customer_name = session["customer_details"].get("name", "")

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
