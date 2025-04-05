from django.conf import settings
from django.core.mail import send_mail


def send_email(subject, message, recipient_list):
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=False,
    )

def send_transfer_success_email(sender_email, receiver_email, value):
    message = f'A transferência de R${value} para o usuário {receiver_email} foi concluída com sucesso.'
    send_email('Transferência Concluída', message, [sender_email])

def receiver_transfer_success_email(receiver_email, sender_name, value):
    message = f'Você recebeu uma transferência de R${value} de {sender_name}.'
    send_email('Transferência Recebida', message, [receiver_email])

def send_transfer_failure_email(sender_email, receiver_email, value):
    message = f'A transferência de R${value} para o usuário {receiver_email} falhou. Você foi reembolsado.'
    send_email('Falha na Transferência', message, [sender_email])
