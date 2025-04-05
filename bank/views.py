from decimal import Decimal

import requests
from django.shortcuts import render
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import CustomUser

from .models import Account, Transaction, Transfer
from .serializers import (AccountSerializer, TransactionSerializer,
                          TransferSerializer)
from .services.email_service import (send_transfer_failure_email,
                                     send_transfer_success_email)
from .services.transfer_services import transferService


class AccountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Retrieve account details for a specific user
        """
        user_id = request.user.id 
        try:
            account = Account.objects.get(user_id=user_id)
        except Account.DoesNotExist:
            raise NotFound("Account not found.")
        
        user_name = request.user.name

        transfer = Transfer.objects.filter(sender_id=user_id) | Transfer.objects.filter(receiver_id=user_id)
        transfers_serializer = TransferSerializer(transfer, many=True)
        transactions = Transaction.objects.filter(transfer__in=transfer)
        transactions_serializer = TransactionSerializer(transactions, many=True)

        response_data = {
            "name": user_name,
            "balance": str(account.balance),  
            "transfers": transfers_serializer.data,  
            "transactions": transactions_serializer.data,  
        }
        
        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Create an account for the user
        """
        user_id = request.user.id 
        if Account.objects.filter(user_id=user_id).exists():
            return Response({"detail": "Account already exists."}, status=status.HTTP_400_BAD_REQUEST)
        
        account = Account.objects.create(user_id=user_id)
        serializer = AccountSerializer(account)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class TransferView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Create a new transfer
        """
        serializer = TransferSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        sender_id = request.user.id 
        receiver_email = request.data.get("receiver_email")
        receiver_cpf = request.data.get("receiver_cpf")
        value = request.data.get("value")

        try: 
            if receiver_email:
                receiver = CustomUser.objects.get(email=receiver_email)
            elif receiver_cpf:
                receiver = CustomUser.objects.get(cpf=receiver_cpf)  

        except CustomUser.DoesNotExist:
            return Response({"detail": "Receiver does not exist."}, 
                                status=status.HTTP_404_NOT_FOUND)

        receiver_id = receiver.id

        try:
            transfer, transaction = transferService(request, sender_id, receiver_id, value)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        response_data = {
            "transfer": TransferSerializer(transfer).data,
            "transaction": TransactionSerializer(transaction).data
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

        



class TransactionView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Criar uma transação para uma transferência específica.
        """
        serializer = TransferSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        transfer_id = request.data.get("transfer_id")
        status = request.data.get("status")

        # Verificar se a transferência existe
        try:
            transfer = Transfer.objects.get(id=transfer_id)
        except Transfer.DoesNotExist:
            return Response({"detail": "Transfer not found."}, status=status.HTTP_404_NOT_FOUND)

        # Criar a transação
        transaction = Transaction.objects.create(
            transfer_id=transfer_id,
            status=status,
        )

        return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)




class DepositView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):


        deposit_value = request.data.get("value")
        user_id = request.user.id 
       
        # Verifica se o valor do depósito é válido
        try:
            deposit_value = Decimal(str(deposit_value))
        except (ValueError, decimal.InvalidOperation):
            return Response({"detail": "Valor inválido."}, status=status.HTTP_400_BAD_REQUEST)

        if deposit_value is None or deposit_value <= 0:
            return Response({"detail": "O valor do depósito deve ser maior que zero."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            user_account = Account.objects.get(user_id=user_id)
            user_account.balance += deposit_value
            user_account.save()

            return Response({"detail": f"Depósito de R${deposit_value} realizado com sucesso.",
                    "new_balance": str(user_account.balance)},
                    status=status.HTTP_200_OK)
        except Account.DoesNotExist:
            return Response({"detail": "Conta não encontrada."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": "Erro inesperado ao realizar o depósito."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)