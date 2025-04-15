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
        return Response({"error": str(e)}, status=400)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_checkout_session_details(request):
    session_id = request.GET.get('session_id')
    if not session_id:
        return Response({"error": "No session ID provided"}, status=400)

    try:
        session = stripe.checkout.Session.retrieve(
            session_id,
            expand=['payment_intent', 'subscription']
        )

        amount_total = None
        currency = None
        receipt_url = None
        customer_name = ""

        # --- One-time or immediate payment ---
        if session.payment_intent:
            payment_intent = stripe.PaymentIntent.retrieve(
                session.payment_intent.id if isinstance(session.payment_intent, stripe.PaymentIntent) else session.payment_intent,
                expand=['charges']
            )
            charges = payment_intent.get('charges', {}).get('data', [])
            receipt_url = charges[0].get('receipt_url') if charges else None
            amount_total = payment_intent.get('amount')
            currency = payment_intent.get('currency')

        # --- Subscription (delayed billing or trial) ---
        elif session.subscription:
            subscription = stripe.Subscription.retrieve(
                session.subscription.id if isinstance(session.subscription, stripe.Subscription) else session.subscription,
                expand=['latest_invoice.payment_intent']
            )
            invoice = subscription.get('latest_invoice')
            if invoice:
                amount_total = invoice.get('amount_paid')
                currency = invoice.get('currency')
                payment_intent = invoice.get('payment_intent')
                if payment_intent:
                    payment_intent = stripe.PaymentIntent.retrieve(
                        payment_intent.id if isinstance(payment_intent, stripe.PaymentIntent) else payment_intent,
                        expand=['charges']
                    )
                    charges = payment_intent.get('charges', {}).get('data', [])
                    receipt_url = charges[0].get('receipt_url') if charges else None

        # Optional: retrieve customer details
        if session.get('customer'):
            customer = stripe.Customer.retrieve(session['customer'])
            customer_name = customer.get('name', "")

        return Response({
            "customer_name": customer_name,
            "amount_total": amount_total,
            "currency": currency,
            "receipt_url": receipt_url,
        })

    except Exception as e:
        return Response({"error": str(e)}, status=400)
