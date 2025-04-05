
from decimal import Decimal

import requests
from rest_framework import status
from rest_framework.response import Response

from ..models import Account, Transaction, Transfer
from ..serializers import TransferSerializer
from .email_service import (receiver_transfer_success_email,
                            send_transfer_failure_email,
                            send_transfer_success_email)


def transferService(request, sender_id, receiver_id, value):

    try:
        sender_account = Account.objects.get(user_id=sender_id)
    except Account.DoesNotExist:
        raise ValueError("Conta do remetende não encontrada.")

    try:
        receiver_account = Account.objects.get(user_id=receiver_id)
    except Account.DoesNotExist:
        raise ValueError("Conta de destinatário não encontrada.")

    if receiver_account.user.id == sender_account.user.id:
        raise ValueError("Não é possível transferir para a própria conta.")

    if request.user.lojista:
        raise ValueError("Não autorizado. Lojistas não podem realizar transferências.")

    if sender_account.balance < value:
        raise ValueError("Saldo insuficiente.")

    # Criar a transferência
    transfer = Transfer.objects.create(
        sender_id=sender_id,
        receiver_id=receiver_id,
        value=value,
        status="pendente",  # Transação ainda pendente até ser autorizada
        authorized=False,  # A autorização externa ainda precisa ser verificada
    )

    sender_account.balance -= Decimal(str(value))
    sender_account.save()

    transaction = Transaction.objects.create(
        transfer=transfer,  # Relaciona a transação com a transferência
        status="pendente"  # A transação começa com status pendente
    )

    # Simulando a autorização externa
    try:
        auth_response = requests.get("https://util.devi.tools/api/v2/authorize")
        #caso a resposta não seja 200, cancelamos a transferência
        if auth_response.status_code != 200:
            transfer.status = "cancelada"
            transfer.save()

            # Marca a transação como falhada
            transaction.status = "falhou"
            transaction.save()

            sender_account.balance += Decimal(str(value))
            sender_account.save()

            send_transfer_failure_email(request.user.email, receiver_account.user.email, value)

            raise ValueError("Falha na autorização externa. Transação revertida.")
    except requests.RequestException as e:
        # Se ocorrer qualquer outro erro, cancelamos a transferência
        transfer.status = "cancelada"
        transfer.save()

        transaction.status = "falhou"
        transaction.save()

        sender_account.balance += Decimal(str(value))
        sender_account.save()

        send_transfer_failure_email(request.user.email, receiver_account.user.email, value)

        raise ValueError("Falha na autorização externa. Transação revertida.")

    # Se a autorização for bem-sucedida
    receiver_account.balance += Decimal(str(value))
    receiver_account.save()

    transfer.status = "concluída"
    transfer.authorized = True
    transfer.save()

    # Atualiza o status da transação para concluída
    transaction.status = "completa"
    transaction.save()

    send_transfer_success_email(request.user.email, receiver_account.user.email, value)
    receiver_transfer_success_email(receiver_account.user.email, request.user.name, value)

    return transfer, transaction
