import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import ClientPage
from .serializers import ClientPageSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY

class ClientPageViewSet(ReadOnlyModelViewSet):
    queryset = ClientPage.objects.all()
    serializer_class = ClientPageSerializer
    lookup_field = 'slug'

    def retrieve(self, request, slug=None, *args, **kwargs):
        client_page = get_object_or_404(ClientPage, slug=slug)
        serializer = self.get_serializer(client_page)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_checkout_session_details(request):
    session_id = request.GET.get('session_id')
    if not session_id:
        return Response({"error": "No session ID provided"}, status=400)
    try:
        # Expand both payment_intent and subscription for flexibility.
        session = stripe.checkout.Session.retrieve(
            session_id,
            expand=['payment_intent', 'subscription']
        )

        payment_intent = None
        receipt_url = None
        amount_total = None
        currency = None

        # Case 1: When a payment_intent exists (one-time payment or immediate charge part of a subscription)
        if session.payment_intent:
            if isinstance(session.payment_intent, str):
                payment_intent = stripe.PaymentIntent.retrieve(
                    session.payment_intent,
                    expand=['charges']
                )
            else:
                payment_intent = session.payment_intent
                # Ensure charges are populated.
                if not payment_intent.get('charges'):
                    payment_intent = stripe.PaymentIntent.retrieve(
                        payment_intent.id,
                        expand=['charges']
                    )
            charges = payment_intent.get('charges', {}).get('data', [])
            receipt_url = charges[0].get('receipt_url') if charges and charges[0].get('receipt_url') else None
            amount_total = payment_intent.get('amount')
            currency = payment_intent.get('currency')

        # Case 2: When no immediate payment_intent exists but it’s a subscription session
        elif session.subscription:
            subscription = session.subscription
            # Retrieve subscription details and expand latest_invoice.payment_intent
            if isinstance(subscription, str):
                subscription = stripe.Subscription.retrieve(
                    subscription,
                    expand=['latest_invoice.payment_intent']
                )
            else:
                if not subscription.get('latest_invoice'):
                    subscription = stripe.Subscription.retrieve(
                        subscription.id,
                        expand=['latest_invoice.payment_intent']
                    )
            invoice = subscription.get('latest_invoice')
            if invoice:
                # Capture the immediate charge if available
                payment_intent = invoice.get('payment_intent')
                amount_total = invoice.get('amount_paid')  # could be 0 if under trial
                currency = invoice.get('currency')
                if payment_intent:
                    if isinstance(payment_intent, str):
                        payment_intent = stripe.PaymentIntent.retrieve(
                            payment_intent,
                            expand=['charges']
                        )
                    else:
                        if not payment_intent.get('charges'):
                            payment_intent = stripe.PaymentIntent.retrieve(
                                payment_intent.id,
                                expand=['charges']
                            )
                    charges = payment_intent.get('charges', {}).get('data', [])
                    receipt_url = charges[0].get('receipt_url') if charges and charges[0].get('receipt_url') else None

        # Retrieve customer details if available
        customer_name = ""
        customer_id = session.get('customer')
        if customer_id:
            customer = stripe.Customer.retrieve(customer_id)
            customer_name = customer.get('name', "")

        return Response({
            "customer_name": customer_name,
            "amount_total": amount_total,
            "currency": currency,
            "receipt_url": receipt_url,
        })
    except Exception as e:
        return Response({"error": str(e)}, status=400)

# New endpoint to retrieve session details for the success page
@api_view(['GET'])
@permission_classes([AllowAny])
def get_checkout_session_details(request):
    session_id = request.GET.get('session_id')
    if not session_id:
        return Response({"error": "No session ID provided"}, status=400)
    try:
        # Retrieve the Checkout Session and expand the PaymentIntent
        session = stripe.checkout.Session.retrieve(
            session_id,
            expand=['payment_intent']
        )

        # Check if payment_intent is a string (not expanded) or an object
        if isinstance(session.payment_intent, str):
            payment_intent = stripe.PaymentIntent.retrieve(
                session.payment_intent,
                expand=['charges']
            )
        else:
            payment_intent = session.payment_intent
            # If charges are not expanded, retrieve them.
            if not payment_intent.get('charges'):
                payment_intent = stripe.PaymentIntent.retrieve(
                    payment_intent.id,
                    expand=['charges']
                )

        # Extract the receipt URL from the first charge, if available
        charges = payment_intent.get('charges', {}).get('data', [])
        receipt_url = charges[0].get('receipt_url') if charges and charges[0].get('receipt_url') else None

        # Retrieve customer details if available
        customer_name = ""
        customer_id = session.get('customer')
        if customer_id:
            customer = stripe.Customer.retrieve(customer_id)
            customer_name = customer.get('name', "")

        return Response({
            "customer_name": customer_name,
            "amount_total": payment_intent.get('amount'),
            "currency": payment_intent.get('currency'),
            "receipt_url": receipt_url,
        })
    except Exception as e:
        return Response({"error": str(e)}, status=400)