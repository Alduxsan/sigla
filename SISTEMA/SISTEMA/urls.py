
from django.contrib import admin
from django.urls import path
from gestor import urls, views
from django.conf.urls import url, include

from django.contrib.auth.decorators import login_required


from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from gestor import views
from django.views.generic import RedirectView



#Add URL maps to redirect the base URL to our application
from django.views.generic import RedirectView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # path('',RedirectView.as_view(url='', permanent=False)),
    path('inicio/', views.inicio, name='inicio'),
    path('inicio_op/', views.inicio_op, name='inicio_op'),
    path('reservas/nuevo', login_required(views.ReservaCreate.as_view()), name='reserva'),
    path('reservas/listar',login_required(views.ReservaList.as_view()), name='reserva_listar'),    
    url('productor/nuevo', views.ProductorCreate.as_view(), name='productor_crear'),
    url('productor/listar/', login_required (views.ProductorList.as_view()), name='productor_listar'),
    url(r'^editar/(?P<pk>\d+)/$', login_required(views.ProductorUpdate.as_view()), name='productor_editar'),
    #url(r'^productoreliminar/(?P<pk>\d+)/$', views.ProductorDelete.as_view(), name='productor_eliminar'),
    url('chacra/nuevo',  login_required (views.ChacraCreate.as_view()), name='chacra_crear'),
    url('chacra/listar',  login_required(views.ChacraList.as_view()), name='chacra_listar'),
    url(r'^modificar/(?P<pk>\d+)/$', login_required (views.ChacraUpdate.as_view()), name='chacra_editar'),
    #url(r'^eliminar/(?P<pk>\d+)/$', views.ChacraDelete.as_view(), name='chacra_eliminar'),
    url('usuario/nuevo',  views.usuario_crear, name='usuario_crear'),
    url('usuario/listar',  login_required(views.UserList.as_view()), name='usuario_listar'),
    url(r'^usuarioeditar/(?P<pk>\d+)/$',  login_required(views.UserUpdate.as_view()), name='usuario_editar'),
    url('transportista/nuevo', login_required(views.TransportistaCreate.as_view()), name='transportista_crear'),
    url('transportista/listar', login_required(views.TransportistaList.as_view()), name='transportista_listar'),
    url(r'^alterar/(?P<pk>\d+)/$', login_required(views.TransportistaUpdate.as_view()), name='transportista_editar'),
    #url(r'^transportistaeliminar/(?P<pk>\d+)/$', views.TransportistaDelete.as_view(), name='transportista_eliminar'),
    url('camion/nuevo',  login_required(views.CamionCreate.as_view()), name='camion_crear'),
    url('camion/listar',  login_required(views.CamionList.as_view()), name='camion_listar'),
    url(r'^cambiar/(?P<pk>\d+)/$',  login_required(views.CamionUpdate.as_view()), name='camion_editar'),
    #url(r'^camioneliminar/(?P<pk>\d+)/$', views.CamionDelete.as_view(), name='camion_eliminar'),
    url('planta/nuevo',  login_required(views.PlantaCreate.as_view()), name='planta_crear'),
    url('planta/listar',  login_required(views.PlantaList.as_view()), name='planta_listar'),
    url(r'^plantaeditar/(?P<pk>\d+)/$',  login_required(views.PlantaUpdate.as_view()), name='planta_editar'),
    #url(r'^plantaeliminar/(?P<pk>\d+)/$', views.PlantaDelete.as_view(), name='planta_eliminar'),
    url('producto/listar',  login_required(views.ProductList.as_view()), name='producto_listar'),
    url('producto/nuevo', views.ProductCreate.as_view(), name='producto_crear'),
    url(r'^productoeditar/(?P<pk>\d+)/$',  login_required(views.ProductUpdate.as_view()), name='producto_editar'),
    #url(r'^productoeliminar/(?P<pk>\d+)/$', views.ProductDelete.as_view(), name='producto_eliminar'),
    path('ajax/cargar-chacras/', views.cargar_chacras, name='ajax_cargar_chacras'),

]


urlpatterns += [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('gestor.urls')),
    path('gestor/', include('gestor.urls')),
    ]
    


from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)