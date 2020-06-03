#Estados de la reserva#    
PENDIENTE = 'Pendiente'; ASIGNADO = 'Asignado'; RECHAZADO = 'Rechazado'; ENTREGADO = 'Entregado'
SIN_MOTIVO = 'NO'; FIN_CHACRA = 'Fin de chacra'; ROT_CAMION = 'Rotura de camión'; ROT_MAQUIN = 'Rotura de maquina en chacra'
DESVIO_CAM = 'Desvío de camión'; CANCELA_PROD = 'Cancelada por productor'; LLUVIA = 'Lluvia'

ESTADOS = [
    (PENDIENTE, ('Pendiente')),
    (ASIGNADO, ('Asignado')),
    (RECHAZADO,('Rechazado')),
    (ENTREGADO,('Entregado'))
    ]

ESTADOS_ASIGNADA = [
    (ASIGNADO, ('Asignado')),
    (RECHAZADO,('Rechazado')),
    (ENTREGADO,('Entregado'))
    ]

ESTADOS_PENDIENTE = [
    (PENDIENTE, ('Pendiente')),
    (RECHAZADO,('Rechazado'))
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