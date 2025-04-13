from rest_framework import serializers
from WomenPeriodApp.models import Versiones

class VersionesSerializers(serializers.ModelSerializer):
    class Meta:
        model=Versiones
        fields= '__all__'
        
    # fecha_creacion = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    fecha_creacion = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S')
    