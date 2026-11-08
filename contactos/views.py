from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Contacto
from .forms import ContactoForm

def lista_contactos(request):
    query = request.GET.get('q', '')
    if query:
        contactos_list = Contacto.objects.filter(nombre__icontains=query) | Contacto.objects.filter(email__icontains=query)
    else:
        contactos_list = Contacto.objects.all()

    paginator = Paginator(contactos_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'contactos/lista_contactos.html', {'page_obj': page_obj, 'query': query})

def cliente_api(request):
    return render(request, 'contactos/cliente_api.html')

def crear_contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_contactos')
    else:
        form = ContactoForm()
    
    return render(request, 'contactos/formulario_contacto.html', {
        'form': form,
        'titulo': 'Nuevo Contacto'
    })

def editar_contacto(request, pk):
    contacto = get_object_or_404(Contacto, pk=pk)
    if request.method == 'POST':
        form = ContactoForm(request.POST, instance=contacto)
        if form.is_valid():
            form.save()
            return redirect('lista_contactos')
    else:
        form = ContactoForm(instance=contacto)

    return render(request, 'contactos/formulario_contacto.html', {
        'form': form,
        'titulo': 'Editar Contacto'
    })

def eliminar_contacto(request, pk):
    contacto = get_object_or_404(Contacto, pk=pk)
    if request.method == 'POST':
        contacto.delete()
        messages.success(request, '¡Contacto eliminado exitosamente!')
        return redirect('lista_contactos')
    return render(request, 'contactos/confirmar_eliminacion.html', {'contacto': contacto})