from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User, Group
from django.views.generic.edit import CreateView
from django.views.generic import ListView,UpdateView,DeleteView
from django.urls import reverse_lazy,reverse
import requests
from requests import request
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q

from .models import Productor, Chacra, Transportista, Camion, Planta, Producto, Reserva
from .forms import ProductForm, UserForm, ProductorForm, ChacraForm, TransportistaForm, CamionForm, ReservaForm, PlantaForm, \
    ReservaOperForm, ReservaOperFormUpdate,ProductUpdateForm, ReservaOperPreEstado

from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
 
#Control de grupo de usuarios habilitados para el sitio#
def es_miembro(user):
    return user.groups.filter(name='Productores').exists()
def es_miembro2(user):
    return user.groups.filter(name='Operadores').exists()

@login_required
@user_passes_test(es_miembro2, login_url='inicio')
def usuario_crear(request):
    context = {}
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        context['user_form'] = user_form
        if user_form.is_valid():
            u = user_form.save()    
            return HttpResponseRedirect(reverse('inicio_op'))
        else:
            return render(request, 'registrar.html', context)
    else:
        user_form = UserForm()
        context['user_form'] = user_form
        return render(request, 'registrar.html', context)

#Listado de usuarios#
class UserList(UserPassesTestMixin,ListView):
    model = User
    template_name = 'usuario_list.html'
    paginate_by = 10
    def test_func(self):
        return self.request.user.groups.filter(name='Operadores').exists()
    def handle_no_permission(self):
            return HttpResponse('Usuario sin permisos, favor contactar al administrador')

#Actualizacion datos de usuario#
class UserUpdate(UserPassesTestMixin,UpdateView):
    model=User
    form_class=UserForm
    template_name = 'usuario_update.html'
    success_url = reverse_lazy('usuario_listar')
    
    def test_func(self):
        return self.request.user.groups.filter(name='Operadores').exists()
        
    def handle_no_permission(self):
        return HttpResponse('Usuario sin permisos, favor contactar al administrador')

#Listado productores#
class ProductorList(UserPassesTestMixin,ListView):
    model = Productor
    template_name = 'productor_list.html'
    paginate_by = 10
    def test_func(self):
        return self.request.user.groups.filter(name='Operadores').exists()
    def handle_no_permission(self):
            return HttpResponse('Usuario sin permisos, favor contactar al administrador')

#Actualizacion productor#
class ProductorUpdate(UserPassesTestMixin,UpdateView):
    model=Productor
    form_class=ProductorForm
    template_name = 'productor.html'
    success_url = reverse_lazy('productor_listar')
    
    def test_func(self):
        return self.request.user.groups.filter(name='Operadores').exists()
        
    def handle_no_permission(self):
        return HttpResponse('Usuario sin permisos, favor contactar al administrador')

#Eliminar productor#
#class ProductorDelete(UserPassesTestMixin,DeleteView):
 #   model=Productor
  #  template_name='eliminar_productor.html'
   # success_url=reverse_lazy('productor_listar')
    
    #def test_func(self):
     #   return self.request.user.groups.filter(name='Operadores').exists()
        
    #def handle_no_permission(self):return HttpResponse('You have been denied')

#Creación chacra#
class ChacraCreate(CreateView):
    model= Chacra
    form_class = ChacraForm
    template_name = 'chacra_crear.html'
    success_url = reverse_lazy('chacra_listar')

    def test_func(self):
        return self.request.user.groups.filter(name='Operadores').exists()
  
    def handle_no_permission(self):
        return HttpResponse('Usuario sin permisos, favor contactar al administrador')

#Listado de chacras#
class ChacraList(UserPassesTestMixin,ListView):
    model=Chacra
    template_name='chacra_list.html'
    paginate_by = 10
    
    def test_func(self):
        return self.request.user.groups.filter(name='Operadores').exists()
  
    def handle_no_permission(self):
        return HttpResponse('Usuario sin permisos, favor contactar al administrador')

#Actualización de chacras#
class ChacraUpdate(UserPassesTestMixin,UpdateView):
    model=Chacra
    form_class=ChacraForm
    template_name='chacra_crear.html'
    success_url=reverse_lazy('chacra_listar')
    
    def test_func(self):
        return self.request.user.groups.filter(name='Operadores').exists()
  
    def handle_no_permission(self):
        return HttpResponse('Usuario sin permisos, favor contactar al administrador')

#Eliminar chacras#
#class ChacraDelete(UserPassesTestMixin,DeleteView):
 #   model = Chacra
  #  template_name = 'eliminar_chacra.html'
   # success_url = reverse_lazy('chacra_listar')
    
    #def test_func(self):
     #   return self.request.user.groups.filter(name='Operadores').exists()
  
    #def handle_no_permission(self):
     #   """ Do whatever you want here if the user doesn't pass the test """
      #  return HttpResponse('You have been denied')


#Creación transportista#
class TransportistaCreate(UserPassesTestMixin,CreateView):
    model= Transportista
    form_class = TransportistaForm
    template_name = 'transportista_crear.html'
    success_url = reverse_lazy('transportista_listar')

    def test_func(self):
        return self.request.user.groups.filter(name='Operadores').exists()
  
    def handle_no_permission(self):
        return HttpResponse('Usuario sin permisos, favor contactar al administrador')


#Listado transportista#
class TransportistaList(UserPassesTestMixin,ListView):
    model = Transportista
    template_name = 'transportista_list.html'
    paginate_by = 10
    
    def test_func(self):
        return self.request.user.groups.filter(name='Operadores').exists()
    def handle_no_permission(self):
            return HttpResponse('Usuario sin permisos, favor contactar al administrador')

#Actualizacion datos de transportista#
class TransportistaUpdate(UserPassesTestMixin,UpdateView):
    model = Transportista
    form_class = TransportistaForm
    template_name = 'transportista_crear.html'
    success_url = reverse_lazy('transportista_listar')

    def test_func(self):
        return self.request.user.groups.filter(name='Operadores').exists()
  
    def handle_no_permission(self):
        return HttpResponse('Usuario sin permisos, favor contactar al administrador')

#Eliminar transportista#
#class TransportistaDelete(UserPassesTestMixin,DeleteView):
 #   model = Transportista
  #  template_name = 'eliminar_transportista.html'
   # success_url = reverse_lazy('transportista_listar')
    
    #def test_func(self):
    #    return self.request.user.groups.filter(name='Operadores').exists()
  
    #def handle_no_permission(self):
     #   """ Do whatever you want here if the user doesn't pass the test """
      #  return HttpResponse('You have been denied')

#Creacion camion#
class CamionCreate(CreateView):
    model= Camion
    form_class = CamionForm
    template_name = 'camion_crear.html'
    success_url = reverse_lazy('camion_listar')

    def test_func(self):
        return self.request.user.groups.filter(name='Operadores').exists()
  
    def handle_no_permission(self):
        """ Do whatever you want here if the user doesn't pass the test """
        return HttpResponse('Usuario sin permisos, favor contactar al administrador')

#Listado de camiones#
class CamionList(UserPassesTestMixin,ListView):
    model = Camion
    template_name = 'camion_list.html'
    paginate_by = 10

    def test_func(self):
        return self.request.user.groups.filter(name='Operadores').exists()
  
    def handle_no_permission(self):
        """ Do whatever you want here if the user doesn't pass the test """
        return HttpResponse('Usuario sin permisos, favor contactar al administrador')

#Actualizacion datos de camion#
class CamionUpdate(UserPassesTestMixin,UpdateView):
    model = Camion
    form_class = CamionForm
    template_name = 'camion_crear.html'
    success_url = reverse_lazy('camion_listar')

    def test_func(self):
        return self.request.user.groups.filter(name='Operadores').exists()
  
    def handle_no_permission(self):
        return HttpResponse('Usuario sin permisos, favor contactar al administrador')

#Eliminar camiones#
#class CamionDelete(UserPassesTestMixin,DeleteView):
 #   model = Camion
   # template_name = 'eliminar_camion.html'
   # success_url = reverse_lazy('camion_listar')
    
    #def test_func(self):
       # return self.request.user.groups.filter(name='Operadores').exists()
  
    #def handle_no_permission(self):
     #   """ Do whatever you want here if the user doesn't pass the test """
      #  return HttpResponse('You have been denied')

#Creacion de planta de descarga#
class PlantaCreate(UserPassesTestMixin,CreateView):
    model= Planta
    form_class = PlantaForm
    template_name = 'planta_crear.html'
    success_url = reverse_lazy('planta_listar')

    def test_func(self):
        return self.request.user.groups.filter(name='Operadores').exists()

    def handle_no_permission(self):
        return HttpResponse('No tienes acceso')

#Listado de plantas de descarga#
class PlantaList(UserPassesTestMixin,ListView):
    model = Planta
    template_name = 'planta_list.html'
    paginate_by = 10

    def test_func(self):
        return self.request.user.groups.filter(name='Operadores').exists()

    def handle_no_permission(self):
        return HttpResponse('No tienes acceso')

#Actualizacion datos de plantas#
class PlantaUpdate(UserPassesTestMixin,UpdateView):
    model = Planta
    form_class = PlantaForm
    template_name = 'planta_crear.html'
    success_url = reverse_lazy('planta_listar')

    def test_func(self):
        return self.request.user.groups.filter(name='Operadores').exists()

    def handle_no_permission(self):
        return HttpResponse('No tienes acceso')

#Eliminar plantas de descarga#
#class PlantaDelete(UserPassesTestMixin,DeleteView):
    #model = Planta
    #template_name = 'eliminar_planta.html'
    #success_url = reverse_lazy('planta_listar')
    
    #def test_func(self):
    #    return self.request.user.groups.filter(name='Operadores').exists()

   # def handle_no_permission(self):
   #     return HttpResponse('No tienes acceso') 

#Creacion de productos#
class ProductCreate(UserPassesTestMixin,CreateView):
    model= Producto
    form_class = ProductForm
    template_name = 'producto_crear.html'
    success_url = reverse_lazy('producto_listar')

    def test_func(self):
        return self.request.user.groups.filter(name='Operadores').exists()
  
    def handle_no_permission(self):
        return HttpResponse('Usuario sin permisos, favor contactar al administrador')

#Listado de productos#
class ProductList(UserPassesTestMixin,ListView):
    model = Producto
    template_name = 'producto_list.html'
    paginate_by = 10

    def test_func(self):
        return self.request.user.groups.filter(name='Operadores').exists()
  
    def handle_no_permission(self):
        return HttpResponse('Usuario sin permisos, favor contactar al administrador')

#Actualizacion datos de productos#
class ProductUpdate(UserPassesTestMixin,UpdateView):
    model = Producto
    form_class = ProductUpdateForm
    template_name = 'producto_crear.html'
    success_url = reverse_lazy('producto_listar')

    def test_func(self):
        return self.request.user.groups.filter(name='Operadores').exists()
  
    def handle_no_permission(self):
        return HttpResponse('Usuario sin permisos, favor contactar al administrador')
        
#Eliminar producto#
#class ProductDelete(UserPassesTestMixin,DeleteView):
 #   model = Producto
  #  template_name = 'eliminar_producto.html'
    #success_url = reverse_lazy('producto_listar')
    
#    def test_func(self):
 #       return self.request.user.groups.filter(name='Operadores').exists()
  
  #  def handle_no_permission(self):
    #    """ Do whatever you want here if the user doesn't pass the test """
     #   return HttpResponse('You have been denied')

#Creacion de productor#
class ProductorCreate(UserPassesTestMixin,CreateView):
    model= Productor
    form_class = ProductorForm
    template_name = 'productor.html'
    success_url = reverse_lazy('productor_listar')

    def test_func(self):
        return self.request.user.groups.filter(name='Operadores').exists()
  
    def handle_no_permission(self):
        return HttpResponse('Usuario sin permisos, favor contactar al administrador')

@login_required
@user_passes_test(es_miembro, login_url='inicio_op')
def inicio(request):
    if request.method == 'GET':
            return render(request, 'inicio.html', context={})
	
@login_required
@user_passes_test(es_miembro2)
def inicio_op(request):
    if request.method == 'GET':
        return render(request, 'inicio_op.html', context={})


#formulario de la reserva
@login_required
@user_passes_test(es_miembro)
def reserva_view(request):
    user = request.user   
    if request.method == 'POST':
        form = ReservaForm(user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('inicio')
    else:
        form = ReservaForm(user)
    
    return render(request, 'reservas.html', {'form':form})

#Creacion de reserva por el lado de productor#
class ReservaCreate(UserPassesTestMixin,CreateView):
    
    model= Reserva
    form_class = ReservaForm
    template_name = 'reservas.html'
    success_url = reverse_lazy('inicio')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        
        return kwargs  


    def get(self, request, *args, **kwargs):
        
        kwargs = self.get_form_kwargs()
        
        form = ReservaForm(**kwargs)
        args = {'form': form }

        return render(request, self.template_name, args)
    
    
    def test_func(self):
        return self.request.user.groups.filter(name='Productores').exists()
  
    def handle_no_permission(self):
        return HttpResponse('Usuario sin permisos, favor contactar al administrador')

#Listado de reservas vista del productor#
class ReservaList(UserPassesTestMixin,ListView):
    
    model = Reserva
    template_name = 'reservas_lista.html'
    context_object_name = 'reservas_realizadas'
    
    #Filtro para que solo se muestren las reservas del productor logueado#
    def get_queryset(self):
        
        reservas_realizadas = Reserva.objects.filter(productor__user_id=self.request.user.id)
        print(reservas_realizadas)
        print(self.request.user.id)
        return reservas_realizadas
        
    def test_func(self):
        return self.request.user.groups.filter(name='Productores').exists()
  
    def handle_no_permission(self):
        return HttpResponse('Usuario sin permisos, favor contactar al administrador')

#Informacion del productor logueado#
class DatosUsuarioList(UserPassesTestMixin,ListView):

    model = Productor
    template_name = 'datos_usuario.html'
    context_object_name = 'datos_usuario_logeado'

    def get_queryset(self):
                
        datos_usuario_logeado = Productor.objects.filter(user=self.request.user)
        return datos_usuario_logeado


    def test_func(self):
        return self.request.user.groups.filter(name='Productores').exists()
  
    def handle_no_permission(self):
        return HttpResponse('Has sido expulsado del sitio')

#Informacion del operador logueado#
class DatosUsuarioOperadorList(UserPassesTestMixin,ListView):

    model = Productor
    template_name = 'datos_usuario_operador.html'
    context_object_name = 'datos_usuario_logeado'

    def get_queryset(self):
 
        user = User.objects.filter(id = self.request.user.id)
        return user
        
            
    def test_func(self):
        return self.request.user.groups.filter(name='Operadores').exists()
  
    def handle_no_permission(self):
        return HttpResponse('Has sido expulsado del sitio')

#Creacion de reserva por el operador#
class ReservaOperCreate(UserPassesTestMixin,CreateView):
    model= Reserva
    form_class = ReservaOperForm
    template_name = 'reservas_op.html'
    success_url = reverse_lazy('reserva_op_pendientes')
  
    def test_func(self):
        return self.request.user.groups.filter(name='Operadores').exists()
  
    def handle_no_permission(self):
        return HttpResponse('Usuario sin permisos, favor contactar al administrador')

#Desplegable para que solo muestre chacras del productor seleccionado#
def cargar_chacras(request):
    productor_id = request.GET.get('productor')
    chacras = Chacra.objects.filter(productor_id=productor_id).exclude(estado='Inactivo')
    return render(request, 'chacras_dropdown.html', {'chacras': chacras})

#Listado de reservas pendientes para el operador#
class ReservaOperPendList(UserPassesTestMixin,ListView):
	
    model = Reserva
	
    template_name = 'reservas_op_lista.html'
	
    paginate_by = 10
    
    queryset = Reserva.objects.filter(estado='Pendiente')

    def test_func(self):
        return self.request.user.groups.filter(name='Operadores').exists()
  
    def handle_no_permission(self):
        return HttpResponse('Usuario sin permisos, favor contactar al administrador')

#Listado de reservas asignadas para el operador#
class ReservaOperAsigList(ListView):
	
    model = Reserva
	
    template_name = 'reservas_op_lista asig.html'
	
    paginate_by = 10
    
    queryset = Reserva.objects.filter(estado='Asignado')

    def test_func(self):
        return self.request.user.groups.filter(name='Productores').exists()
  
    def handle_no_permission(self):
        return HttpResponse('You have been denied')

#Actualizacion de datos de la reserva#
class ReservaUpdate(UserPassesTestMixin,UpdateView):
    model = Reserva
    form_class = ReservaOperPreEstado
    template_name = 'reservas_op.html'
    success_url = reverse_lazy('reserva_op_pendientes')

    def test_func(self):
        return self.request.user.groups.filter(name='Operadores').exists()
  
    def handle_no_permission(self):
        return HttpResponse('Usuario sin permisos, favor contactar al administrador')

#Actualizacion de estado de la reserva#
class ReservaUpdateEstado(UserPassesTestMixin,UpdateView):
    model = Reserva
    form_class = ReservaOperFormUpdate
    template_name = 'reservas_op_update.html'
    success_url = reverse_lazy('reserva_op_asignadas')

    def test_func(self):
        return self.request.user.groups.filter(name='Operadores').exists()
  
    def handle_no_permission(self):
        return HttpResponse('Usuario sin permisos, favor contactar al administrador')

#Actualizacion de estado de la reserva a entregado#
class ReservaOperFinList(UserPassesTestMixin,ListView):
	
    model = Reserva    	
    template_name = 'reservas_op_lista fin.html'
    reservas = Reserva.objects.all()
    queryset = reservas.filter(estado='Entregado')

    def test_func(self):
        return self.request.user.groups.filter(name='Operadores').exists()
  
    def handle_no_permission(self):
        return HttpResponse('Usuario sin permisos, favor contactar al administrador')

#Actualizacion de estado de la reserva a rechazado#
class ReservaOperRechList(UserPassesTestMixin,ListView):
	
    model = Reserva    	
    template_name = 'reservas_op_lista_rech.html'
    reservas = Reserva.objects.all()
    queryset = reservas.filter(estado='Rechazado')

    def test_func(self):
        return self.request.user.groups.filter(name='Operadores').exists()
  
    def handle_no_permission(self):
        return HttpResponse('Usuario sin permisos, favor contactar al administrador')