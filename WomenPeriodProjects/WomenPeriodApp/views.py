from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import calendar
from datetime import datetime
# Create your views here.

class CalendarioView(APIView):
    def get(self, request, *args, **kwargs):
        nombre_dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        year = 2025
        month = 12

        last_day = calendar.monthrange(year, month)[1]
        dia=1
        calendario = {nombre: [] for nombre in nombre_dias}

        prev_month = month - 1 if month > 1 else 12
        prev_year = year if month > 1 else year - 1
        prev_last_day = calendar.monthrange(prev_year, prev_month)[1]

        next_month = month + 1 if month < 12 else 1
        next_year = year if month < 12 else year + 1
        
        
        while dia <= last_day:
            
            fecha = f"{dia}/{month}/{year}"
            
            fecha_obj = datetime.strptime(fecha, "%d/%m/%Y")
            fecha_formateada = fecha_obj.strftime("%d/%m/%Y")
            
                
            dia_semana = fecha_obj.weekday()
            if dia==1:
                
                if dia_semana!=0:
                    inicio=(prev_last_day - dia_semana) + 1
                    
                    while inicio <= prev_last_day:
                        fecha_ant = f"{inicio}/{prev_month}/{prev_year}"
                        
                        fecha_obj_ant = datetime.strptime(fecha_ant, "%d/%m/%Y")
                        
                        fecha_formateada_ante = fecha_obj_ant.strftime("%d/%m/%Y")
                        dia_semana_ant = fecha_obj_ant.weekday()
                        nombre_dia_ant = nombre_dias[dia_semana_ant]
                        calendario[nombre_dia_ant].append(fecha_formateada_ante)
                        
                        inicio += 1
            
            
            nombre_dia = nombre_dias[dia_semana]
            calendario[nombre_dia].append(fecha_formateada) 
            if dia==last_day:
                cant_day_add=6
                if dia_semana !=0:
                    cant_day_add=cant_day_add + (7 - dia_semana)
                
                fin_inicio=1
                
                # print(f'la cantidad de dias agregados fue de {cant_day_add}')
                while fin_inicio <=cant_day_add:
                    fecha_post = f"{str(fin_inicio)}/{str(next_month)}/{str(next_year)}"
                    fecha_obj_post = datetime.strptime(fecha_post, "%d/%m/%Y")
                    fecha_formateada_post = fecha_obj_post.strftime("%d/%m/%Y")
                    dia_semana_post = fecha_obj_post.weekday()
                    nombre_dia_post = nombre_dias[dia_semana_post]
                    calendario[nombre_dia_post].append(fecha_formateada_post)
                    fin_inicio += 1
                    
            dia += 1  # Incrementa el día
            
            
        return Response(calendario, status=status.HTTP_200_OK)
    

class GenerarCalendario(APIView):
    def get(self, request, *args, **kwargs):
        nombre_dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        year = 2025
        month = 2

        last_day = calendar.monthrange(year, month)[1]
        dia=1
        calendario = {nombre: [] for nombre in nombre_dias}

        prev_month = month - 1 if month > 1 else 12
        prev_year = year if month > 1 else year - 1
        prev_last_day = calendar.monthrange(prev_year, prev_month)[1]

        next_month = month + 1 if month < 12 else 1
        next_year = year if month < 12 else year + 1
        
        dia_ins=0
        corresponde_mes=False
        fecha_value=''
        orden=1
        calendario_ins=[]
        while dia <= last_day:
            
            fecha = f"{dia}/{month}/{year}"
            
            fecha_obj = datetime.strptime(fecha, "%d/%m/%Y")
            fecha_formateada = fecha_obj.strftime("%d/%m/%Y")
            
                
            dia_semana = fecha_obj.weekday()
            # if dia==1:
                
            #     if dia_semana!=0:
            #         inicio=(prev_last_day - dia_semana) + 1
                    
            #         while inicio <= prev_last_day:
            #             fecha_ant = f"{inicio}/{prev_month}/{prev_year}"
            #             fecha_obj_ant = datetime.strptime(fecha_ant, "%d/%m/%Y")
            #             fecha_formateada_ante = fecha_obj_ant.strftime("%d/%m/%Y")
            #             dia_semana_ant = fecha_obj_ant.weekday()
                        
            #             numero_mes = fecha_obj_ant.month
            #             result_ins={
            #                 'dia':inicio,
            #                 'Mes':numero_mes,
            #                 'dia de la semana':dia_semana_ant,
            #                 'valor':fecha_obj_ant,
            #                 'Pertenece_Mes':numero_mes==month,
            #                 'Orden':orden
            #             }
            #             calendario_ins.append(result_ins)
            #             orden +=1
            #             inicio += 1
            
            
            numero_mes = fecha_obj.month
            result_ins={
                            'dia':dia,
                            'Mes':numero_mes,
                            'dia de la semana':dia_semana,
                            'valor':fecha_obj,
                            'Pertenece_Mes':numero_mes==month,
                            'Orden':orden
                        }
            calendario_ins.append(result_ins)

            # if dia==last_day:
            #     cant_day_add=6
            #     if dia_semana !=0:
            #         cant_day_add=cant_day_add + (7 - dia_semana)
                
            #     fin_inicio=1
            #     orden +=1
            #     # print(f'la cantidad de dias agregados fue de {cant_day_add}')
            #     while fin_inicio <=cant_day_add:
            #         fecha_post = f"{str(fin_inicio)}/{str(next_month)}/{str(next_year)}"
            #         fecha_obj_post = datetime.strptime(fecha_post, "%d/%m/%Y")
            #         numero_mes = fecha_obj_post.month
            #         dia_semana_post = fecha_obj_post.weekday()
                    
            #         result_ins={
            #                 'dia':fin_inicio,
            #                 'Mes':numero_mes,
            #                 'dia de la semana':dia_semana_post,
            #                 'valor':fecha_obj_post,
            #                 'Pertenece_Mes':numero_mes==month,
            #                 'Orden':orden
            #             }
            #         calendario_ins.append(result_ins)
            #         fin_inicio += 1
            #         orden +=1
            dia += 1  # Incrementa el día
            orden +=1
            
        return Response(calendario_ins, status=status.HTTP_200_OK)
    
