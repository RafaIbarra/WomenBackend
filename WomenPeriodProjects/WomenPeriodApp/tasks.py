# women_period_app/tasks.py
from celery import shared_task
import requests

@shared_task(bind=True, max_retries=3)
def enviar_notificaciones_dias_previos(self):
    url = "https://wom.rafaelibarra.xyz/api/EnvioNotificacionesDiasPrevios/"
    
    try:
        response = requests.get(  # Cambiado a GET
            url,
            timeout=10  # Timeout de 10 segundos
        )
        response.raise_for_status()  # Lanza error si status != 200
        
        return {
            'status_code': response.status_code,
            'response': response.text  # Usamos .text en lugar de .json() por si la respuesta no es JSON
        }
        
    except requests.exceptions.RequestException as e:
        self.retry(exc=e, countdown=60)  # Reintenta después de 60 segundos
        return {'error': str(e)}