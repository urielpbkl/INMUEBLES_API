from rest_framework import permissions

class IsAdminOrReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view): #No podemos llamarla diferente a "has_permission"

        if request.method == 'GET': #SI SOLAMENTE QUIERE VER DATOS EL USUARIO SE LO PERMITIMOS
            return True
        else: #PERO SI EL MÉTODO ES PUT, POST O DELETE (EDITAR, AGREGAR O ELIMINAR REGISTROS)
            staff_permission = bool(request.user and request.user.is_staff) #TIENE QUE ESTAR LOGEADO Y SER PARTE DEL "staff"

        return staff_permission

class IsComentarioUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        #COMPRUEBA QUE SI EL MÉTODO ES "GET" SOLAMENTE LO PUEDA "LEER" EL USUARIO ACTUAL, PERO SI ES EL DUEÑO DEL COMENTARIO, LO PUEDA "EDITAR" Y/O "BORRAR"
        if request.method in permissions.SAFE_METHODS: # "SAFE_METHODS" ES IGUAL AL MÉTODO "GET" 
            return True
        else: #SI NO ES EL MÉTODO "GET" Y EL USUARIO QUIERE HACER ALGO MÁS CON EL REGISTRO COMO UN "PUT" O "DELETE", PRIMERO COMPRUEBE QUE EL USUARIO LOGEADO SEA IGUAL AL USUARIO QUE CREÓ EL REGISTRO O EL USUARIO ES UN ADMINISTRADOR
            return obj.comentario_user == request.user or request.user.is_staff
        