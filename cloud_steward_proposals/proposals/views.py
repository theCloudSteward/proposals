import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import ClientPage
from .serializers import ClientPageSerializer
import logging

# Configure logging for debugging
logger = logging.getLogger(__name__)

# Set Stripe API key from Django settings
stripe.api_key = settings.STRIPE_SECRET_KEY

# ClientPageViewSet: Unchanged to preserve original functionality
class ClientPageViewSet(ReadOnlyModelViewSet):
    queryset = ClientPage.objects.all()
    serializer_class = ClientPageSerializer
    lookup_field = 'slug'

    def retrieve(self, request, slug=None, *args, **kwargs):
        client_page = get_object_or_404(ClientPage, slug=slug)
        serializer = self.get_serializer(client_page)
        return Response(serializer.data)

# create_checkout_session: Updated with fixed Stripe logic
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def create_checkout_session(request):
    data = request.data
    slug = data.get('slug')
    option = data.get('option')

    # Validate required input
    if not slug or not option:
        return Response({"error": "Missing slug or option"}, status=status.HTTP_400_BAD_REQUEST)

    # Fetch the ClientPage object
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
                success_url=f"https://proposals.thecloudsteward.com/success?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"https://proposals.thecloudsteward.com/{slug}",
            )
            return Response({"url": session.url})
        else:
            # Validate the subscription option
            if not hasattr(page, option):
                return Response({"error": f"Invalid option: {option}"}, status=status.HTTP_400_BAD_REQUEST)

            # Get prices dynamically and convert to cents
            subscription_price = int(getattr(page, option) * 100)
            project_price = int(page.project_with_subscription_price * 100)

            # Create one-time price for immediate project fee
            one_time_price = stripe.Price.create(
                unit_amount=project_price,
                currency='usd',
                product_data={
                    'name': f"{page.company_name} One-Time Project Fee",
                },
            )

            # Create recurring price for subscription starting in 30 days
            recurring_price = stripe.Price.create(
                unit_amount=subscription_price,
                currency='usd',
                recurring={'interval': 'month'},
                product_data={
                    'name': f"{page.company_name} Monthly Subscription (starts in 30 days)",
                },
            )

            # Create checkout session with both one-time and subscription items
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
                    'trial_period_days': 30,  # Subscription starts after 30 days
                },
                success_url=f"https://proposals.thecloudsteward.com/success?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"https://proposals.thecloudsteward.com/{slug}",
            )
            return Response({"url": session.url})

    except stripe.error.StripeError as e:
        logger.error(f"Stripe error: {str(e)}")
        return Response({"error": f"Stripe error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
    except AttributeError as e:
        logger.error(f"Attribute error: {str(e)}")
        return Response({"error": f"Invalid field in ClientPage: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# get_checkout_session_details: Unchanged but with robust error handling
@api_view(['GET'])
@permission_classes([AllowAny])
def get_checkout_session_details(request):
    session_id = request.GET.get('session_id')
    if not session_id:
        return Response({"error": "No session ID provided"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        # Retrieve the checkout session
        session = stripe.checkout.Session.retrieve(session_id)
        line_items = stripe.checkout.Session.list_line_items(session_id)

        # Format line items for response
        items = []
        for item in line_items.data:
            price = item.price
            if price.recurring:
                interval = price.recurring.interval
                description = f"{item.description}"
                item_type = 'subscription'
            else:
                description = item.description
                item_type = 'one-time'
            items.append({
                'description': description,
                'amount': item.amount_total / 100,  # Convert cents to dollars
                'currency': item.currency,
                'type': item_type,
            })

        # Get receipt URL if available
        receipt_url = None
        if session.payment_intent:
            payment_intent = stripe.PaymentIntent.retrieve(session.payment_intent)
            if payment_intent.charges.data:
                receipt_url = payment_intent.charges.data[0].receipt_url

        # Get customer name if available
        customer_name = ""
        customer_id = session.get('customer')
        if customer_id:
            customer = stripe.Customer.retrieve(customer_id)
            customer_name = customer.get('name', "")

        return Response({
            "customer_name": customer_name,
            "items": items,
            "receipt_url": receipt_url,
        })
    except stripe.error.StripeError as e:
        logger.error(f"Stripe error in session retrieval: {str(e)}")
        return Response({"error": f"Stripe error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Unexpected error in session retrieval: {str(e)}")
        return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)