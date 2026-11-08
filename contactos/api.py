from rest_framework import routers, viewsets

from .models import Contacto
from .serializers import ContactoSerializer

class ContactoViewSet(viewsets.ModelViewSet):
    queryset = Contacto.objects.all()
    serializer_class = ContactoSerializer

router = routers.DefaultRouter()
router.register(r'contactos', ContactoViewSet)