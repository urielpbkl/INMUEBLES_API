from django.forms import ValidationError
from rest_framework.response import Response
#from rest_framework.decorators import api_view
from inmuebleslist_app.models import Edificacion, Empresa, Comentario
from inmuebleslist_app.api.serializers import EdificacionSerializer, EmpresaSerializer, ComentarioSerializer
from rest_framework import status, generics, mixins
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
# IMPORTAMOS LAS CLASES QUE DAN PERMISOS
from inmuebleslist_app.api.permissions import IsAdminOrReadOnly, IsComentarioUserOrReadOnly
# "ScopedRateThrottle" PERMITE PRESONALIZAR "throttling"
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from inmuebleslist_app.api.throttling import ComentarioCreateThrottle, ComentarioListThrottle

from django_filters.rest_framework import DjangoFilterBackend  # PARA HACER FILTROS
from rest_framework import filters  # PARA HACER BÚSQUEDAS


from inmuebleslist_app.api.pagination import EdificacionPagination


# class ComentarioList(mixins.ListModelMixin, mixins.CreateModelMixin ,generics.GenericAPIView):
#    queryset = Comentario.objects.all()
#    serializer_class = ComentarioSerializer
#
#    def get(self, request, *args, **kwargs):
#        return self.list(request, *args, **kwargs)
#
#    def post(self, request, *args, **kwargs):
#        return self.create(request, *args, **kwargs)
#
# class ComentarioDetail(mixins.RetrieveModelMixin ,generics.GenericAPIView):
#    queryset = Comentario.objects.all()
#    serializer_class = ComentarioSerializer
#
#    def get(self, request, *args, **kwargs):
#        return self.retrieve(request, *args, **kwargs)


# OBTENER LOS COMENTARIOS DEL USUARIO LOGEADO
class UsuarioComentario(generics.ListAPIView):
    serializer_class = ComentarioSerializer  # TRAEMOS EL SERIALIZER DE COMENTARIOS

    def get_queryset(self):
        username = self.request.query_params.get(
            'username', None)  # DE LA "url" VA A VENIR EL "USER"
        # RETORNAMOS LOS COMENTARIOS HECHOS POR EL USUARIO
        return Comentario.objects.filter(comentario_user__username=username)


class ComentarioCreate(generics.CreateAPIView):

    permission_classes = [IsAuthenticated]  # SOLAMENTE LOS USUARIOS LOGEADOS
    # SOLAMENTE SE VAN A PODER HACER 2 REQUEST POR DÍA
    throttle_classes = [ComentarioCreateThrottle]

    serializer_class = ComentarioSerializer

    def get_queryset(self):
        return Comentario.objects.all()

    # CREAMOS UN COMENTARIO PARA UNA "edificacion" EN ESPECÍFICO
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        inmueble = Edificacion.objects.get(pk=pk)

        # MANDAMOS A TRAER AL USUARIO QUE HACE EL COMENTARIO
        user = self.request.user
        comentario_queryset = Comentario.objects.filter(
            edificacion=inmueble, comentario_user=user)

        if comentario_queryset.exists():  # SI EL USUARIO YA PUSO UN COMENTARIO A ESTA "edificacion"
            raise ValidationError(
                "El usuario ya escribio un comentario para este inmueble")

        if inmueble.number_calificacion == 0:
            inmueble.avg_calificacion = serializer.validated_data['calificacion']
        else:
            inmueble.avg_calificacion = (
                serializer.validated_data['calificacion'] + inmueble.avg_calificacion)/2

        inmueble.number_calificacion = inmueble.number_calificacion + 1
        inmueble.save()

        # GUARDAMOS EL COMENTARIO DE LA "Edificacion"
        serializer.save(edificacion=inmueble, comentario_user=user)


# "ListCreateAPIView" INDICA QUE ES UNA OPERACIÓN DE CONSULTA DE DATOS
class ComentarioList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]


    # SOLAMENTE SE VAN A PODER HACER 8 REQUEST POR DÍA DE ESTA SECCIÓN Y SI SON ANÓNIMOS LOS USUARIOS 5 REQUEST
    throttle_classes = [ComentarioListThrottle, AnonRateThrottle]
    serializer_class = ComentarioSerializer

#--------------------------------FILTROS------------------------------------------------------
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['comentario_user__username', 'active']

    # DEVOLVEMOS LOS COMENTARIOS RELACIONADOS A UNA "edificacion"
    def get_queryset(self):
        # "kwargs" ENTREGA TODAS LAS PROPIEDADES/ATRIBUTOPS QUE DA EL CLIENTE
        pk = self.kwargs['pk']
        return Comentario.objects.filter(edificacion=pk)


# "RetrieveUpdateDestroyAPIView" PERMITE CONSULTAR, EDITAR Y ELIMINAR DATOS
class ComentarioDetail(generics.RetrieveUpdateDestroyAPIView):
    # SOLAMENTE EL DUEÑO DEL COMENTARIO PUEDE EDITARLO, LOS DEMÁS SOLAMENTE PODRÁN VERLO
    permission_classes = [IsComentarioUserOrReadOnly]

    # SOLAMENTE SE VAN A PODER HACER 3 REQUEST POR DÍA
    throttle_classes = [ScopedRateThrottle]
    # TIENE QUE IR JUNTO CON "ScopedRateThrottle"
    throttle_scope = 'comentario-detail'

    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer


class EmpresaAV(APIView):
    # SOLAMENTE LOS USUARIOS ADMINISTRADORES PUEDEN ENTRAR A ESTA SECCIÓN
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        inmuebles = Empresa.objects.all()
        serializer = EmpresaSerializer(
            inmuebles, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = EmpresaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.data)


class EmpresaDetalleAV(APIView):

    def get(self, request, id):
        try:
            empresa = Empresa.objects.get(pk=id)
        except Empresa.DoesNotExist:
            return Response({'Error': 'La empresa no existe'}, status=status.HTTP_404_NOT_FOUND)

        serializer = EmpresaSerializer(empresa, context={'request': request})
        return Response(serializer.data)

    def put(self, request, id):
        try:
            empresa = Empresa.objects.get(pk=id)
        except Empresa.DoesNotExist:
            return Response({'Error': 'La empresa no existe'}, status=status.HTTP_404_NOT_FOUND)

        serializer = EmpresaSerializer(empresa, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            empresa = Empresa.objects.get(pk=id)
        except Empresa.DoesNotExist:
            return Response({'Error': 'La empresa no existe'}, status=status.HTTP_404_NOT_FOUND)

        empresa.delete()
        # CONFIRMAMOS QUE LA OPERACIÓN SE REALIZÓ, PERO NO HAY NADA QUE MOSTRAR
        return Response(status=status.HTTP_204_NO_CONTENT)



class EdificacionList(generics.ListAPIView):
    queryset = Edificacion.objects.all()
    serializer_class = EdificacionSerializer
    
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['direccion', 'empresa__nombre']

    pagination_class = EdificacionPagination



class EdificacionAV(APIView):

    # SOLAMENTE LOS USUARIOS ADMINISTRADORES PUEDEN ENTRAR A ESTA SECCIÓN
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        inmuebles = Edificacion.objects.all()
        serializer = EdificacionSerializer(inmuebles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EdificacionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.data)


class EdificacionDetalleAV(APIView):

    # SOLAMENTE LOS USUARIOS ADMINISTRADORES PUEDEN ENTRAR A ESTA SECCIÓN
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, id):
        try:
            inmueble = Edificacion.objects.get(pk=id)
        except Edificacion.DoesNotExist:
            # SI PONEMOS UN "id" QUE NO EXISTE
            return Response({'Error': 'El Inmueble no existe'}, status=status.HTTP_404_NOT_FOUND)
        serializer = EdificacionSerializer(inmueble)
        return Response(serializer.data)

    def put(self, request, id):
        try:
            inmueble = Edificacion.objects.get(pk=id)
        except Edificacion.DoesNotExist:
            # SI PONEMOS UN "id" QUE NO EXISTE
            return Response({'Error': 'El Inmueble no existe'}, status=status.HTTP_404_NOT_FOUND)
        serializer = EdificacionSerializer(inmueble, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            # SI ENVÍAMOS DATOS QUE NO SON VÁLIDOS
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            inmueble = Edificacion.objects.get(pk=id)
        except Edificacion.DoesNotExist:
            # SI PONEMOS UN "id" QUE NO EXISTE
            return Response({'Error': 'El Inmueble no existe'}, status=status.HTTP_404_NOT_FOUND)
        inmueble.delete()
        # CONFIRMAMOS QUE LA OPERACIÓN SE REALIZÓ, PERO NO HAY NADA QUE MOSTRAR
        return Response(status=status.HTTP_204_NO_CONTENT)
