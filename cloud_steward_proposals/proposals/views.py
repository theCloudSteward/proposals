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

# Checkout session creation view – updated to use Stripe's default success page
@api_view(['POST'])
@authentication_classes([])  # CRITICAL!
@permission_classes([AllowAny])  # CRITICAL!
def create_checkout_session(request):
    data = request.data
    slug = data.get('slug')
    option = data.get('option')

    if not slug or not option:
        return Response({"error": "Missing slug or option"}, status=400)

    page = get_object_or_404(ClientPage, slug=slug)

    try:
        if option == 'project_only_price':
            # One-time payment for project_only_price
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
                cancel_url=f"https://proposals.thecloudsteward.com/{slug}",
            )
            return Response({"url": session.url})
        else:
            # Validate the subscription option
            if not hasattr(page, option):
                return Response({"error": f"Invalid option: {option}"}, status=400)

            # Get prices and convert to cents
            subscription_price = int(getattr(page, option) * 100)
            project_price = int(page.project_with_subscription_price * 100)

            # Create one-time price for immediate project fee
            one_time_price = stripe.Price.create(
                unit_amount=project_price,
                currency='usd',
                product_data={
                    'name': "One-Time Project Fee",
                },
            )

            # Create recurring price for subscription
            recurring_price = stripe.Price.create(
                unit_amount=subscription_price,
                currency='usd',
                recurring={'interval': 'month'},
                product_data={
                    'name': "Support Plan Subscription",
                },
            )

            # Create checkout session with both prices and a 30-day trial for subscription
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price': one_time_price.id,
                        'quantity': 1,
                    },
                    {
                        'price': recurring_price.id,
                        'quantity': 1,
                    },
                ],
                mode='subscription',
                subscription_data={
                    'trial_period_days': 30,  # Subscription billing starts after 30 days
                },
                cancel_url=f"https://proposals.thecloudsteward.com/{slug}",
            )
            return Response({"url": session.url})

    except stripe.error.StripeError as e:
        return Response({"error": str(e)}, status=400)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

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