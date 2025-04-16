# proposals/webhooks.py
import json, logging, stripe
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail            # or your favourite ESP wrapper

logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY
WEBHOOK_SECRET = getattr(settings, "STRIPE_WEBHOOK_SECRET", "")

@csrf_exempt
def stripe_webhook(request):
    payload     = request.body
    sig_header  = request.META.get("HTTP_STRIPE_SIGNATURE", "")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, WEBHOOK_SECRET)
    except ValueError:
        logger.warning("⚠️  Invalid JSON on webhook")
        return HttpResponseBadRequest()
    except stripe.error.SignatureVerificationError:
        logger.warning("⚠️  Invalid signature on webhook")
        return HttpResponseBadRequest()

    _log_event(event)      # <‑‑ optional but handy while testing

    try:
        #
        # ---- handle only the events you care about ------------------------
        #
        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            customer_email = (
                session.get("customer_details", {}).get("email") or
                session.get("customer_email")
            )
            if customer_email:
                _safe_send_instruction_email(customer_email, session)

        elif event["type"] == "invoice.payment_succeeded":
            invoice = event["data"]["object"]
            if (invoice.get("billing_reason") == "subscription_create" and
                    invoice.get("customer_email")):
                _safe_send_instruction_email(invoice["customer_email"], invoice)

    except Exception:
        # Any *coding* error on our side is logged, but we still acknowledge
        logger.exception("Unhandled error inside webhook handler")
        # return HttpResponse(status=200)   # <-- Stripe sees success anyway

    return HttpResponse(status=200)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _safe_send_instruction_email(to_email: str, context):
    """
    Wrapper around the real mail‑send that catches SMTP / config errors
    so the webhook never returns 500.
    """
    try:
        _send_instruction_email(to_email, context)
        logger.info("✅ Sent follow‑up email to %s (context id %s)",
                    to_email, context.get("id"))
    except Exception:
        logger.exception("❌ Could not send follow‑up email to %s", to_email)


def _send_instruction_email(to_email: str, context):
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
        fail_silently=True,      # suppress SMTP errors in production webhook
    )


def _log_event(event):
    """
    Tiny helper so you can watch Stripe events hit your server:
        sudo journalctl -u gunicorn -f | grep "🔔"
    """
    logger.debug("🔔 Stripe event received: %s", event["type"])
