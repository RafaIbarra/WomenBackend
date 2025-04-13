from rest_framework import serializers
from WomenPeriodApp.models import DiasPreviosAvisoPeriodo

class DiasPreviosAvisoPeriodoSerializer(serializers.ModelSerializer):
    class Meta:
        model=DiasPreviosAvisoPeriodo
        fields= '__all__'
        
    FechaRegistro = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    