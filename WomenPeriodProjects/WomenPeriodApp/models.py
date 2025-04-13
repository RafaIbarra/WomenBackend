from django.db import models


# Create your models here.

class Usuarios(models.Model):
    
    id= models.IntegerField(primary_key=True, serialize=False)
    nombre_usuario=models.CharField(max_length=200,blank=False)
    apellido_usuario=models.CharField(max_length=200,blank=False)
    fecha_nacimiento=models.DateField("Fecha Nacimiento")
    user_name=models.CharField(max_length=100,blank=False,unique=True)
    correo=models.EmailField(blank=True)
    numero_telefono=models.CharField(max_length=20,blank=True)
    ultima_conexion=models.DateTimeField("fecha ultma conexion")
    push_token = models.CharField(max_length=255, blank=True, null=True)
    fecha_registro=models.DateTimeField("fecha registro")

    class Meta:
        db_table="Usuarios"

class SesionesActivas(models.Model):
    id= models.AutoField(primary_key=True, serialize=False)
    user_name=models.CharField(max_length=100,blank=False)
    fecha_conexion=models.DateTimeField("fecha ultma conexion")
    token_session=models.CharField(max_length=100,blank=True)
    dispositivo=models.CharField(max_length=200,blank=True)
    
    class Meta:
        db_table="SesionesActivas"

    def __str__(self):
        return (f"{self.user_name.capitalize()} , {self.user_name.capitalize()}")
    
class SolicitudPassword(models.Model):
    CAMBIO_CONTRASENA = 1
    RECUPERACION_CONTRASENA = 2

    OPCIONES_TIPO = [
        (CAMBIO_CONTRASENA, 'Cambio de contraseña'),
        (RECUPERACION_CONTRASENA, 'Recuperación de contraseña'),
    ]
    
    id= models.AutoField(primary_key=True, serialize=False)
    user=models.ForeignKey(Usuarios, on_delete=models.CASCADE, default=1)
    codigo_recuperacion=models.IntegerField()
    fecha_creacion=models.DateTimeField("fecha creacion",blank=False)
    fecha_vencimiento=models.DateTimeField("fecha vencimiento",blank=False)
    fecha_procesamiento=models.DateTimeField("fecha vencimiento",blank=True,null=True)
    codigo_tipo = models.IntegerField(choices=OPCIONES_TIPO, default=RECUPERACION_CONTRASENA) 

    class Meta:
        db_table="SolicitudPassword"

class Versiones(models.Model):
    id= models.AutoField(primary_key=True, serialize=False)
    version=models.CharField(max_length=20,blank=False)
    link_descarga=models.CharField(max_length=200,blank=False)
    descripcion=models.CharField(max_length=200,blank=False)
    estado=models.IntegerField()
    fecha_creacion=models.DateTimeField("fecha creacion",blank=False)

    class Meta:
        db_table="Versiones"
class Meses(models.Model):
    
    id= models.AutoField(primary_key=True, serialize=False)
    NumeroMes = models.IntegerField(unique=True) 
    NombreMes=models.CharField(max_length=200,blank=False)
    FechaRegistro=models.DateTimeField("fecha registro")

    class Meta:
        db_table="Meses"

class DiasSemana(models.Model):
    
    id= models.AutoField(primary_key=True, serialize=False)
    NumeroDia=models.IntegerField(unique=True) 
    NombreDia=models.CharField(max_length=200,blank=False)
    Abreviatura=models.CharField(max_length=2,blank=False,default='LU')
    FechaRegistro=models.DateTimeField("fecha registro")

    class Meta:
        db_table="DiasSemana"

class Calendario(models.Model):
    
    id= models.AutoField(primary_key=True, serialize=False)
    Mes=models.ForeignKey(Meses, on_delete=models.CASCADE, default=1)
    AnnoCalendario=models.IntegerField(blank=False,default=2025)
    FechaInicio=models.DateField("Fecha Inicio Mes")
    FechaFin=models.DateField("Fecha Fin Mes")
    FechaRegistro=models.DateTimeField("fecha registro")

    class Meta:
        db_table="Calendario"

class CalendarioDias(models.Model):
    
    id= models.AutoField(primary_key=True, serialize=False)
    Calendario=models.ForeignKey(Calendario, on_delete=models.CASCADE, default=1)
    DiaSemana=models.ForeignKey(DiasSemana, on_delete=models.CASCADE, default=1)
    ValorFecha=models.DateField("Fecha")
    DiaValorFecha=models.IntegerField()
    MesValorFecha=models.IntegerField()
    AnnoValorFecha=models.IntegerField(blank=False,default=2025)
    PerteneceMes=models.BooleanField(default=True) 
    Orden=models.IntegerField()
    FechaRegistro=models.DateTimeField("fecha registro")

    class Meta:
        db_table="CalendarioDias"

class NivelIntensidad(models.Model):
    
    id= models.AutoField(primary_key=True, serialize=False)
    NombreIntensidad=models.CharField(max_length=100,blank=False)
    NumeroNivel=models.IntegerField()
    FechaRegistro=models.DateTimeField("fecha registro")

    class Meta:
        db_table="NivelIntensidad"

class TipoMarca(models.Model):
    
    id= models.AutoField(primary_key=True, serialize=False)
    NombreTipoMarca=models.CharField(max_length=100,blank=False)
    FechaRegistro=models.DateTimeField("fecha registro")

    class Meta:
        db_table="TipoMarca"

class MarcasUsuario(models.Model):
    
    id= models.AutoField(primary_key=True, serialize=False)
    user=models.ForeignKey(Usuarios, on_delete=models.CASCADE, default=1)
    Intensidad=models.ForeignKey(NivelIntensidad, on_delete=models.CASCADE, default=1)
    TipoMarca=models.ForeignKey(TipoMarca, on_delete=models.CASCADE, default=1)
    DesdeDia = models.ForeignKey(CalendarioDias, on_delete=models.CASCADE, default=1, related_name='marcas_desde_dia')
    HastaDia = models.ForeignKey(CalendarioDias, on_delete=models.CASCADE, default=1, related_name='marcas_hasta_dia')
    Observacion=models.CharField(max_length=100,blank=True,null=True)
    FechaRegistro=models.DateTimeField("fecha registro")

    class Meta:
        db_table="MarcasUsuario"

class DiasPreviosAvisoPeriodo(models.Model):
    id= models.AutoField(primary_key=True, serialize=False)
    user=models.ForeignKey(Usuarios, on_delete=models.CASCADE, default=1)
    CantidadDias=models.IntegerField() 
    FechaRegistro=models.DateTimeField("fecha registro",null=True,blank=True)

    class Meta:
        db_table="DiasPreviosAvisoPeriodo"
