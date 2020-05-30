from django.contrib.auth.models import User, Group
from django import forms
from .models import Productor, Chacra, Transportista, Camion, Reserva, Planta, Producto
from django.contrib.auth.forms import UserCreationForm
 
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

from django.db.models import Q

#Formulario creación usuario#
class UserForm (forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    re_password = forms.CharField(widget=forms.PasswordInput,label='Repetir contraseña')
    grupo = forms.ModelChoiceField(queryset=Group.objects.all())
     
    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'email', 'username',
                  'password', 're_password']
               
        label = {
            'password': 'Contraseña'
        }

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            initial = kwargs.setdefault('initial', {})
            if kwargs['instance'].groups.all():
                initial['grupo'] = kwargs['instance'].groups.all()[0]
            else:
                initial['grupo'] = None

        forms.ModelForm.__init__(self, *args, **kwargs)

    def clean(self):
        super(UserForm, self).clean()
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')
        if not password == re_password:
            self.add_error('re_password', 'La contraseña no coincide, ingrese nuevamente')

    def save(self):
        password = self.cleaned_data.pop('password')
        grupo = self.cleaned_data.pop('grupo')
        u = super().save()
        u.groups.set([grupo])
        u.set_password(password)
        u.save()
        return u

#Formulario creación productor#
class ProductorForm(forms.ModelForm):

    class Meta:
        model = Productor
        fields = [
            'user',
            'nombre',
            'apellido',
            'razonsocial',
            'rut',
            'direccion',
            'celular',
            'email',
            'estado'
        ]
        labels = {
            'user': 'Usuario',
			'nombre': 'Nombre',
			'apellido': 'Apellido',
			'razonsocial': 'Razón Social',
			'rut':'RUT',
			'direccion': 'Dirección',
		    'celular': 'Celular',
            'email': 'Email',
            'estado': 'Estado',
		  }
        widgets = {
            'user': forms.Select(attrs={'class':'form-control'}),
			'nombre': forms.TextInput(attrs={'class':'form-control'}),
			'apellido': forms.TextInput(attrs={'class':'form-control'}),
			'razonsocial': forms.TextInput(attrs={'class':'form-control'}),
			'rut': forms.TextInput(attrs={'class':'form-control'}),
			'direccion': forms.TextInput(attrs={'class':'form-control'}),
			'celular': forms.TextInput(attrs={'placeholder': 'Ingrese el numero sin el 0 inicial','class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'estado': forms.Select(attrs={'class':'form-control'}),
		   }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(groups__name='Productores')

#Formulario creación chacra#
class ChacraForm(forms.ModelForm):

#Filtrado para que solo muestres productores activos#
    def __init__(self, *args, **kwargs):

        super(ChacraForm, self).__init__( *args, **kwargs) 
    
        self.fields['productor'].queryset = Productor.objects.filter(estado='Activo')

    class Meta:
        model = Chacra
        fields = [  
            'productor',
            'nombre',
            'ubicacion',
            'observacion',
            'estado'
        ]
        labels = {
            'productor': 'Productor',
            'nombre': 'Nombre',
            'ubicacion': 'Ubicación',
            'observacion': 'Observaciones',
            'estado': 'Estado'
		  }
        widgets = {
            'productor': forms.Select(attrs={'class':'form-control'}),
			'nombre': forms.TextInput(attrs={'class':'form-control'}),
			'ubicacion': forms.TextInput(attrs={'class':'form-control'}),
			'observacion': forms.TextInput(attrs={'class':'form-control'}),
			'estado': forms.Select(attrs={'class':'form-control'}),
			
		   }

#Formulario creación transportista#
class TransportistaForm(forms.ModelForm):

    class Meta:
        model = Transportista
        fields = [
            'nombre',
            'rut',
            'direccion',
            'celular',
            'email',
            'estado'
        ]
        labels = {
			'nombre': 'Nombre',
			'rut':'RUT',
			'direccion': 'Dirección',
		    'celular': 'Celular',
            'email': 'Email',
            'estado': 'Estado',
		  }
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
			'rut': forms.TextInput(attrs={'class':'form-control'}),
			'direccion': forms.TextInput(attrs={'class':'form-control'}),
            'celular': forms.TextInput(attrs={'placeholder': 'Ingrese el numero sin el 0 inicial','class':'form-control'}),            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'estado': forms.Select(attrs={'class':'form-control'}),
		   }

#Formulario creación camion#    
class CamionForm(forms.ModelForm):
    
    class Meta:
        model = Camion
        fields = [
            'idtransportista',
            'matricula',
            'marca',
            'modelo',
            'estado',
        ]
        labels = {
			'idtransportista': 'Transportista',
			'matricula':'Matricula',
			'marca': 'Marca',
		    'modelo': 'Modelo',
            'estado': 'Estado',
		  }
        widgets = {
            'idtransportista': forms.Select(attrs={'class':'form-control'}),
			'matricula': forms.TextInput(attrs={'class':'form-control'}),
			'marca': forms.TextInput(attrs={'class':'form-control'}),
			'modelo': forms.TextInput(attrs={'class':'form-control'}),
            'estado': forms.Select(attrs={'class':'form-control'}),
		   }

#Filtrado para que solo muestres transportistas activos#
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['idtransportista'].queryset = Transportista.objects.filter(estado='Activo')

#Formulario creación planta#
class PlantaForm(forms.ModelForm):

    class Meta:
        model = Planta
        fields = [
            'nombre',
            'direccion',
            'celular',
            'estado',
        ]
        labels = {
			'nombre': 'Nombre',
			'direccion':'Dirección',
			'Celular': 'Celular',
		    'estado': 'Estado',
		  }
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
			'direccion': forms.TextInput(attrs={'class':'form-control'}),
			'celular': forms.TextInput(attrs={'placeholder': 'Ingrese el numero sin el 0 inicial','class':'form-control'}),
            'estado': forms.Select(attrs={'class':'form-control'}),
		   }

#Formulario creación producto#
class ProductForm(forms.ModelForm):

    class Meta:
        model = Producto
        fields = [
            'nombre',
            'zafra',
            'estado',
        ]
        labels = {
			'nombre': 'Producto',
			'zafra':'Zafra',
		    'estado': 'Estado',
		  }
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
			'zafra': forms.TextInput(attrs={'class':'form-control'}),
            'estado': forms.Select(attrs={'class':'form-control'}),
		   }
    
#Control para no duplicación de zafra y año#
    def clean(self):
        cleaned_data = super(ProductForm, self).clean()
        nombre = cleaned_data.get("nombre")
        zafra = cleaned_data.get("zafra")
        try:
            producto = Producto.objects.get(nombre=nombre, zafra=zafra)
        except Producto.DoesNotExist:
            pass

        else:
            raise forms.ValidationError(
                "Ya existe este producto para ese año de Zafra"
            )

#Formulario de actualizacion de producto#            
class ProductUpdateForm(forms.ModelForm):

    class Meta:
        model = Producto
        fields = [
            'nombre',
            'zafra',
            'estado',
        ]
        labels = {
			'nombre': 'Producto',
			'zafra':'Zafra',
		    'estado': 'Estado',
		  }
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
			'zafra': forms.TextInput(attrs={'class':'form-control'}),
            'estado': forms.Select(attrs={'class':'form-control'}),
		   }

#Form para el date/time picker en reservas#
class MyDateInput(forms.DateInput):
    input_type = 'date'


class MyTimeInput(forms.TimeInput):
    input_type = 'time'

#Formulario creación reserva por productor#
class ReservaForm(forms.ModelForm):


    def __init__(self, *args, **kwargs):

        user = kwargs.pop('user')
        logged_user = user
        

        super(ReservaForm, self).__init__( *args, **kwargs) 
    
        self.fields['producto'].queryset = Producto.objects.filter(estado='Activo')
        chacras_choices = []

        #obtener el id del productor igual al id del logueado
        productorid = Productor.objects.filter(user_id=logged_user.id) 
        
        #obtener chacras donde el id del productor coincida con el id del usuario logueado
        chacras = Chacra.objects.filter(Q(productor__id__in=productorid) &  Q(estado='Activo'))
        
        #bucle para grupo iterable de select de chacras segun productor
        for chacra in chacras:
             chacras_choices.append((chacra.id,chacra.nombre))
        
        logged_productor = []
        #obtener productores con el id igual al del logueado
        productores = Productor.objects.filter(user_id= logged_user.id)

        nombre = '{} {}'.format(logged_user.first_name, logged_user.last_name)
        for productor in productores:
            
            logged_productor.append((productor.id, nombre))

        self.fields['productor'].choices = logged_productor
        self.fields['chacra'].choices = chacras_choices
        self.fields['productor'].readonly = True
        self.fields['productor'].initial = logged_productor

   
    class Meta:

        model = Reserva

        widgets = {
            'productor': forms.Select(attrs={'class':'form-control', 'id':'productor'}),
            'chacra': forms.Select(choices=[],attrs={'class':'form-control', 'id':'chacra'}),
            'producto': forms.Select(attrs={'class':'form-control', 'id':'producto'}),
            'fecha': MyDateInput(attrs={'class':'form-control', 'id':'fecha'}),
            'hora' : MyTimeInput(attrs={'class':'form-control', 'id':'hora'}),
			'observaciones': forms.TextInput(attrs={'rows':4, 'cols':15, 'class':'form-control', 'id':'observaciones'}),
			'fecha_hora_creacion': forms.HiddenInput(attrs={'class':'form-control', 'id':'fecha_hora_creacion'})
		}

        fields = [
			
			'productor', 'chacra', 'producto',
			'fecha','hora', 'observaciones', 'fecha_hora_creacion']
		
        labels = {
			'productor': 'Productor',
			'chacra': 'Chacra',
			'producto': 'Producto',
			'fecha': 'Fecha de recogida',
            'hora': 'Hora de recogida',
			'observaciones': 'Observaciones',
			'fecha_hora_creacion': 'Fecha y hora de creacion'
			
		  }

#Formulario creación reserva por el operador#
class ReservaOperForm(forms.ModelForm):

    class Meta:
        model = Reserva
        fields = [
            'productor',
            'chacra',
            'producto',
            'fecha',
            'hora',
            'observaciones',
            'idcamion',
            'idplanta',
            'estado',
            'fecha_hora_creacion',
        ]
        labels = {
			'productor': 'Productor',
			'chacra':'Chacra',
		    'producto': 'Producto',
            'fecha': 'Fecha de recogida',
            'hora': 'Hora de recogida',
            'observaciones': 'Observaciones',
            'idcamion': 'Camion',
            'idplanta': 'Planta descarga',
            'estado': 'Estado',
            'fecha_hora_creacion': 'Fecha y hora de creacion',
		  }
        widgets = {
            'nombre': forms.Select(attrs={'class':'form-control'}),
			'chacra': forms.Select(attrs={'class':'form-control'}),
            'producto': forms.Select(attrs={'class':'form-control'}),
            'fecha': MyDateInput(attrs={'class':'form-control', 'id':'fecha'}),
            'hora' : MyTimeInput(attrs={'class':'form-control', 'id':'hora'}),
            'observaciones': forms.TextInput(attrs={'class':'form-control'}),
            'idcamion': forms.Select(attrs={'class':'form-control'}),
            'idplanta': forms.Select(attrs={'class':'form-control'}),
            'estado': forms.Select(attrs={'class':'form-control'}),
            'fecha_hora_creacion': forms.DateTimeInput(attrs={'class':'form-control'}),
		   }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['chacra'].queryset = Chacra.objects.none()
        self.fields['idcamion'].queryset = Camion.objects.filter(estado="Disponible")
        self.fields['idplanta'].queryset = Planta.objects.filter(estado='Activo')
        self.fields['estado'].disabled = True
        self.fields['fecha_hora_creacion'].disabled = True
        

        if 'productor' in self.data:
            productor_id = int(self.data.get('productor'))
            self.fields['chacra'].queryset = Chacra.objects.filter(productor_id=productor_id).order_by('nombre')

        elif self.instance.pk:
            self.fields['chacra'].queryset = self.instance.productor.chacra_set.order_by('nombre')

#Formulario de actualizacion reserva de operador#        
class ReservaOperFormUpdate(forms.ModelForm):

    class Meta:

        model = Reserva

        fields = [
            'productor',
            'chacra',
            'producto',
            'fecha',
            'hora',
            'observaciones',
            'motivo_rechazo',
            'idcamion',
            'idplanta',
            'estado',
            'fecha_hora_creacion',
        ]
        labels = {
			'productor': 'Productor',
			'chacra':'Chacra',
		    'producto': 'Producto',
            'fecha': 'Fecha de recogida',
            'hora': 'Hora de recogida',
            'observaciones': 'Observaciones',
            'motivo_rechazo': 'Observación por rechazo',
        
            'idcamion': 'Camion',
            'idplanta': 'Planta descarga',
            'estado': 'Estado',
            'fecha_hora_creacion': 'Fecha y hora de creacion',
		  }
        widgets = {
            'nombre': forms.Select(attrs={'class':'form-control'}),
			'chacra': forms.Select(attrs={'class':'form-control'}),
            'producto': forms.Select(attrs={'class':'form-control'}),
            'fecha': forms.DateInput(attrs={'class':'form-control', 'id':'fecha'}),
            'hora' : forms.TimeInput(attrs={'class':'form-control', 'id':'hora'}),
            'observaciones': forms.TextInput(attrs={'class':'form-control'}),
            'motivo_rechazo': forms.Select(attrs={'class':'form-control'}),
            'idcamion': forms.Select(attrs={'class':'form-control'}),
            'idplanta': forms.Select(attrs={'class':'form-control'}),
            'estado': forms.Select(attrs={'class':'form-control'}),
            'fecha_hora_creacion': forms.DateTimeInput(attrs={'class':'form-control'}),
		   }

#Datos habilitados o inhabilitados#
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['chacra'].disabled = True
        self.fields['productor'].disabled = True
        self.fields['producto'].disabled = True
        self.fields['fecha'].disabled = True
        self.fields['hora'].disabled = True
        self.fields['observaciones'].disabled = True
        self.fields['idcamion'].disabled = True
        self.fields['idplanta'].disabled = True
        self.fields['fecha_hora_creacion'].disabled = True
        
        if 'productor' in self.data:
            try:
                productor_id = int(self.data.get('productor'))
                self.fields['chacra'].queryset = Chacra.objects.filter(productor_id=productor_id).order_by('nombre')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['chacra'].queryset = self.instance.productor.chacra_set.order_by('nombre')

#Formulario actualizacion reserva operador#
class ReservaOperPreEstado(forms.ModelForm):

    class Meta:

        model = Reserva

        fields = [
            'productor',
            'chacra',
            'producto',
            'fecha',
            'hora',
            'observaciones',
            'idcamion',
            'idplanta',
            'estado',
            'fecha_hora_creacion',
        ]
        labels = {
			'productor': 'Productor',
			'chacra':'Chacra',
		    'producto': 'Producto',
            'fecha': 'Fecha de recogida',
            'hora': 'Hora de recogida',
            'observaciones': 'Observaciones',
            'motivo_rechazo': 'Observación por rechazo',
            'idcamion': 'Camion',
            'idplanta': 'Planta descarga',
            'estado': 'Estado',
            'fecha_hora_creacion': 'Fecha y hora de creacion',
		  }
        widgets = {
            'nombre': forms.Select(attrs={'class':'form-control'}),
			'chacra': forms.Select(attrs={'class':'form-control'}),
            'producto': forms.Select(attrs={'class':'form-control'}),
            'fecha': forms.DateInput(attrs={'class':'form-control', 'id':'fecha'}),
            'hora' : forms.TimeInput(attrs={'class':'form-control', 'id':'hora'}),
            'observaciones': forms.TextInput(attrs={'class':'form-control'}),
            'motivo_rechazo': forms.TextInput(attrs={'class':'form-control'}),
            'idcamion': forms.Select(attrs={'class':'form-control'}),
            'idplanta': forms.Select(attrs={'class':'form-control'}),
            'estado': forms.Select(attrs={'class':'form-control'}),
            'fecha_hora_creacion': forms.DateTimeInput(attrs={'class':'form-control'}),
		   }

#Datos habilitados o inhabilitados#
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['chacra'].disabled = True
        self.fields['productor'].disabled = True
        self.fields['producto'].disabled = True
        self.fields['fecha'].disabled = True
        self.fields['hora'].disabled = True
        self.fields['observaciones'].disabled = True
        self.fields['fecha_hora_creacion'].disabled = True
        self.fields['idcamion'].queryset = Camion.objects.filter(estado="Disponible")
        self.fields['idplanta'].queryset = Planta.objects.filter(estado='Activo')
        
        if 'productor' in self.data:
            try:
                productor_id = int(self.data.get('productor'))
                self.fields['chacra'].queryset = Chacra.objects.filter(productor_id=productor_id).order_by('nombre')
            except (ValueError, TypeError):
                pass  
        elif self.instance.pk:
            self.fields['chacra'].queryset = self.instance.productor.chacra_set.order_by('nombre')




            
