from django.db.models.signals import post_save
from django.dispatch import receiver

from bank.models import Account

from .models import CustomUser


@receiver(post_save, sender=CustomUser)
def create_account_for_new_user(sender, instance, created, **kwargs):
    """
    Cria automaticamente uma conta quando um novo usuário é registrado.
    """
    if created:
        # Se o usuário foi criado (não atualizado)
        Account.objects.create(user_id=instance.id)