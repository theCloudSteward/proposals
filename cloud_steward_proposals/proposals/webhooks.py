# payments/webhooks.py
import json, logging, stripe
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail      # or your favourite ESP wrapper

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
        return HttpResponseBadRequest()        # invalid JSON
    except stripe.error.SignatureVerificationError:
        return HttpResponseBadRequest()        # invalid signature

    # ---- handle the events you care about ---------------------------------
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        # example metadata you set in create_checkout_session()
        # project_id = session["metadata"].get("project_id")

        customer_email = (
            session.get("customer_details", {}).get("email") or
            session.get("customer_email")
        )
        if customer_email:
            _send_instruction_email(customer_email, session)
            logger.info("Sent follow‑up email to %s for session %s",
                        customer_email, session["id"])

    elif event["type"] == "invoice.payment_succeeded":
        invoice = event["data"]["object"]
        customer_email = invoice.get("customer_email")
        if customer_email and invoice["billing_reason"] == "subscription_create":
            _send_instruction_email(customer_email, invoice)

    # -----------------------------------------------------------------------
    return HttpResponse(status=200)


def _send_instruction_email(to_email: str, context):
    """
    Craft and send whatever 'next steps' email you want.
    This is *just* an example using Django‑core send_mail; swap in Postmark,
    Amazon SES, SendGrid, etc. as you prefer.
    """
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
