from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.views import TokenObtainPairView
from WomenPeriodApp.Serializadores.CustomsSerializers import *
from WomenPeriodApp.models import MarcasUsuario,DiasPreviosAvisoPeriodo,Usuarios

from django.db import models
from datetime import date, timedelta
from django.db.models.functions import Coalesce
from django.db.models import Q, Subquery, OuterRef,Value, ExpressionWrapper, F, DurationField
from django.db.models import DateField
from dateutil.relativedelta import relativedelta
import requests
class EnvioNotificacionesDiasPrevios(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    def get(self, request, *args, **kwargs):
        hoy=date.today()
        
        mes=hoy.month
        anno=hoy.year
        mes_anterior=mes - 1

        subquery_dias_previos = DiasPreviosAvisoPeriodo.objects.filter(
            user_id=OuterRef('user_id')
        ).values('CantidadDias')[:1]  # solo uno por usuario
        condicion_marca_usuario = Q(
                Q(DesdeDia__AnnoValorFecha=anno) 
                &
                Q(DesdeDia__MesValorFecha=mes_anterior)
            )
        marcas_usuario = MarcasUsuario.objects.filter(condicion_marca_usuario).annotate(
                            cantidad_dias=Coalesce(Subquery(subquery_dias_previos), Value(0)),
                            fecha_aviso=ExpressionWrapper(
                                F('DesdeDia__ValorFecha') - F('cantidad_dias') * Value(timedelta(days=1)),
                                output_field=models.DateField()
                            )
                    ).values(
            'user_id','DesdeDia__ValorFecha','user__user_name','user__push_token', 'cantidad_dias','fecha_aviso'
            )
        for item in marcas_usuario:
            fecha_marca = item["DesdeDia__ValorFecha"]
            fecha_aviso = item["fecha_aviso"]

            
            user_id= item["user_id"]
            # fecha_marca= fecha_marca.isoformat() if fecha_marca else None
            fecha_marca = fecha_marca.strftime("%d/%m/%Y") if fecha_marca else None
            user_name= item["user__user_name"]
            push_token= item["user__push_token"]
            cantidad_dias= item["cantidad_dias"]
            fecha_aviso= (fecha_aviso + relativedelta(months=1)).date().isoformat() if fecha_aviso else None
            
            if date.fromisoformat(fecha_aviso)==hoy:
                msg_dia='dias' if cantidad_dias >1 else 'dia'
                
                message = {
                'to': push_token,
                'sound': 'default',
                'title': (f'¡Hola {user_name}!'),
                'body': (f'Te recordamos que faltan {cantidad_dias} {msg_dia} para un nuevo registro desde que marcaste como inicio el dia {fecha_marca}'),
                }
                try:
                    response = requests.post('https://exp.host/--/api/v2/push/send', json=message)
                    response.raise_for_status()
                    
                except requests.exceptions.RequestException as e:
                    print(f'Error al enviar notificación a {push_token}: {e}')

            
            
        return Response([],status= status.HTTP_200_OK)
    
class EnvioNotificacionPrueba(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    def get(self, request, *args, **kwargs):
        
        
        data_usuarios=Usuarios.objects.all().values()
        if data_usuarios:
            token=data_usuarios[0]['push_token']
            usuario=data_usuarios[0]['user_name']
            print(token)
            # message = {
            #     'to': token,
            #     'sound': 'default',
            #     'title': (f'¡Hola {usuario}!'),
            #     'body': 'Perdón! Esta es solo una notificacion de prueba',
            # }
            # try:
            #     response = requests.post('https://exp.host/--/api/v2/push/send', json=message)
            #     response.raise_for_status()
            #     print('se envio sin errores')
            # except requests.exceptions.RequestException as e:
            #     print(f'Error al enviar notificación a {token}: {e}')
            try:
    # Verificar token primero
                
                
                response = requests.post(
                    'https://exp.host/--/api/v2/push/send',
                    json={
                        'to': token,
                        'title': f'¡Hola {usuario}!',
                        'body': 'Notificación de prueba',
                        'sound': 'default',
                        'channelId': 'default',  # Importante para Android 8+
                        'priority': 'high',     # Prioridad alta para Android
                        'ttl': 60,             # Tiempo de vida en segundos
                    },
                    timeout=15
                )
                
                response_data = response.json()
                print(f"Respuesta del servidor: {response_data}")
                
                if response_data.get('data', {}).get('status') == 'ok':
                    print("Notificación aceptada por el servidor de Expo")
                else:
                    print(f"Posible problema: {response_data}")
                
            except Exception as e:
                print(f"Error completo: {str(e)}")
                if hasattr(e, 'response') and e.response:
                    print(f"Contenido de error: {e.response.text}")
        
        return Response({'vacio'},status= status.HTTP_200_OK)