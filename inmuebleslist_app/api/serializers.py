from rest_framework import serializers
from inmuebleslist_app.models import Edificacion, Empresa, Comentario



class ComentarioSerializer(serializers.ModelSerializer):

    comentario_user = serializers.StringRelatedField(read_only=True) #AGREGAMOS EL USUARIO QUE CREÓ CADA COMENTARIO

    class Meta:
        model = Comentario
        exclude = ['edificacion'] #LO EXCLUIMOS PORQUE YA LO ESTAMOS ELIGIENDO A TRAVÉS DE LA "URL"



class EdificacionSerializer(serializers.ModelSerializer):

    comentarios = ComentarioSerializer(many=True, read_only=True) #AGREGAMOS LOS COMENTARIOS A CADA EDIFICACIÓN
    empresa_nombre = serializers.CharField(source='empresa.nombre') #MOSTRAR EL NOMBRE DE LA EMPRESA

    class Meta:
        model = Edificacion
        fields = '__all__'  # MOSTRAMOS TODOS LOS CAMPOS
        # exclude = ['id', 'direccion'] #SI QUISIERAMOS EXCLUIR CAMPOS, PODRÍAMOS HACER ESTO


class EmpresaSerializer(serializers.ModelSerializer):
    # MOSTRAR LISTA DE INMUEBLES QUE TIENE CADA EMPRESA
    # NOS MUESTRA TODOS LOS CAMPOS DE TODOS LOS REGISTROS DE LAS EDIFICACIONES RELACIONADAS CON CADA EMPRESA.
    edificacionList = EdificacionSerializer(many=True, read_only=True)

    # edificacionList =  serializers.StringRelatedField(many=True) #REGRESA LA FUNCION "__str__" QUE ESTÁ EN EL ARCHIVO "models.py", QUE EN ESTE CASO SELECCIONA AL CAMPO "direccion" DE CADA REGISTRO

    class Meta:
        model = Empresa
        fields = '__all__'  # MOSTRAMOS LOS CAMPOS
        # exclude = ['id', 'direccion'] #SI QUISIERAMOS EXCLUIR CAMPOS, PODRÍAMOS HACER ESTO



