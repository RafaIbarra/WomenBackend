from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from datetime import datetime
from WomenPeriodApp.models import Calendario,Meses,CalendarioDias,DiasSemana,NivelIntensidad,TipoMarca
from WomenPeriodApp.Serializadores.MesesSerializers import MesesSerializers
from WomenPeriodApp.Serializadores.DiasSemanaSerializers import DiasSemanaSerializers
from WomenPeriodApp.Serializadores.CalendarioSerializers import CalendarioSerializers
from WomenPeriodApp.Serializadores.CalendarioDiasSerializers import CalendarioDiasSerializers
from WomenPeriodApp.Serializadores.NivelIntensidadSerializers import NivelIntensidadSerializers
from WomenPeriodApp.Serializadores.TipoMarcaSerializers import TipoMarcaSerializers
import calendar
from django.db.models import Q
class GenerarMeses(APIView):
    def get(self, request, *args, **kwargs):
        data_list = []
        data_errores=''
        n=1
        while n < 13:
            if n==1: nombremes='Enero'
            if n==2: nombremes='Febrero'
            if n==3: nombremes='Marzo'
            if n==4: nombremes='Abril'
            if n==5: nombremes='Mayo'
            if n==6: nombremes='Junio'
            if n==7: nombremes= 'Julio'
            if n==8: nombremes='Agosto'
            if n==9: nombremes='Septiembre'
            if n==10: nombremes='Octubre'
            if n==11: nombremes='Noviembre'
            if n==12: nombremes='Diciembre'

            datasave={
                "id":  0,
                "NumeroMes": n,
                "NombreMes":nombremes,
                "FechaRegistro": datetime.now()
                
            }
            data_list.append(datasave)
            
            meses_serializer=MesesSerializers(data=datasave)
            n=n+1
            if meses_serializer.is_valid():
                meses_serializer.save()
                
            else:
                print(meses_serializer.errors)
            
        return Response([],status= status.HTTP_200_OK)
            
class GenerarDias(APIView):
    def get(self, request, *args, **kwargs):
        data_list = []
        nombre_dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        data_errores=''
        n=0
        while n < 7:
            if n==0: nombredia='Lunes'
            if n==1: nombredia='Martes'
            if n==2: nombredia='Miercoles'
            if n==3: nombredia='Jueves'
            if n==4: nombredia='Viernes'
            if n==5: nombredia='Sabado'
            if n==6: nombredia= 'Domingo'
            abreviatura = nombredia[:2].upper()

            datasave={
                "id":  0,
                "NumeroDia": n,
                "NombreDia":nombredia,
                "Abreviatura":abreviatura,
                "FechaRegistro": datetime.now()
                
            }
            data_list.append(datasave)
            
            dias_serializer=DiasSemanaSerializers(data=datasave)
            n +=1
            if dias_serializer.is_valid():
                dias_serializer.save()
                
            else:
                return Response({'error':dias_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
            
        return Response({'dias Generados'},status= status.HTTP_200_OK)
    
@api_view(['POST'])
def ProcesarCalendario(request):
    year=int(request.data['year'])

    month = 1
    while month <=12:
        
        last_day = calendar.monthrange(year, month)[1]
        ultima_fecha = f"{last_day}/{month}/{year}"
        last_date= datetime.strptime(ultima_fecha, "%d/%m/%Y").date()
        dia_inicio=1
        primer_fecha = f"{dia_inicio}/{month}/{year}"
        firts_date= datetime.strptime(primer_fecha, "%d/%m/%Y").date() 
        
        condicion_mes = Q(NumeroMes__exact=month)
        data_mes=Meses.objects.filter(condicion_mes).values()
        id_mes=data_mes[0]['id']

        condicion1=Q(AnnoCalendario__exact=year)
        condicion2=Q(Mes_id__exact=id_mes)
        data_calendario=Calendario.objects.filter(condicion1 & condicion2).values()
        id_calendario=0
        if data_calendario:
            id_calendario=data_calendario[0]['id']
        else:
            data_list = []
            datasave={
                "id":  0,
                "Mes": id_mes,
                "AnnoCalendario":year,
                "FechaInicio":firts_date,
                "FechaFin":last_date,
                "FechaRegistro": datetime.now()
                
            }
            data_list.append(datasave)
            
            calendario_serializer=CalendarioSerializers(data=datasave)
            
            if calendario_serializer.is_valid():
                instancia = calendario_serializer.save()
                id_calendario = instancia.id
                
            else:
                return Response({'error':calendario_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
            
        if id_calendario >0:
            
            dia=1
            orden=1

            prev_month = month - 1 if month > 1 else 12
            prev_year = year if month > 1 else year - 1
            prev_last_day = calendar.monthrange(prev_year, prev_month)[1]

            next_month = month + 1 if month < 12 else 1
            next_year = year if month < 12 else year + 1
            # print( f"el mes anterior es {prev_last_day}/{prev_month}/{prev_year} ")
            # print( f"el mes siguiente es 01/{next_month}/{next_year} ")
            while dia <= last_day:
                fecha = f"{dia}/{month}/{year}"
                fecha_obj = datetime.strptime(fecha, "%d/%m/%Y")
                
                dia_semana=fecha_obj.weekday()
                # if dia==1:
                #     if dia_semana!=0:
                #         inicio=(prev_last_day - dia_semana) + 1
                #         while inicio <= prev_last_day:
                #             fecha_ant = f"{inicio}/{prev_month}/{prev_year}"
                #             fecha_obj_ant = datetime.strptime(fecha_ant, "%d/%m/%Y")
                #             date_value_reg=fecha_obj_ant.date()
                #             dia_semana_ant = fecha_obj_ant.weekday()
                #             id_dia = retornar_id_dia(dia_semana_ant)
                #             numero_mes = fecha_obj_ant.month
                #             debe_registrar=control_existencia(id_calendario,inicio,numero_mes)
                #             if debe_registrar:
                #                 result_reg=registro_calendario_dia(id_calendario,month,id_dia,inicio,numero_mes,date_value_reg,orden)
                                
                #             orden +=1
                #             inicio += 1

                


                
                debe_registrar=control_existencia(id_calendario,dia,month)
                
                if debe_registrar:
                    
                    id_dia = retornar_id_dia(dia_semana)
                    date_value_reg=fecha_obj.date()
                    result_reg=registro_calendario_dia(id_calendario,month,id_dia,dia,month,date_value_reg,orden)
                    
                
                # if dia==last_day:
                #     cant_day_add=6
                #     if dia_semana !=0:
                #         cant_day_add=cant_day_add + (7 - dia_semana)
                    
                #     fin_inicio=1
                #     orden +=1
                #     while fin_inicio <=cant_day_add:
                #         fecha_post = f"{str(fin_inicio)}/{str(next_month)}/{str(next_year)}"
                #         fecha_obj_post = datetime.strptime(fecha_post, "%d/%m/%Y")
                #         numero_mes = fecha_obj_post.month
                #         dia_semana_post = fecha_obj_post.weekday()
                #         id_dia = retornar_id_dia(dia_semana_post)
                #         debe_registrar=control_existencia(id_calendario,fin_inicio,numero_mes)
                #         date_value_reg=fecha_obj_post.date()
                #         if debe_registrar:
                #             result_reg=registro_calendario_dia(id_calendario,month,id_dia,fin_inicio,numero_mes,date_value_reg,orden)
                            
                #         fin_inicio += 1
                #         orden +=1

                dia += 1  # Incrementa el día
                orden +=1


            # n +=1
        month +=1
    
    return Response('calendario_ins', status=status.HTTP_200_OK)

class CargaReferenciales(APIView):
    def get(self, request, *args, **kwargs):
        data_list = []
        
        # id= models.AutoField(primary_key=True, serialize=False)
        # NombreIntensidad=models.CharField(max_length=100,blank=False)
        # NumeroNivel=models.IntegerField()
        # FechaRegistro=models.DateTimeField("fecha registro")
        c=1
        while c <4:
            nivel=""
            if c==1:
                nivel="Elevado"
            if c==2:
                nivel="Medio"
            if c==3:
                nivel="Bajo"
            datasave={
                "id":  0,
                "NombreIntensidad": nivel,
                "NumeroNivel":c,
                "FechaRegistro": datetime.now()
                
            }
            data_list.append(datasave)
            
            dias_serializer=NivelIntensidadSerializers(data=datasave)
            c +=1
            if dias_serializer.is_valid():
                dias_serializer.save()
                
            else:
                return Response({'error':dias_serializer.errors},status= status.HTTP_400_BAD_REQUEST)
        i=1
        while i<3:
            if i==1:
                marca="Roja"
            if i==2:
                marca="Marron"
            datasave={
                "id":  0,
                "NombreTipoMarca": marca,
                "FechaRegistro": datetime.now()
                
            }
            data_list.append(datasave)
            
            dias_serializer=TipoMarcaSerializers(data=datasave)
            i +=1
            if dias_serializer.is_valid():
                dias_serializer.save()
                
            else:
                return Response({'error':dias_serializer.errors},status= status.HTTP_400_BAD_REQUEST)


            
        return Response({'dias Generados'},status= status.HTTP_200_OK)


def control_existencia(id_calen,dia,numeromes):
    condicion1=Q(Calendario_id__exact=id_calen)
    condicion2=Q(DiaValorFecha__exact=dia)
    condicion3=Q(MesValorFecha__exact=numeromes)
    data_calendario_dia=CalendarioDias.objects.filter(condicion1 & condicion2 & condicion3).values()
    if data_calendario_dia:
        return False
    else:
        return True
    
def retornar_id_dia(numerodia):
    condicion1=Q(NumeroDia__exact=numerodia)
    data_dia=DiasSemana.objects.filter(condicion1).values()
    
    id_dia=data_dia[0]['id']
    return id_dia


def registro_calendario_dia(id_calen,mesproceso,id_dia,numerodia,numeromes,value_date,orden):
    data_list = []
    datasave={
        "id":  0,
        "Calendario": id_calen,
        "DiaSemana":id_dia,
        "ValorFecha": value_date,
        "DiaValorFecha":numerodia,
        "MesValorFecha":value_date.month,
        "AnnoValorFecha":value_date.year,
        "PerteneceMes":mesproceso==numeromes,
        "Orden":orden,
        "FechaRegistro":datetime.now()
        
    }
    data_list.append(datasave)
    
    calendario_dia_serializer=CalendarioDiasSerializers(data=datasave)
    
    if calendario_dia_serializer.is_valid():
        calendario_dia_serializer.save()
        return True
        
    else:
        
        return False