import re

import validate_cpf
from rest_framework import serializers

from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "email","cpf", "name", "password", "lojista")
        extra_kwargs = {
            "password": {"write_only": True},
            "lojista": {"required": True} 
        }

    def validate_email(self, value):

        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este e-mail já está registrado.")
        return value
    
    def validate_name(self, value):
        # Verifica se o nome contém apenas letras e espaços
        if not re.match(r'^[A-Za-zÀ-ÿ\s]+$', value):
            raise serializers.ValidationError("O nome deve conter apenas letras e espaços.")
        
        # Verifica se o nome tem mais de 100 caracteres
        if len(value) > 100:
            raise serializers.ValidationError("O nome não pode ter mais de 100 caracteres.")
        
        return value

    def validate_cpf(self, value):
        # Verifica o comprimento do CPF antes de consultar no banco de dados
        
        value = re.sub(r'[^0-9]', '', value)

        if len(value) != 11:
            raise serializers.ValidationError("O CPF deve ter 11 caracteres.")
        
        if not validate_cpf.is_valid(value):
            raise serializers.ValidationError("O CPF inserido é inválido")


        # Verifica se o CPF já está registrado no banco de dados
        if CustomUser.objects.filter(cpf=value).exists():
            raise serializers.ValidationError("Este CPF já está registrado.")
        
        return value

    def validate_lojista(self, value):
       
        if value not in [True, False]:
            raise serializers.ValidationError("Formato incorreto do campo lojista")
        return value 
    


    def validate_password(self, value):
        """
        Valida a senha para garantir complexidade.
        """
        if not value:
            raise serializers.ValidationError("A senha é obrigatória.")

        allowed_characters = r'[A-Za-z0-9!@#$%^*()_+\-=\[\]{};:"\\|,.<>/?`~ ]'
        sanitized_value = ''.join(re.findall(allowed_characters, value))
        if len(sanitized_value) != len(value):
            raise serializers.ValidationError("A senha contém caracteres inválidos (<, >, & não são permitidos).")
        
        if len(sanitized_value) < 8:
            raise serializers.ValidationError("A senha deve ter pelo menos 8 caracteres.")
        if not re.search(r'\d', sanitized_value):
            raise serializers.ValidationError("A senha deve conter pelo menos um número.")
        if not re.search(r'[A-Z]', sanitized_value):
            raise serializers.ValidationError("A senha deve conter pelo menos uma letra maiúscula.")
        if not re.search(r'[\W_]', sanitized_value):
            raise serializers.ValidationError("A senha deve conter pelo menos um caractere especial.")
        return sanitized_value

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user