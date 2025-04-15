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

logger = logging.getLogger(__name__)  # <-- This is your logger

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
    email = data.get('email')  # Optional but recommended

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
                customer_email=email,  # ensure receipt can be emailed
                payment_intent_data={
                    'receipt_email': email  # triggers Stripe to send a receipt
                } if email else {},
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
                    'name': "Support Plan Subscription",
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
                subscription_data={
                    'trial_period_days': 30,
                },
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
    session_id = request.GET.get('session_id')
    if not session_id:
        return Response({"error": "No session ID provided"}, status=400)

    logger.debug("get_checkout_session_details called with session_id=%s", session_id)

    try:
        # Retrieve the Checkout Session. Expand payment_intent and subscription.
        logger.debug("Retrieving Checkout Session with expand=['payment_intent', 'subscription']")
        session = stripe.checkout.Session.retrieve(
            session_id,
            expand=['payment_intent', 'subscription']
        )
        logger.debug("Retrieved Checkout Session object:\n%r", session)

        amount_total = None
        currency = None
        receipt_url = None
        customer_name = ""

        # One-time payment flow
        if session.payment_intent:
            logger.debug("Session is one-time payment. PaymentIntent: %r", session.payment_intent)
            pi_id = (session.payment_intent.id
                     if isinstance(session.payment_intent, stripe.PaymentIntent)
                     else session.payment_intent)
            logger.debug("Retrieving PaymentIntent %s with expand=['charges']", pi_id)
            payment_intent = stripe.PaymentIntent.retrieve(pi_id, expand=['charges'])
            logger.debug("Retrieved PaymentIntent:\n%r", payment_intent)
            charges = payment_intent.get('charges', {}).get('data', [])
            logger.debug("PaymentIntent charges: %r", charges)
            if not charges:
                latest_charge_id = payment_intent.get('latest_charge')
                logger.debug("No charges in PaymentIntent; latest_charge=%s", latest_charge_id)
                if latest_charge_id:
                    logger.debug("Retrieving Charge %s directly", latest_charge_id)
                    charge_obj = stripe.Charge.retrieve(latest_charge_id)
                    logger.debug("Charge object:\n%r", charge_obj)
                    receipt_url = charge_obj.get('receipt_url')
                    logger.debug("Fallback receipt_url: %s", receipt_url)
            else:
                receipt_url = charges[0].get('receipt_url')
                logger.debug("Found receipt_url: %s", receipt_url)
            amount_total = payment_intent.get('amount')
            currency = payment_intent.get('currency')
            logger.debug("Amount total: %s, currency: %s", amount_total, currency)

        # Subscription payment flow
        elif session.subscription:
            logger.debug("Session is subscription. Subscription: %r", session.subscription)
            sub_id = (session.subscription.id
                      if isinstance(session.subscription, stripe.Subscription)
                      else session.subscription)
            logger.debug("Retrieving Subscription %s with expand=['latest_invoice.payment_intent']", sub_id)
            subscription = stripe.Subscription.retrieve(
                sub_id,
                expand=['latest_invoice.payment_intent']
            )
            logger.debug("Retrieved Subscription:\n%r", subscription)
            invoice = subscription.get('latest_invoice')
            if invoice:
                logger.debug("Subscription latest_invoice: %r", invoice)
                amount_total = invoice.get('amount_paid')
                currency = invoice.get('currency')
                payment_intent_data = invoice.get('payment_intent')
                if payment_intent_data:
                    pi_id = (payment_intent_data.id
                             if isinstance(payment_intent_data, stripe.PaymentIntent)
                             else payment_intent_data)
                    logger.debug("Invoice references PaymentIntent ID: %s", pi_id)
                    payment_intent = stripe.PaymentIntent.retrieve(pi_id, expand=['charges'])
                    logger.debug("Subscription PaymentIntent:\n%r", payment_intent)
                    charges = payment_intent.get('charges', {}).get('data', [])
                    logger.debug("Subscription PaymentIntent charges: %r", charges)
                    if not charges:
                        latest_charge_id = payment_intent.get('latest_charge')
                        logger.debug("No charges in PaymentIntent; latest_charge=%s", latest_charge_id)
                        if latest_charge_id:
                            logger.debug("Retrieving Charge %s directly (subscription fallback)", latest_charge_id)
                            charge_obj = stripe.Charge.retrieve(latest_charge_id)
                            logger.debug("Charge object:\n%r", charge_obj)
                            receipt_url = charge_obj.get('receipt_url')
                            logger.debug("Fallback receipt_url (sub): %s", receipt_url)
                    else:
                        receipt_url = charges[0].get('receipt_url')
                        logger.debug("Found subscription receipt_url: %s", receipt_url)

        # Fetch customer name from either session.customer or session.customer_details
        if session.get('customer'):
            logger.debug("session.customer exists: %s", session['customer'])
            customer = stripe.Customer.retrieve(session['customer'])
            logger.debug("Retrieved customer:\n%r", customer)
            customer_name = customer.get('name', "")
        elif session.get('customer_details'):
            logger.debug("session.customer_details exists: %r", session.get('customer_details'))
            customer_name = session.get('customer_details').get('name', "")

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
