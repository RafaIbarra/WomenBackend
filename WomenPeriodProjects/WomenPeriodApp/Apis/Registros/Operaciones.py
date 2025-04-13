from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status  

from django.db.models import Q
from WomenPeriodApp.Apis.Seguridad.Validaciones import *
from WomenPeriodApp.Apis.Seguridad.obtener_datos_token import *
from WomenPeriodApp.models import MarcasUsuario,DiasPreviosAvisoPeriodo
from WomenPeriodApp.Serializadores.MarcasUsuarioSerializers import MarcasUsuarioSerializers
from WomenPeriodApp.Serializadores.DiasPreviosAvisoPeriodoSerializers import DiasPreviosAvisoPeriodoSerializer
import time
@api_view(['POST'])
def RegistroMarcaUsuario(request):

    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    
    if resp==True:
        try:
                
            
            id=int(request.data['codmarca'])

            if id>0:
                
                marcas_usuario = MarcasUsuario.objects.filter(Q(id__exact=id),user_id=id_user).values()
                
                id_reg=marcas_usuario[0]['id']
            else:
                id_reg=0
            id_reg=id
            intensidad=request.data['intensidad']
            tipomarca=request.data['tipomarca']
            desde=request.data['desde']
            hasta=request.data['hasta']
            Observacion=request.data['observacion']
            datasave={
                "id":id_reg,
                "user": id_user,
                "Intensidad":  intensidad,
                "TipoMarca": tipomarca ,
                "DesdeDia": desde,
                "HastaDia": hasta,
                "Observacion": Observacion,
                "FechaRegistro": datetime.now()
            
            }
            
            data_list = []
            data_list.append(datasave)
            if id_reg>0:
                
                condicion1 = Q(id__exact=id_reg)
                dato_existente=MarcasUsuario.objects.filter(condicion1)
                if dato_existente:
                    control_marca_hasta = MarcasUsuario.objects.filter(
                        Q(DesdeDia__id__lte=hasta) & Q(HastaDia__id__gte=hasta) & #entre
                        ~Q(id=id_reg),  # distinto a 
                        user_id=id_user
                    ).values()
                    if control_marca_hasta:
                        return Response({'error':'Ya existe un registro cuyo dia seleccionado como fin coincide con el actual'},status= status.HTTP_400_BAD_REQUEST)

                    existente=MarcasUsuario.objects.get(condicion1)
                    
                    marca_serializer=MarcasUsuarioSerializers(existente,data=datasave)

                else:
                    return Response({'error':'El registro a actualizar no existe'},status= status.HTTP_400_BAD_REQUEST)
            else:
                control_marca_hasta = MarcasUsuario.objects.filter(
                        Q(DesdeDia__id__lte=hasta) & Q(HastaDia__id__gte=hasta) , user_id=id_user
                    ).values()
                control_marca_desde = MarcasUsuario.objects.filter(
                        Q(DesdeDia__id__lte=desde) & Q(HastaDia__id__gte=desde) , user_id=id_user
                    ).values()
                
                if control_marca_hasta:
                        
                        return Response({'error':'Ya existe un registro cuyo dia seleccionado como fin coincide con el actual'},status= status.HTTP_400_BAD_REQUEST)
                
                if control_marca_desde:
                        return Response({'error':'Ya existe un registro cuyo dia seleccionado como inicio coincide con el actual'},status= status.HTTP_400_BAD_REQUEST)
                
                
                marca_serializer=MarcasUsuarioSerializers(data=datasave)

            if marca_serializer.is_valid():
                
                marca_serializer =marca_serializer.save()
                
                #id__gen=marca_serializer.id
                
                return Response({'mensaje':'Marca Usuario Almacenado'},status= status.HTTP_200_OK)
            else:
                return Response({'error':marca_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            
            return Response(
                {'error': f'Ocurrió un error inesperado: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    else:
        return Response(resp,status= status.HTTP_403_FORBIDDEN)
    

@api_view(['POST'])
def EliminarMarcaUsuario(request):

    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    
    if resp==True:
        try:
                
            
            id=int(request.data['codmarca'])
            condicion1 = Q(id__exact=id)
            lista=MarcasUsuario.objects.filter(condicion1).values()
            if lista:
        
                marca_del = MarcasUsuario.objects.get(pk=id)
                marca_del.delete()
                return Response({'message':'Marca Eliminada'},status= status.HTTP_200_OK)
            else:
                return Response({'error':'No hay registros que eliminar'},status= status.HTTP_200_OK)

        except Exception as e:
                
                return Response(
                    {'error': f'Ocurrió un error inesperado: {str(e)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    else:
        return Response(resp,status= status.HTTP_403_FORBIDDEN)


@api_view(['POST'])  
def RegistroDiasPrevio(request):
    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    
    if resp==True:
        try:
            id=int(request.data['codregistro'])
            cantdias=int(request.data['cantdias'])
            if cantdias<1:
                return Response({'error':'La cantidad de dias no puede ser menor a 1 (UNO)'},status= status.HTTP_400_BAD_REQUEST)
            if cantdias>15:
                return Response({'error':'La cantidad de dias no puede ser mayor a 15 (QUINCE)'},status= status.HTTP_400_BAD_REQUEST)
            
            if id>0:
                
                dias_previo_usuario = DiasPreviosAvisoPeriodo.objects.filter(Q(id__exact=id),user_id=id_user).values()
                
                id_reg=dias_previo_usuario[0]['id']
            else:
                id_reg=0
            datasave={
                "id":id_reg,
                "user": id_user,
                "CantidadDias":  cantdias,
                "FechaRegistro": datetime.now()
            
            }
            data_list = []
            data_list.append(datasave)
            if id_reg>0:
                condicion1 = Q(id__exact=id_reg)
                dato_existente=DiasPreviosAvisoPeriodo.objects.filter(condicion1)
                if dato_existente:
                    existente=DiasPreviosAvisoPeriodo.objects.get(condicion1)
                    dias_previo_serializer=DiasPreviosAvisoPeriodoSerializer(existente,data=datasave)
                else:
                    return Response({'error':'El registro a actualizar no existe'},status= status.HTTP_400_BAD_REQUEST)
            else:
                dias_previo_serializer=DiasPreviosAvisoPeriodoSerializer(data=datasave)

            if dias_previo_serializer.is_valid():
                
                dias_previo_serializer =dias_previo_serializer.save()
                
                #id__gen=marca_serializer.id
                
                return Response({'mensaje':'Dia Previo Almacenado'},status= status.HTTP_200_OK)
            else:
                return Response({'error':dias_previo_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
        except Exception as e:
                
                return Response(
                    {'error': f'Ocurrió un error inesperado: {str(e)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    else:
        return Response(resp,status= status.HTTP_403_FORBIDDEN)