from rest_framework.decorators import api_view
from rest_framework.response import Response
from user_app.api.serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token
#from user_app import models
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken #CON ESTA LIBRERÍA VAMOS A GENERAR EL TOKEN
from django.contrib import auth


@api_view(['POST',])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(['POST',])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data) #CAPTAMOS LA INFORMACIÓN QUE VIENE DEL CLIENTE Y LA SERIALIZAMOS
        data = {} #INICIALIZAMOS LA VARIABLE "data"
        if serializer.is_valid(): #SI ES VÁLIDA LA INFORMACIÓN QUE MANDA EL CLIENTE
            account = serializer.save() #CREAMOS LA CUENTA
            data['response'] = 'El registro del usuario fue exitoso' #AGREGAMOS UN MENSAJE DE CONFIRMACIÓN
            data['username'] = account.username #GUARDAMOS EN LA VARIABLE "data" EL "username"
            data['email'] = account.email #GUARDAMOS EN LA VARIABLE "data" EL "email"
            data['first_name'] = account.first_name
            data['last_name'] = account.last_name
            data['phone_number'] = account.phone_number

            #token = Token.objects.get(user=account).key
            #data['token'] = token

            refresh = RefreshToken.for_user(account) #CREAMOS EL TOKEN
            data['token'] = { #AGREGAMOS LA INFORMACIÓN DEL TOKEN A LA VARIABLE "data"
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }

        else:
            data = serializer.errors

        return Response(data) #MOSTRAMOS TODO LO QUE GUARDAMOS EN LA VARIABLE "data"


@api_view(['POST'])
def login_view(request):
    data = {}
    if request.method=='POST':
        email = request.data.get('email')
        password = request.data.get('password')
        account = auth.authenticate(email=email, password=password)
        if account is not None:
            data['response']='El Login fue exitoso'
            data['username']=account.username
            data['email']=account.email
            data['first_name']=account.first_name
            data['last_name']=account.last_name
            data['phone_number']=account.phone_number
            refresh = RefreshToken.for_user(account)
            data['token'] = {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
            return Response(data)
        else:
            data['error'] = "Credenciales incorrectas"
            return Response(data, status.HTTP_500_INTERNAL_SERVER_ERROR)