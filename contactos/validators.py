import re

from django.core.exceptions import ValidationError


def normalize_email(value):
    email = value.lower().strip()
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValidationError(
            'Ingresa un correo electrónico válido (ejemplo: usuario@dominio.com).'
        )
    return email


def normalize_telefono(value):
    telefono = value.strip().replace(' ', '')
    pattern = r'^(\+?56)?(\d{9})$'
    if not re.match(pattern, telefono):
        raise ValidationError(
            'El teléfono debe tener un formato válido (Ej: +56912345678 o 912345678).'
        )
    return telefono
