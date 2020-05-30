from django.contrib import admin
from .models import Camion, Planta, Producto, Productor, Transportista, Chacra, Reserva #Estadopedido


# Register your models here.
admin.site.register(Productor)
admin.site.register(Chacra)
admin.site.register(Producto)
admin.site.register(Planta)
admin.site.register(Camion)
admin.site.register(Transportista)
admin.site.register(Reserva)


