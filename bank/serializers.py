from decimal import Decimal

from rest_framework import serializers

from users.models import CustomUser

from .models import Account, Transaction, Transfer


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'user_id', 'balance', 'creation_date']


class TransferSerializer(serializers.ModelSerializer):

    receiver_email = serializers.EmailField(required=False)
    receiver_cpf = serializers.CharField(required=False)

    class Meta:
        model = Transfer
        fields = ["id", "sender", "receiver", "value", "receiver_email", "receiver_cpf"]
        extra_kwargs = {
            "sender": {"required": False, "read_only": True},
            "receiver": {"required": False, "read_only": True},
        }
    def validate(self, attrs):
        """
        Garante que pelo menos um dos campos receiver_email ou receiver_cpf seja fornecido.
        """
        receiver_email = attrs.get('receiver_email')
        receiver_cpf = attrs.get('receiver_cpf')

        if not receiver_email and not receiver_cpf:
            raise serializers.ValidationError(
                "Você deve fornecer um dos seguintes campos: email ou cpf."
            )

        if receiver_email and receiver_cpf:
            raise serializers.ValidationError(
                "Você deve fornecer apenas um dos seguintes campos: email ou cpf."
            )
            

        return attrs

    def validate_value(self, value):
        
        #o campo só pode conter numeros
        if not isinstance(value, (int, float, Decimal)):
            raise serializers.ValidationError("O valor deve ser um número")

        value = Decimal(str(value))

        #validação para que o valor de trandferência não seja menor ou igual a zero
        if value <= 0:
            raise serializers.ValidationError("O valor não pode ser igual ou menor que zero")
        
        return value

    def validate_receiver_cpf(self, value):

        cleaned_cpf = value.replace('.', '').replace('-', '')


        if not cleaned_cpf.isdigit():
            raise serializers.ValidationError("O cpf deve conter apenas números")

        if len(cleaned_cpf) != 11:
            raise serializers.ValidationError("O cpf deve ter 11 numeros")
        return value

        try:
            receiver = CustomUser.objects.get(cpf=cleaned_cpf)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(f"Não foi encontrado um usuário com este CPF")
        return value

    def validate_receiver_email(self, value):

        try:
            receiver = CustomUser.objects.get(email=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(f"Não foi encontrado um usuário com este Email")
        
        return value

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["id", "transfer", "status"]

