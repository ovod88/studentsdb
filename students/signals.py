from django.dispatch import Signal

email_admin_sent_signal = Signal(providing_args=["from_", "message"])