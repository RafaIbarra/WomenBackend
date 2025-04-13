from rest_framework import serializers
from WomenPeriodApp.models import Calendario,Meses,CalendarioDias,DiasSemana
from WomenPeriodApp.Serializadores.CalendarioDiasSerializers import CalendarioDiasSerializers
from django.db.models import Q,F
class CalendarioSerializers(serializers.ModelSerializer):
    NombreMes=serializers.SerializerMethodField()
    NumeroMes=serializers.SerializerMethodField()
    DiasMes = serializers.SerializerMethodField()
    DiasAgrupado = serializers.SerializerMethodField()
    class Meta:
        model=Calendario
        fields= [
                "id",
                "Mes",
                "NombreMes",
                "NumeroMes",
                "AnnoCalendario",
                "FechaInicio",
                "FechaFin",
                "FechaRegistro",
                "DiasMes",
                "DiasAgrupado"
                ]
    FechaRegistro = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S')

    def get_NombreMes(self, obj):
        
        codigo = obj.Mes_id
        try:
            empresa_obj = Meses.objects.get(id=codigo)
            return empresa_obj.NombreMes
        except Meses.DoesNotExist:
            return None
    def get_NumeroMes(self, obj):
        
        codigo = obj.Mes_id
        try:
            empresa_obj = Meses.objects.get(id=codigo)
            return empresa_obj.NumeroMes
        except Meses.DoesNotExist:
            return None
        
    def get_DiasMes(self, obj):
        # Filtrar los detalles relacionados con la factura
        detalles_obj = CalendarioDias.objects.filter(Calendario=obj)
        
        # Serializamos los detalles utilizando el serializador de FacturasDetalle
        detalle_serializer = CalendarioDiasSerializers(detalles_obj, many=True)
        
        return detalle_serializer.data  # Retornamos los datos serializados
    
    def get_DiasAgrupado(self, obj):
        detalles_obj = CalendarioDias.objects.filter(Calendario=obj)  # Obtener los datos
        detalle_serializer = CalendarioDiasSerializers(detalles_obj, many=True)  # Serializar los datos
        detalle_data = detalle_serializer.data  # Convertir en lista de diccionarios
        detalle_data_ordenado = sorted(detalle_data, key=lambda x: x["NumeroDia"])
        # Crear un diccionario para agrupar los días por AbreviaturaDia
        dias_agrupados = {}

        for detalle in detalle_data_ordenado:  # Recorrer los datos serializados
            abreviatura = detalle["AbreviaturaDia"]  # Acceder al valor del diccionario

            # Si no existe una entrada para este día, la inicializamos
            if abreviatura not in dias_agrupados:
                dias_agrupados[abreviatura] = []

            # Añadir el detalle al grupo correspondiente
            dias_agrupados[abreviatura].append({
                "id": detalle["id"],
                "NombreDia": detalle["NombreDia"],
                "DiaValorFecha": detalle["DiaValorFecha"],
                "MesValorFecha":detalle["MesValorFecha"],
                "AnnoValorFecha":detalle["AnnoValorFecha"],
                "ValorFecha": detalle["ValorFecha"],
                "PerteneceMes": detalle["PerteneceMes"],
                "Orden": detalle["Orden"],
                
                
            })

        return dias_agrupados
    

class CalendarioDisplaySerializers(serializers.ModelSerializer):
    NombreMes=serializers.SerializerMethodField()
    NumeroMes=serializers.SerializerMethodField()
    DiasAgrupado = serializers.SerializerMethodField()
    
    class Meta:
        model=Calendario
        fields= [
                "id",
                
                "Mes",
                "NombreMes",
                "NumeroMes",
                "AnnoCalendario",
                "FechaInicio",
                "FechaFin",
                "FechaRegistro",
                "DiasAgrupado"
                ]
    FechaRegistro = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S')
    

    def get_NombreMes(self, obj):
        
        codigo = obj.Mes_id
        try:
            empresa_obj = Meses.objects.get(id=codigo)
            return empresa_obj.NombreMes
        except Meses.DoesNotExist:
            return None
    def get_NumeroMes(self, obj):
        
        codigo = obj.Mes_id
        try:
            empresa_obj = Meses.objects.get(id=codigo)
            return empresa_obj.NumeroMes
        except Meses.DoesNotExist:
            return None
    
    
    def get_DiasAgrupado(self, obj):
        detalles_obj = CalendarioDias.objects.filter(Calendario=obj)  # Obtener los datos
        detalle_serializer = CalendarioDiasSerializers(detalles_obj, many=True)  # Serializar los datos
        detalle_data = detalle_serializer.data  # Convertir en lista de diccionarios
        detalle_data_ordenado = sorted(detalle_data, key=lambda x: x["NumeroDia"])
        # Crear un diccionario para agrupar los días por AbreviaturaDia
        dias_agrupados = {}

        for detalle in detalle_data_ordenado:  # Recorrer los datos serializados
            abreviatura = detalle["AbreviaturaDia"]  # Acceder al valor del diccionario

            # Si no existe una entrada para este día, la inicializamos
            if abreviatura not in dias_agrupados:
                dias_agrupados[abreviatura] = []

            # Añadir el detalle al grupo correspondiente
            dias_agrupados[abreviatura].append({
                "id": detalle["id"],
               
                "NombreDia": detalle["NombreDia"],
                "DiaValorFecha": detalle["DiaValorFecha"],
                "MesValorFecha":detalle["MesValorFecha"],
                "AnnoValorFecha":detalle["AnnoValorFecha"],
                "ValorFecha": detalle["ValorFecha"],
                "PerteneceMes": detalle["PerteneceMes"],
                "Orden": detalle["Orden"],
                "Marca":False
                
                
            })

        return dias_agrupados
    
class CalendarioUserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    Mes = serializers.IntegerField(source="Mes.id")
    NombreMes = serializers.CharField(source="Mes.NombreMes")
    NumeroMes = serializers.IntegerField(source="Mes.NumeroMes")
    AnnoCalendario = serializers.IntegerField()
    FechaInicio = serializers.DateField(format="%Y-%m-%d")
    FechaFin = serializers.DateField(format="%Y-%m-%d")
    FechaRegistro = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S")
    DiasAgrupado = serializers.SerializerMethodField()
    

    # def get_DiasAgrupado(self, obj):
    #     # Obtener marcas para optimizar la búsqueda
    #     marcas = { 
    #         (marca["DesdeDia_id"], marca["HastaDia_id"]): {
    #             "Intensidad": marca["Intensidad_id"], 
    #             "TipoMarca": marca["TipoMarca_id"]
    #         }
    #         for marca in self.context["marcas"]
    #     }

    #     # Agrupar los días por la abreviatura (LU, MA, etc.)
    #     dias_agrupados = {}
    #     print( obj.calendariodias_set.all())
    #     for dia in obj.calendariodias_set.all():
    #         abrev = dia.DiaSemana.Abreviatura

    #         # Verificar si el ID del día está en algún rango de marcas
    #         marca_info = {"Marca": False, "Intensidad": 0, "TipoMarca": 0}
    #         for (desde, hasta), valores in marcas.items():
    #             if desde <= dia.id <= hasta:
    #                 marca_info = {"Marca": True, "Intensidad": valores["Intensidad"], "TipoMarca": valores["TipoMarca"]}
    #                 break
            
    #         dia_info = {
    #             "id": dia.id,
    #             "NombreDia": dia.DiaSemana.NombreDia,
    #             "DiaValorFecha": dia.ValorFecha.day,
    #             "MesValorFecha": dia.ValorFecha.month,
    #             "AnnoValorFecha": dia.ValorFecha.year,
    #             "ValorFecha": dia.ValorFecha.strftime("%d/%m/%Y"),
    #             "PerteneceMes": dia.PerteneceMes,
    #             "Orden": dia.Orden,
    #             **marca_info
    #         }
            
    #         if abrev not in dias_agrupados:
    #             dias_agrupados[abrev] = []
    #         dias_agrupados[abrev].append(dia_info)
        
    #     return dias_agrupados
    
    def get_DiasAgrupado(self, obj):
        # Obtener marcas para optimizar la búsqueda
        marcas = { 
            (marca["DesdeDia_id"], marca["HastaDia_id"]): {
                "Intensidad": marca["Intensidad_id"], 
                "TipoMarca": marca["TipoMarca_id"]
            }
            for marca in self.context["marcas"]
        }

        # Agrupar los días por la abreviatura (LU, MA, etc.)
        dias_agrupados = {}
        i=0
        total=len(obj.calendariodias_set.all())
        
        for dia in obj.calendariodias_set.all():
            


            if i ==0:
                if i!=dia.DiaSemana.NumeroDia:
                    
                    c=dia.DiaSemana.NumeroDia
                    c_i=dia.id - dia.DiaSemana.NumeroDia
                    while c >0:
                        condicion1=Q(id__exact=c_i)
                        
                        data_dia = CalendarioDias.objects.select_related("DiaSemana").filter(condicion1).values(
                                "id",
                                "Calendario_id",
                                "DiaSemana_id",  # ID de la relación con DiasSemana
                                "ValorFecha",
                                "DiaValorFecha",
                                "MesValorFecha",
                                "AnnoValorFecha",
                                "PerteneceMes",
                                "Orden",
                                "FechaRegistro"
                            ).annotate(
                                NombreDia=F("DiaSemana__NombreDia"),  # Obtener el NombreDia de la relación
                                Abreviatura=F("DiaSemana__Abreviatura")  # Obtener la Abreviatura de la relación
                            )
                        valores_data_dia=data_dia[0]
                        abrev = valores_data_dia['Abreviatura']
                        dia_info = {
                            "id": valores_data_dia['id'] * (-1),
                            "NombreDia": valores_data_dia['NombreDia'],
                            "DiaValorFecha": valores_data_dia['ValorFecha'].day,
                            "MesValorFecha": valores_data_dia['ValorFecha'].month,
                            "AnnoValorFecha": valores_data_dia['ValorFecha'].year,
                            "ValorFecha": valores_data_dia['ValorFecha'].strftime("%d/%m/%Y"),
                            "PerteneceMes": False,
                            "Orden": valores_data_dia['Orden'],
                            
                        }
                        
                        if abrev not in dias_agrupados:
                            dias_agrupados[abrev] = []
                        dias_agrupados[abrev].append(dia_info)
                        c_i=c_i +1
                        c=c -1
                        

            abrev = dia.DiaSemana.Abreviatura

            # Verificar si el ID del día está en algún rango de marcas
            marca_info = {"Marca": False, "Intensidad": 0, "TipoMarca": 0}
            for (desde, hasta), valores in marcas.items():
                if desde <= dia.id <= hasta:
                    marca_info = {"Marca": True, "Intensidad": valores["Intensidad"], "TipoMarca": valores["TipoMarca"]}
                    break
            
            dia_info = {
                "id": dia.id,
                "NombreDia": dia.DiaSemana.NombreDia,
                "DiaValorFecha": dia.ValorFecha.day,
                "MesValorFecha": dia.ValorFecha.month,
                "AnnoValorFecha": dia.ValorFecha.year,
                "ValorFecha": dia.ValorFecha.strftime("%d/%m/%Y"),
                "PerteneceMes": dia.PerteneceMes,
                "Orden": dia.Orden,
                **marca_info
            }
            
            if abrev not in dias_agrupados:
                dias_agrupados[abrev] = []
            dias_agrupados[abrev].append(dia_info)
            i=i +1
            if total==i:
                
                if dia.DiaSemana.NumeroDia !=6:
                    fin_inicio=dia.DiaSemana.NumeroDia +1
                    fin_id=dia.id +1
                    while fin_inicio <= 6:


                        condicion1=Q(id__exact=fin_id)
                        
                        data_dia = CalendarioDias.objects.select_related("DiaSemana").filter(condicion1).values(
                                "id",
                                "Calendario_id",
                                "DiaSemana_id",  # ID de la relación con DiasSemana
                                "ValorFecha",
                                "DiaValorFecha",
                                "MesValorFecha",
                                "AnnoValorFecha",
                                "PerteneceMes",
                                "Orden",
                                "FechaRegistro"
                            ).annotate(
                                NombreDia=F("DiaSemana__NombreDia"),  # Obtener el NombreDia de la relación
                                Abreviatura=F("DiaSemana__Abreviatura")  # Obtener la Abreviatura de la relación
                            )
                        valores_data_dia=data_dia[0]
                        abrev = valores_data_dia['Abreviatura']
                        dia_info = {
                            "id": valores_data_dia['id'] * (-1),
                            "NombreDia": valores_data_dia['NombreDia'],
                            "DiaValorFecha": valores_data_dia['ValorFecha'].day,
                            "MesValorFecha": valores_data_dia['ValorFecha'].month,
                            "AnnoValorFecha": valores_data_dia['ValorFecha'].year,
                            "ValorFecha": valores_data_dia['ValorFecha'].strftime("%d/%m/%Y"),
                            "PerteneceMes": False,
                            "Orden": valores_data_dia['Orden'],
                            
                        }
                        
                        if abrev not in dias_agrupados:
                            dias_agrupados[abrev] = []
                        dias_agrupados[abrev].append(dia_info)






                        fin_id=fin_id +1
                        fin_inicio=fin_inicio + 1
        
        return dias_agrupados
    