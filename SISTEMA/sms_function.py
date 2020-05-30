import os
from twilio.rest import Client

account = 'ACf9e1a57719322f8971ade2052e91ee47'
auth = 'ea0050cef2ef5222d69a1f4cb5ed427b'

#tipos de mensaje segun estados:
    # 1 - Mensaje al productor cuando se asigna matricula 
    # 2 - Mensaje al productor cuando se entrega producto en Planta
    # 3 - Mensaje al productor de flete Rechazado
    # 4 - Mensaje al transportista cuando se asigna matricula
    # 5 - Mensaje al transportista cuando se cancela reserva que se le asigno
  
def sms_productor(tipo, nombre, producto, chacra, camion, celular, fecha, hora, obs_rechazo):
    account_sid = account
    auth_token = auth
    client = Client(account_sid, auth_token)

    if tipo == 1:
        message = client.messages \
            .create(
                body='Estimado/a {} su flete para {} en {} ha sido asignado. Sera recogido por el camion de matricula {}, el {} y aproximadamente a las {} horas.'.format(nombre, producto, chacra, camion, fecha, hora),
                from_='+15005550006',  #este valor tambien deberia ir almacenada en una variable de entorno
                to='+598'+celular
                )
                
        print(message.sid), print(message.body)  
    
    else:
        if tipo == 2:
            message = client.messages \
                .create(
                    body='Estimado/a {} su cosecha de {} recogido el {}, ha sido entregado correctamente por el camion {}'.format(nombre, producto, fecha, camion),
                    from_='+15005550006',  #este valor tambien deberia ir almacenada en una variable de entorno
                    to='+598'+celular
                    )
                    
            print(message.sid), print(message.body)

        else:
            if tipo == 3:
                message = client.messages \
                    .create(
                        body='Estimado/a {} su reserva de {} para el {} a las {} ha sido rechazada. Motivo: {}'.format(nombre, producto, fecha,hora, obs_rechazo),
                        from_='+15005550006',  #este valor tambien deberia ir almacenada en una variable de entorno
                        to='+598'+celular
                        )  

                print(message.sid), print(message.body)   
        
#A la funcion de transportista despues hay que cambiarle la variable del celular.
def sms_transportista(tipo, chacra, direccion, fecha, matricula, celular, hora, obs_rechazo):
    account_sid = account
    auth_token = auth
    client = Client(account_sid, auth_token)
    if tipo == 4:
            message = client.messages \
                .create(
                body= 'Se solicita FLETE para {} en {}, el dia {} a las {}, asignado al camion {}'.format(chacra, direccion, fecha, hora,  matricula),
                from_='+15005550006',  #este valor tambien deberia ir almacenada en una variable de entorno
                to='+598'+celular
            )  

            print(message.sid), print(message.body)

    else:
        if tipo == 5:
            message = client.messages \
                .create(
                    body= 'Se ha CANCELADO el flete para {} en {}, del dia {}, hora {}, asignado al camion {}. Motivo: {}'.format(chacra, direccion, fecha, hora, matricula, obs_rechazo),
                    from_='+15005550006',  #este valor tambien deberia ir almacenada en una variable de entorno
                    to='+598'+celular
                    )
            print(message.sid), print(message.body)
