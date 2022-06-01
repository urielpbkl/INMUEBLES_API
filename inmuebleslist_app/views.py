""" from django.shortcuts import render
from django.http import JsonResponse
from inmuebleslist_app.models import Inmueble

# Create your views here.
def inmueble_list(request):
    inmuebles = Inmueble.objects.all()
    data = {
        'inmuebles': list(inmuebles.values())
    }

    return JsonResponse(data)


#BÚSQUEDA POR ID
def inmueble_detalle(request, id):
    inmueble = Inmueble.objects.get(pk=id)

    data = {
        'direccion': inmueble.direccion,
        'pais': inmueble.pais,
        'imagen': inmueble.imagen,
        'activate': inmueble.activate,
        'descripcion': inmueble.descripcion,
    }

    return JsonResponse(data) """