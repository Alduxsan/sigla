from django.db import models
from django.db.models import Model
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from datetime import date, datetime, time
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

from sms_function import sms_productor,sms_transportista

#Creación productor#
class Productor(models.Model):
    
    ACTIVO = 'Activo'
    INACTIVO = 'Inactivo'
   
    STATUS = [
        (ACTIVO, ('Activo')),
        (INACTIVO, ('Inactivo'))
        ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    celular = models.CharField(db_column='celular', max_length=8, null=False, blank=False, validators=[RegexValidator('^[0-9_]*$','Ingrese solo números sin el cero inicial')])
    direccion = models.TextField(db_column='direccion', max_length=100, blank=False, null=False)
    razonsocial = models.TextField(db_column='razonSocial', max_length=80)  
    rut = models.CharField(db_column='rut', max_length=12, blank=False, null=False,unique=True, validators=[RegexValidator('^[0-9_]*$','Ingrese formato correcto para RUT, solo 12 números')])  
    nombre = models.CharField(db_column='nombre', max_length=15, blank=False, null=False)  
    apellido = models.CharField(db_column='apellido', max_length=50, blank=False, null=False) 
    email = models.CharField(db_column='email', max_length=50, blank=True, null=True) 
    estado = models.CharField(db_column='estado', max_length=20, choices= STATUS, default='Activo', blank=False, null=False)
    
    class Meta:
        managed = True
        db_table = 'Productor'
        verbose_name = "Productor"
        verbose_name_plural = "Productores"
        ordering = ['user','estado']

    def __str__(self):
        "Returns the person's full name."
        return '%s %s' % (self.nombre, self.apellido)

#Creación transportista#
class Transportista(models.Model):

    ACTIVO = 'Activo'
    INACTIVO = 'Inactivo'
   
    STATUS = [
        (ACTIVO, ('Activo')),
        (INACTIVO, ('Inactivo'))
        ] 

    nombre = models.CharField(db_column='Nombre', max_length=100, blank=False, null=False)  
    rut = models.CharField(db_column='RUT', max_length=12, blank=False, null=False,unique=True, validators=[RegexValidator('^[0-9_]*$','Ingrese formato correcto para RUT, solo 12 números')])  
    direccion = models.TextField(db_column='Direccion', max_length=100, blank=False, null=False) 
    celular = models.CharField(db_column='celular', max_length=8, null=False, blank=False, validators=[RegexValidator('^[0-9_]*$','Ingrese solo números sin el cero inicial')])
    email = models.CharField(db_column='eMail', max_length=50, blank=True, null=True)  
    estado = models.CharField(db_column='estado', max_length=20, choices= STATUS, default="Activo", blank=False, null=False)

    class Meta:
        managed = True
        db_table = 'Transportista'
        verbose_name = "Transportista"
        verbose_name_plural = "Transportistas"
        ordering = ['nombre', 'estado']

    def __str__(self):
        
        return self.nombre

#Creación camion
class Camion(models.Model):

#Estados para camion 
    disponible = 'Disponible'
    ocupado = 'Ocupado'
    no_disponible = 'No disponible'
   
    STATUS = [
        (disponible, ('Disponible')),
        (ocupado, ('Ocupado')),
        (no_disponible,('No disponible'))
        ]
    matricula = models.CharField(db_column='matricula', max_length=7, blank=False,unique=True, null=False, validators=[RegexValidator('^[A-Z_0-9]*$','Ingrese matricula en mayusculas y sin espacio')])
    idtransportista = models.ForeignKey(Transportista,on_delete = models.CASCADE)
    marca = models.CharField(db_column='marca', max_length=20, blank=False, null=False)  
    modelo = models.CharField(db_column='modelo', max_length=20,blank=False, null=False)  
    viajes = models.IntegerField(db_column='viajes_asignados', validators=[MaxValueValidator(2), MinValueValidator(0)], default=0)
    estado = models.CharField(db_column='estado', max_length=13, choices= STATUS, default="Disponible", blank=False, null=False)

    class Meta:
        managed = True
        db_table = 'Camion'
        verbose_name = "Camion"
        verbose_name_plural = "Camiones"
        ordering = ['matricula','estado']
    

    def __str__(self):
      
        return self.matricula

#Creación chacra#  
class Chacra(models.Model):

    ACTIVO = 'Activo'
    INACTIVO = 'Inactivo'
   
    STATUS = [
        (ACTIVO, ('Activo')),
        (INACTIVO, ('Inactivo'))
        ]
    nombre = models.CharField(db_column='Nombre', max_length=50, blank=False, null=False,unique=True,validators=[RegexValidator('^[A-Z]+(?: [A-Z0-9]+)*$','Ingrese nombre de chacra en mayúsculas')])  
    productor = models.ForeignKey(Productor, on_delete = models.CASCADE)
    ubicacion = models.TextField(db_column='Ubicacion', max_length=100, blank=False, null=False,validators=[RegexValidator('^[A-Z]+(?: [A-Z0-9]+)*$','Ingrese ubicación en mayúsculas')]) 
    observacion = models.CharField(db_column='Observacion', max_length=100, blank=True, null=True)  
    estado = models.CharField(db_column='estado', max_length=10, choices= STATUS, default="Activo", blank=False, null=False)
   
    def __str__(self):
     
        return self.nombre
    
    class Meta:
        managed = True
        db_table = 'Chacra'
        verbose_name = "Chacra"
        verbose_name_plural = "Chacras"
        ordering = ['nombre', 'estado']

#Creación planta# 
class Planta(models.Model):

    ACTIVO = 'Activo'
    INACTIVO = 'Inactivo'
   
    STATUS = [
        (ACTIVO, ('Activo')),
        (INACTIVO, ('Inactivo'))
        ]
    nombre = models.TextField(db_column='nombre',  max_length=20, null=False, blank=False,unique=True, 
    validators=[RegexValidator('^[A-Z]+(?: [A-Z0-9]+)*$','Solo se admiten mayúsculas')])  
    direccion = models.TextField(db_column='direccion', max_length=100, blank=False, null=False)  
    celular = models.CharField(db_column='celular', max_length=8, null=False, blank=False, validators=[RegexValidator('^[0-9_]*$','Ingrese solo números sin el cero inicial')]) 
    estado = models.CharField(db_column='estado', max_length=20, choices= STATUS, default="Activo", blank=False, null=False)
 
    class Meta:
        managed = True
        db_table = 'Planta'
        verbose_name = "Planta"
        verbose_name_plural = "Plantas"
        ordering = ['nombre','estado']
    
    def __str__(self):
     
        return self.nombre

#Creación producto# 
class Producto(models.Model):
    
    ACTIVO = 'Activo'
    INACTIVO = 'Inactivo'
   
    STATUS = [
        (ACTIVO, ('Activo')),
        (INACTIVO, ('Inactivo'))
        ]
    nombre = models.CharField(db_column='Nombre', max_length=15, blank=False, null=False, validators=[RegexValidator('^[A-Z_]*$','Ingrese nombre producto en mayúsculas')])
    zafra = models.CharField(db_column='Zafra', max_length=4, blank=False, null=False, validators=[RegexValidator('^[0-9_]*$','Ingrese año de zafra')])  
    estado = models.CharField(db_column='estado', max_length=20, choices= STATUS, default="Activo", blank=False, null=False)
 
    class Meta:
        managed = True
        db_table = 'Producto'
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['zafra', 'nombre']

    def __str__(self):
        
        return self.nombre


#Creación reserva#
class Reserva(models.Model):

#Estados de la reserva#    
    PENDIENTE = 'Pendiente'
    ASIGNADO = 'Asignado'
    RECHAZADO = 'Rechazado'
    ENTREGADO = 'Entregado'
    SIN_MOTIVO = 'NO'
    FIN_CHACRA = 'Fin de chacra'
    ROT_CAMION = 'Rotura de camión'
    ROT_MAQUIN = 'Rotura de maquina en chacra'
    DESVIO_CAM = 'Desvío de camión'
    CANCELA_PROD = 'Cancelada por productor'
    LLUVIA = 'Lluvia'

    ESTADOS = [
        (PENDIENTE, ('Pendiente')),
        (ASIGNADO, ('Asignado')),
        (RECHAZADO,('Rechazado')),
        (ENTREGADO,('Entregado'))
        ]
#Motivos para el rechazo de reservas#
    MOTIVO_RECHAZO = [
        (SIN_MOTIVO, ('NO')),
        (FIN_CHACRA, ('Fin de chacra')),
        (ROT_CAMION, ('Rotura de camión')),
        (ROT_MAQUIN, ('Rotura de maquina en chacra')),
        (DESVIO_CAM, ('Desvío de camión')),
        (CANCELA_PROD, ('Cancelada por productor')),
        (LLUVIA, ('Lluvia'))
            ]


    productor = models.ForeignKey(Productor, on_delete=models.CASCADE, default = User )
    chacra = models.ForeignKey(Chacra, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, blank=False, null=False, on_delete=models.PROTECT, default=None)
    fecha = models.DateField(default=date.today, blank=False, null=False)
    hora = models.TimeField(default=datetime.now,blank=False, null=False)
    observaciones = models.TextField(db_column='observaciones', max_length=80, blank=True)
    motivo_rechazo = models.CharField(db_column='observacion por rechazo', choices= MOTIVO_RECHAZO, default = SIN_MOTIVO, max_length = 30)
    idcamion = models.ForeignKey(Camion, blank=True, null=True, on_delete=models.PROTECT)
    idplanta = models.ForeignKey(Planta, blank=True, null=True, on_delete=models.PROTECT)
    fecha_hora_creacion = models.DateTimeField(default=datetime.now,blank=True)
    estado = models.CharField(db_column='estado', max_length=20, choices= ESTADOS, default='Pendiente', blank=False, null=False)
    
    class Meta:
        managed = True
        db_table = 'reserva'
        verbose_name = "reserva"
        verbose_name_plural = "reservas"
        ordering = ['-fecha','productor']
    
    
    def __str__(self):
        
        return '{}: {}'.format(self.productor, self.chacra)
    
    def clean(self, *args, **kwargs):
       #corre validacion base
        super(Reserva, self).clean(*args, **kwargs)

        
       #no permite fechas anteriores a la actual#
        if self.fecha < date.today():
            if self.estado == 'Rechazado' or self.estado == 'Entregado':
                pass
            else:
                raise ValidationError('Debe reservar para una fecha posterior a la actual')
        #no permite estado rechazado sin indicar motivo#
        if self.estado == "Rechazado" and (self.motivo_rechazo == 'NO'):
            raise ValidationError('Indique Motivo de Rechazo por favor')

#Control de estado disponible para asignación de camion#
    def save(self, *args, **kwargs):

        if self.idcamion and self.idplanta:
            nomb = self.productor.nombre
            prod = self.producto.nombre
            chac = self.chacra.nombre
            ubic = self.chacra.ubicacion
            cami = self.idcamion.matricula
            fecha = self.fecha
            hora = self.hora
            num_prod = '98877232'
            num_tran = '98877232'
            camion_act = Camion.objects.get(matricula=cami)
            obs_rechazo = self.get_motivo_rechazo_display()

            if self.estado == "Entregado":
                tipo = 2
                camion_act.viajes -= 1
                if camion_act.viajes < 0:
                    camion_act.viajes = 0
                camion_act.estado = "Disponible"
                camion_act.save()
                
                super().save(*args, **kwargs)
                return sms_productor(tipo, nomb, prod, chac, cami, num_prod,fecha, hora, obs_rechazo)

            else:
                if self.estado == "Rechazado" and (self.motivo_rechazo != '0'):
                    
                    tipo_prod = 3
                    tipo_tran = 5
                    
                    camion_act.viajes -= 1
                    if camion_act.viajes < 0:
                        camion_act.viajes = 0
                    camion_act.estado = "Disponible"
                    camion_act.save()
                    
                    super().save(*args, **kwargs)
                    sms_productor(tipo_prod, nomb, prod, chac, cami, num_prod,fecha, hora, obs_rechazo)
                    sms_transportista(tipo_tran, chac, ubic, fecha, cami, num_tran, hora,obs_rechazo)

                else:
                    if (not camion_act.viajes == 2 ):

                        self.estado = "Asignado"
                        camion_act.viajes += 1
                        if camion_act.viajes == 2:
                            camion_act.estado = "Ocupado"
                            camion_act.save()
                        else:
                            camion_act.estado = "Disponible"
                            camion_act.save()
                            
                        tipo_prod = 1
                        tipo_tran = 4
                        
                        super().save(*args, **kwargs)
                        sms_productor(tipo_prod,nomb,prod,chac,cami,num_prod,fecha, hora, obs_rechazo), 
                        sms_transportista(tipo_tran, chac, ubic, fecha, cami, num_tran, hora,obs_rechazo)

        else:
            if (not self.idcamion) and (self.estado == "Rechazado"):
                super().save(*args, **kwargs)

            else:
                self.estado = "Pendiente"
                super().save(*args, **kwargs)                    
            
