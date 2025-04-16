# proposals/webhooks.py

import logging
import stripe

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest

from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail

logger = logging.getLogger(__name__)
stripe.api_key = settings.STRIPE_SECRET_KEY
WEBHOOK_SECRET = settings.STRIPE_WEBHOOK_SECRET  # from your Stripe Dashboard

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, WEBHOOK_SECRET
        )
    except ValueError:
        logger.warning("Invalid JSON payload")
        return HttpResponseBadRequest()
    except stripe.error.SignatureVerificationError:
        logger.warning("Invalid Stripe signature")
        return HttpResponseBadRequest()

    # Handle checkout.session.completed
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        customer_email = (
            session.get("customer_details", {}).get("email")
            or session.get("customer_email")
        )
        if customer_email:
            _send_instruction_email(customer_email)
            logger.info(
                "Sent follow‑up email to %s for session %s",
                customer_email,
                session["id"],
            )

    # Handle initial subscription invoice payment
    elif event["type"] == "invoice.payment_succeeded":
        invoice = event["data"]["object"]
        if (
            invoice.get("billing_reason") == "subscription_create"
            and invoice.get("customer_email")
        ):
            _send_instruction_email(invoice["customer_email"])
            logger.info(
                "Sent onboarding email to %s for subscription %s",
                invoice["customer_email"],
                invoice["subscription"],
            )

    return HttpResponse(status=200)


def _send_instruction_email(to_email: str):
    subject = "Welcome aboard – next steps for your Cloud Steward project"
    body = (
        "Hi there,\n\n"
        "Thanks for your purchase! We'll reach out shortly with onboarding "
        "details.\n\n"
        "If you have any questions just reply to this email.\n\n"
        "— The Cloud Steward Team"
    )
    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [to_email],
        fail_silently=False,
    )
