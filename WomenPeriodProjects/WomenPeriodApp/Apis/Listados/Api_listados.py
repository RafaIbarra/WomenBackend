from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from WomenPeriodApp.models import Calendario,Meses,CalendarioDias,MarcasUsuario,Versiones,DiasPreviosAvisoPeriodo
from WomenPeriodApp.Serializadores.CalendarioSerializers import CalendarioSerializers,CalendarioDisplaySerializers,CalendarioUserSerializer
from WomenPeriodApp.Serializadores.CalendarioDiasSerializers import CalendarioDiasSerializersNormal
from WomenPeriodApp.Serializadores.MarcasUsuarioSerializers import MarcasUsuarioSerializers
from WomenPeriodApp.Serializadores.VersionesSerializers import VersionesSerializers
from WomenPeriodApp.Serializadores.DiasPreviosAvisoPeriodoSerializers import DiasPreviosAvisoPeriodoSerializer
from django.db.models import Q, Subquery, OuterRef
from WomenPeriodApp.Apis.Seguridad.Validaciones import *
from WomenPeriodApp.Apis.Seguridad.obtener_datos_token import *
import pandas as pd

@api_view(['POST'])
def DatosCalendario(request):
    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    
    if resp==True:
        try:
            year=int(request.data['year'])
            month=int(request.data['month'])
            # condicion_marca_usuario=Q(user_id__exact=id_user)
            # data_marcas=MarcasUsuario.objects.filter(condicion_marca_usuario).values()
            # condicion_marca_usuario = Q(user_id__exact=id_user) & Q(DesdeDia__Calendario__AnnoCalendario=year)
            condicion_marca_usuario = Q(user_id=id_user) & (
                Q(DesdeDia__Calendario__AnnoCalendario=year) | 
                Q(HastaDia__Calendario__AnnoCalendario=year)
            )
            data_marcas_ser = list(MarcasUsuario.objects.filter(condicion_marca_usuario).values("DesdeDia_id", "HastaDia_id", "Intensidad_id", "TipoMarca_id"))
            
            
            if month >0:
                condicion_mes=Q(NumeroMes__exact=month)
                data_mes=Meses.objects.filter(condicion_mes).values()
                id_mes=data_mes[0]['id']
                condicion1=Q(Calendario__AnnoCalendario=year)
                condicion2=Q(Calendario__Mes_id=id_mes)
            
                condicion1=Q(AnnoCalendario__exact=year)
                condicion2=Q(Mes_id__exact=id_mes)
                data_calendario = Calendario.objects.select_related("Mes").prefetch_related("calendariodias_set__DiaSemana").filter(condicion1 & condicion2)
                
                

            else:
                # condicion1=Q(AnnoCalendario__exact=year)
                condicion1 = Q(AnnoCalendario=year) | Q(AnnoCalendario=year + 1, Mes__NumeroMes=1)
                data_calendario = Calendario.objects.select_related("Mes").prefetch_related("calendariodias_set__DiaSemana").filter(condicion1)
                

            
            
            serializer = CalendarioUserSerializer(data_calendario, many=True, context={"marcas": data_marcas_ser})
            id_marcas=[]
            for m in data_marcas_ser:
                inicio=m['DesdeDia_id']
                fin=m['HastaDia_id']
                c=inicio
                while c <=fin:
                    
                    id_marcas.append(c)
                    c=c +1
                    
                
                

            
            
            return Response([ {'calendario':serializer.data,
                               'Marcas':id_marcas
                               }
                 
                 ],status= status.HTTP_200_OK)
  
        except Exception as e:
            
            return Response(
                {'error': f'Ocurrió un error inesperado: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    else:
        return Response(resp,status= status.HTTP_403_FORBIDDEN)
    
@api_view(['POST'])
def ConsultaMarcaRegistrada(request):
    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    
    if resp==True:
        try:
            id_dia=int(request.data['id_dia'])
            
            marcas_usuario = MarcasUsuario.objects.filter(Q(DesdeDia__id__lte=id_dia) & Q(HastaDia__id__gte=id_dia),user_id=id_user)
            
            
            # Subconsulta para obtener los días dentro del rango
            dias_en_rango = CalendarioDias.objects.filter(
                Q(id__gte=Subquery(marcas_usuario.values('DesdeDia_id')[:1])) &
                Q(id__lte=Subquery(marcas_usuario.values('HastaDia_id')[:1]))
            ).values(
                "id",
                "ValorFecha",
                "DiaValorFecha",
                "MesValorFecha",
                "AnnoValorFecha",
                "PerteneceMes",
                "Orden"
            ).distinct().order_by("id")

            # Convertir fechas al formato dd/mm/aaaa
            resultado = [
                {
                    "id": dia["id"],
                    "ValorFecha": dia["ValorFecha"].strftime("%d/%m/%Y"),
                    "DiaValorFecha": dia["DiaValorFecha"],
                    "MesValorFecha": dia["MesValorFecha"],
                    "AnnoValorFecha": dia["AnnoValorFecha"],
                    "PerteneceMes": dia["PerteneceMes"],
                    "Orden": dia["Orden"]
                }
                for dia in dias_en_rango
            ]
            marcas_serializers=MarcasUsuarioSerializers(marcas_usuario,many=True)
            if marcas_serializers.data:
                
                return Response([
                    {'detalle':resultado,
                     'valores':marcas_serializers.data
                     }],status= status.HTTP_200_OK)
            else:
                return Response({'error':marcas_serializers.errors},status= status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response(
                {'error': f'Ocurrió un error inesperado: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    else:
        return Response(resp,status= status.HTTP_403_FORBIDDEN)
@api_view(['POST'])
def ObtenerDiasPrevios(request):
    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    
    if resp==True:
        try:
            dias_usuario = DiasPreviosAvisoPeriodo.objects.filter(user_id=id_user)
            dias_serializers=DiasPreviosAvisoPeriodoSerializer(dias_usuario,many=True)
            if dias_serializers.data:
                
                return Response(dias_serializers.data,status= status.HTTP_200_OK)
            else:
                return Response([],status= status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': f'Ocurrió un error inesperado: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    else:
        return Response(resp,status= status.HTTP_403_FORBIDDEN)
    
@api_view(['POST'])
def DatosCalendarioMesSiguiente(request):
    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    
    if resp==True:
        try:
            id_dia=int(request.data['id_dia'])
            
            condicion1=Q(id__exact=id_dia)
            data=CalendarioDias.objects.filter(condicion1).values()
            
            if data:
                calendario_id=data[0]['Calendario_id']
                calendario_id_sg=calendario_id + 1
                condicion1=Q( Calendario_id__gt=calendario_id)
                condicion2=Q( Calendario_id__lt=calendario_id_sg)
                
                data_siguiente = CalendarioDias.objects.filter(
                     Calendario_id__gte=calendario_id,  # Mayor o igual que valor_inicial
                    Calendario_id__lte=calendario_id_sg
                     )
                
                if data_siguiente:
                
                    result_serializer=CalendarioDiasSerializersNormal(data_siguiente,many=True)
                    if result_serializer.data:
                        
                        return Response(result_serializer.data,status= status.HTTP_200_OK)

                    return Response({'message':result_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
                
                return Response([],status= status.HTTP_200_OK)
              
                
            else:
                return Response([],status= status.HTTP_200_OK)
        except Exception as e:
                return Response(
                    {'error': f'Ocurrió un error inesperado: {str(e)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
    else:
        return Response(resp,status= status.HTTP_403_FORBIDDEN)
    

@api_view(['POST'])
def AnnosDisponibles(request):
    token_sesion,usuario,id_user =obtener_datos_token(request)
    resp=validacionpeticion(token_sesion)
    
    if resp==True:
        try:
            
            data=Calendario.objects.all().values()
            
            df_data=pd.DataFrame(data)
            
            años_ordenados = sorted(df_data['AnnoCalendario'].unique().tolist())[:-1]
           
            
            
            if data:
               data_anno={
                   "Desde":años_ordenados[0],
                   "Hasta":años_ordenados[-1],
               }
               return Response(data_anno,status= status.HTTP_200_OK)
              
                
            else:
                return Response([],status= status.HTTP_200_OK)
        except Exception as e:
                return Response(
                    {'error': f'Ocurrió un error inesperado: {str(e)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
    else:
        return Response(resp,status= status.HTTP_403_FORBIDDEN)
    
@api_view(['POST'])
def DatosSistema(request):

     token_sesion,usuario,id_user =obtener_datos_token(request)
     resp=validacionpeticion(token_sesion)
     
     if resp==True:           
        consulta_version=Versiones.objects.filter(estado__exact=1).values()
        

                
        if consulta_version:
            result_serializer=VersionesSerializers(consulta_version,many=True)
            

            if result_serializer.data:
                return Response(result_serializer.data,status= status.HTTP_200_OK)

            return Response({'message':result_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
                
        else:
            return Response([],status= status.HTTP_200_OK)
     else:
             return Response(resp,status= status.HTTP_403_FORBIDDEN)