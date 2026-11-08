from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import Contacto


class ContactosApiTests(TestCase):
    def setUp(self):
        User.objects.create_user(
            username='api-user',
            password='test-password-123',
        )
        self.client = APIClient()

    def authenticate(self):
        response = self.client.post(
            '/api/token/',
            {'username': 'api-user', 'password': 'test-password-123'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {response.data['access']}"
        )

    def contact_data(self, **overrides):
        return {
            'nombre': 'Ana',
            'apellido': 'Pérez',
            'email': 'ANA@example.com',
            'telefono': '912345678',
            'direccion': 'Santiago',
            **overrides,
        }

    def test_contacts_api_requires_jwt(self):
        response = self.client.get('/api/contactos/')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_issue_and_refresh(self):
        response = self.client.post(
            '/api/token/',
            {'username': 'api-user', 'password': 'test-password-123'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        refresh_response = self.client.post(
            '/api/token/refresh/',
            {'refresh': response.data['refresh']},
            format='json',
        )
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', refresh_response.data)

    def test_authenticated_contact_crud_and_domain_validation(self):
        self.authenticate()

        create_response = self.client.post(
            '/api/contactos/',
            self.contact_data(),
            format='json',
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(create_response.data['email'], 'ana@example.com')
        self.assertEqual(create_response.data['telefono'], '912345678')
        contact_id = create_response.data['id']

        list_response = self.client.get('/api/contactos/')
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_response.data), 1)

        duplicate_response = self.client.post(
            '/api/contactos/',
            self.contact_data(email='ana@example.com'),
            format='json',
        )
        self.assertEqual(
            duplicate_response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        invalid_response = self.client.post(
            '/api/contactos/',
            self.contact_data(email='correo-invalido', telefono='123'),
            format='json',
        )
        self.assertEqual(invalid_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', invalid_response.data)
        self.assertIn('telefono', invalid_response.data)

        update_response = self.client.patch(
            f'/api/contactos/{contact_id}/',
            {'direccion': 'Valparaíso'},
            format='json',
        )
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data['direccion'], 'Valparaíso')

        delete_response = self.client.delete(f'/api/contactos/{contact_id}/')
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Contacto.objects.filter(pk=contact_id).exists())

    def test_web_client_is_available_without_api_authentication(self):
        response = self.client.get('/cliente/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Cliente de la API REST')

    def test_cors_allows_configured_local_client_origin(self):
        response = self.client.options(
            '/api/contactos/',
            HTTP_ORIGIN='http://localhost:5173',
            HTTP_ACCESS_CONTROL_REQUEST_METHOD='GET',
        )

        self.assertEqual(
            response['Access-Control-Allow-Origin'],
            'http://localhost:5173',
        )

    def test_cors_rejects_unconfigured_origin(self):
        response = self.client.options(
            '/api/contactos/',
            HTTP_ORIGIN='https://untrusted.example',
            HTTP_ACCESS_CONTROL_REQUEST_METHOD='GET',
        )

        self.assertNotIn('Access-Control-Allow-Origin', response)
