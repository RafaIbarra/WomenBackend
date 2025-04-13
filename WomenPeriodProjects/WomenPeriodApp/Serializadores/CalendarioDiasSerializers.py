from rest_framework import serializers
from WomenPeriodApp.models import CalendarioDias,DiasSemana

class CalendarioDiasSerializers(serializers.ModelSerializer):
    NumeroDia=serializers.SerializerMethodField()
    NombreDia=serializers.SerializerMethodField()
    AbreviaturaDia=serializers.SerializerMethodField()
    class Meta:
        model=CalendarioDias
        fields= [
                "id",
                "Calendario",
                "DiaSemana",
                "NumeroDia",
                "NombreDia",
                "AbreviaturaDia",
                "ValorFecha",
                "DiaValorFecha",
                "MesValorFecha",
                "AnnoValorFecha",
                "PerteneceMes",
                "Orden",
                "FechaRegistro",
                ]
    FechaRegistro = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S')
    ValorFecha= serializers.DateField(format='%d/%m/%Y')

    def get_NumeroDia(self, obj):
        
        codigo = obj.DiaSemana_id
        try:
            empresa_obj = DiasSemana.objects.get(id=codigo)
            return empresa_obj.NumeroDia
        except DiasSemana.DoesNotExist:
            return None
        
    def get_NombreDia(self, obj):
        
        codigo = obj.DiaSemana_id
        try:
            empresa_obj = DiasSemana.objects.get(id=codigo)
            return empresa_obj.NombreDia
        except DiasSemana.DoesNotExist:
            return None
        
    def get_AbreviaturaDia(self, obj):
        
        codigo = obj.DiaSemana_id
        try:
            empresa_obj = DiasSemana.objects.get(id=codigo)
            return empresa_obj.Abreviatura
        except DiasSemana.DoesNotExist:
            return None
        
class CalendarioDiasSerializersNormal(serializers.ModelSerializer):
    
    
    class Meta:
        model=CalendarioDias
        fields= '__all__'
        
    ValorFecha= serializers.DateField(format='%d/%m/%Y')
    