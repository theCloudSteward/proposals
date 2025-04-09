import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import ClientPage
import logging

# Set up logging to debug issues
logger = logging.getLogger(__name__)
stripe.api_key = settings.STRIPE_SECRET_KEY

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def create_checkout_session(request):
    # Extract slug and option from request data
    data = request.data
    slug = data.get('slug')
    option = data.get('option')

    # Validate input
    if not slug or not option:
        return Response({"error": "Missing slug or option"}, status=status.HTTP_400_BAD_REQUEST)

    # Fetch the ClientPage object
    page = get_object_or_404(ClientPage, slug=slug)

    try:
        if option == 'project_only_price':
            # Handle one-time project payment
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
                success_url="https://proposals.thecloudsteward.com/success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=f"https://proposals.thecloudsteward.com/{slug}",
            )
            return Response({"url": session.url})
        else:
            # Handle subscription option
            if not hasattr(page, option):
                return Response({"error": f"Invalid option: {option}"}, status=status.HTTP_400_BAD_REQUEST)

            # Get subscription price dynamically
            subscription_price = int(getattr(page, option) * 100)  # Convert to cents

            # Log for debugging
            logger.info(f"Creating subscription for {page.company_name} with price={subscription_price}")

            # Create recurring price for subscription
            recurring_price = stripe.Price.create(
                unit_amount=subscription_price,
                currency='usd',
                recurring={'interval': 'month'},
                product_data={'name': f"{page.company_name} Monthly Subscription"},
            )

            # Create checkout session with subscription
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price': recurring_price.id,
                    'quantity': 1,
                }],
                mode='subscription',
                success_url="https://proposals.thecloudsteward.com/success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=f"https://proposals.thecloudsteward.com/{slug}",
            )
            return Response({"url": session.url})

    except stripe.error.StripeError as e:
        # Handle Stripe-specific errors
        logger.error(f"Stripe error: {str(e)}")
        return Response({"error": f"Stripe error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
    except AttributeError as e:
        # Handle missing field errors
        logger.error(f"Attribute error: {str(e)}")
        return Response({"error": f"Invalid field in ClientPage: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        # Catch all other unexpected errors
        logger.error(f"Unexpected error: {str(e)}")
        return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)