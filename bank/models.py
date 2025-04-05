from django.db import models

from users.models import CustomUser


class Account(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="conta")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conta de {self.user_id.name} - Saldo: R${self.balance}"


class Transfer(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="transfers_sent")
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="transfers_received")
    value = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('pendente', 'Pendente'), ('concluída', 'Concluída'), ('cancelada', 'Cancelada')], default='pendente')
    authorized = models.BooleanField(default=False)

    def __str__(self):
        return f"Transferência de {self.sender} para {self.receiver} - R${self.value}"


class Transaction(models.Model):
    transfer = models.ForeignKey(Transfer, related_name='Transactions', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('completa', 'Completa'), ('falhou', 'Falhou')], default='falhou')