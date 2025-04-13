from rest_framework import serializers
from WomenPeriodApp.models import MarcasUsuario

class MarcasUsuarioSerializers(serializers.ModelSerializer):
    class Meta:
        model=MarcasUsuario
        fields= '__all__'
    FechaRegistro = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S')