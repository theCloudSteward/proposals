# proposals/views.py
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

# Checkout session creation view – correctly exempt from CSRF and authentication
@api_view(['POST'])
@authentication_classes([])  # CRITICAL!
@permission_classes([AllowAny])  # CRITICAL!
def create_checkout_session(request):
    data = request.data
    slug = data.get('slug')
    option = data.get('option')

    page = get_object_or_404(ClientPage, slug=slug)

    line_items = []
    mode = 'payment'

    if option == 'project_only_price':
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'unit_amount': int(page[option] * 100),
                'product_data': {
                    'name': f"{page.company_name} Project",
                },
            },
            'quantity': 1,
        })
    else:
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'unit_amount': int(page.project_with_subscription_price * 100),
                'product_data': {
                    'name': f"{page.company_name} Project",
                },
            },
            'quantity': 1,
        })
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'unit_amount': int(page[option] * 100),
                'recurring': {'interval': 'month'},
                'product_data': {
                    'name': f"{page.company_name} Subscription",
                },
            },
            'quantity': 1,
        })
        mode = 'subscription'

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode=mode,
        # Using double curly braces so that Stripe replaces the placeholder with the actual session ID
        success_url=f"https://proposals.thecloudsteward.com/success?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"https://proposals.thecloudsteward.com/{slug}",
    )

    return Response({"url": session.url})

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
