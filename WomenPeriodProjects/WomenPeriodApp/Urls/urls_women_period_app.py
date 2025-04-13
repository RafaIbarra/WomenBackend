from django.urls import path
from WomenPeriodApp.Apis.Registros.Usuarios import *
from WomenPeriodApp.Apis.Registros.Operaciones import *
from WomenPeriodApp.Apis.Registros.RegistroVersiones import *
from WomenPeriodApp.Apis.Listados.Api_listados import *
from WomenPeriodApp.Apis.Notificaciones.Api_Notificaciones import *
urlpatterns = [
    path('RegistroUsuario/',RegistroUsuario.as_view(),name="RegistroUsuario"), 
    path('Login/',Login.as_view(),name="Login"), 
    path('ComprobarVersion/',ComprobarVersion.as_view(),name="ComprobarVersion"), 
    path('EnvioNotificacion/',EnvioNotificacion.as_view(),name="EnvioNotificacion"),
    path('EnvioNotificacionesDiasPrevios/',EnvioNotificacionesDiasPrevios.as_view(),name="EnvioNotificacionesDiasPrevios"), 
    path('EnvioNotificacionPrueba/',EnvioNotificacionPrueba.as_view(),name="EnvioNotificacionPrueba"), 
    path('RegistroVersion/',RegistroVersion.as_view(),name="RegistroVersion"), 
    path('ComprobarSesionUsuario/',ComprobarSesionUsuario,name="ComprobarSesionUsuario"), 
    path('DatosCalendario/',DatosCalendario,name='DatosCalendario'),

    path('ConsultaMarcaRegistrada/',ConsultaMarcaRegistrada,name='ConsultaMarcaRegistrada'),
    path('ObtenerDiasPrevios/',ObtenerDiasPrevios,name='ObtenerDiasPrevios'),
    
    path('RegistroMarcaUsuario/',RegistroMarcaUsuario,name='RegistroMarcaUsuario'),
    path('RegistroDiasPrevio/',RegistroDiasPrevio,name='RegistroDiasPrevio'),
    path('EliminarMarcaUsuario/',EliminarMarcaUsuario,name='EliminarMarcaUsuario'),
    path('DatosCalendarioMesSiguiente/',DatosCalendarioMesSiguiente,name='DatosCalendarioMesSiguiente'),

    path('AnnosDisponibles/',AnnosDisponibles,name='AnnosDisponibles'),
    path('DatosSistema/',DatosSistema,name='DatosSistema'),
]
