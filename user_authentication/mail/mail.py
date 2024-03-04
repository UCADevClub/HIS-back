from django.core.mail import send_mail
from django.conf import settings


def send_password(password: str, targets: list[str]) -> None:
    title = 'Password'
    message = password

    send_mail(
        subject=title,
        message=f'{message=}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=targets,
        fail_silently=False
    )
