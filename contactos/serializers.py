from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from .models import Contacto
from .validators import normalize_email, normalize_telefono

class ContactoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacto
        fields = '__all__'

    def validate_email(self, value):
        try:
            email = normalize_email(value)
        except DjangoValidationError as error:
            raise serializers.ValidationError(error.messages) from error

        query = Contacto.objects.filter(email__iexact=email)
        if self.instance:
            query = query.exclude(pk=self.instance.pk)
        if query.exists():
            raise serializers.ValidationError(
                'Este correo electrónico ya se encuentra registrado.'
            )
        return email

    def validate_telefono(self, value):
        try:
            return normalize_telefono(value)
        except DjangoValidationError as error:
            raise serializers.ValidationError(error.messages) from error