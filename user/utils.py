from django.core.mail import send_mail

from board import settings


def send_activation_mail(email, activation_code):
    subject = 'Активация аккаунта'
    message = f"""
                Здравствуйте, уважаемый пользователь! Спасибо за регистрацию на нашем сайте!
                Для активации Вашего аккаунта пройдите по ссылке: 
                http://127.0.0.1:8000/api/accounts/activate/{activation_code}
                
    """

    from_ = settings.EMAIL_HOST_USER
    emails = [email, ]

    send_mail(subject, message, from_, emails)
    # auth_user='alld.mail89@gmail.com', auth_password=

