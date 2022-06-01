from rest_framework.pagination import PageNumberPagination

class EdificacionPagination(PageNumberPagination):

    #NÚMERO DE PÁGINAS EN LAS QUE SE VAN A DISTRUBUIR TODOS LOS REGISTROS
    #page_size=2 

    #PARÁMETRO PARA DETERMINAR EL NÚMERO DE REGISTROS PARA MOSTRAR POR PÁGINA
    page_size_query_param ='size' #http://127.0.0.1:8000/tienda/edificacion/list/?size=1