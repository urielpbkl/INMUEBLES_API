from django.urls import path
from inmuebleslist_app.api.views import EdificacionAV, EdificacionDetalleAV, EmpresaAV, EmpresaDetalleAV, ComentarioList, ComentarioDetail, ComentarioCreate, UsuarioComentario, EdificacionList

urlpatterns = [
    #MUESTRA TODAS LAS EDIFICACIONES
    path('edificacion/', EdificacionAV.as_view(), name='edificacion'),
    #PERMITE HACER BÚSQUEDAS DE LAS EDIFICACIONES
    path('edificacion/list/', EdificacionList.as_view(), name='edificacion-list'),
    #MUESTRA UNA EDIFICACIÓN EN PARTICULAR
    path('edificacion/<int:id>', EdificacionDetalleAV.as_view(), name='edificacion-detail'),

    #MUESTRA TODAS LAS EMPRESAS
    path('empresa/', EmpresaAV.as_view(), name='empresa'),
    #MUESTRA UNA EMPRESA EN PARTICULAR
    path('empresa/<int:id>', EmpresaDetalleAV.as_view(), name='comentario-detail'),

    #CREA UN NUEVO COMENTARIO
    path('edificacion/<int:pk>/comentario-create/', ComentarioCreate.as_view(), name='comentario-create'), 
    #MUESTRA LOS COMENTARIOS DE CADA EMPRESA
    path('edificacion/<int:pk>/comentario/', ComentarioList.as_view(), name='comentario-list'), 
    #MUESTRA UN COMENTARIO EN CONCRETO
    path('edificacion/comentario/<int:pk>', ComentarioDetail.as_view(), name='comentario-detail'), #EN ESTE CASO ES OBLIGATORIO NOMBRARLO "pk", PORQUE SINO NO FUNCIONA
    
    #MOSTRAMOS LOS COMENTARIOS DE CADA USUARIO, http://127.0.0.1:8000/tienda/edificacion/comentarios/?username=sa
    path('edificacion/comentarios/', UsuarioComentario.as_view(), name='usuario-comentario-detail'), 
]
