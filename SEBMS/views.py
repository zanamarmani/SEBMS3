from django.conf import settings
from django.contrib.auth.views import PasswordResetView

class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_name'] = settings.PROJECT_NAME  # Pass the project name
        context['domain'] = settings.PASSWORD_RESET_DOMAIN  # Use the domain defined in settings
        return context
