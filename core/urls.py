from django.urls import path
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views
from .views import home, administrar_productos, obtener_facturas, tienda, ficha, solicitudes,solicitudes_servicio, historial_ventas,admin_solicitudes,solicitudes_tecnico
from .views import iniciar_sesion, registrar_usuario, cerrar_sesion
from .views import perfil_usuario
from .views import iniciar_pago
from .views import pago_exitoso
from .views import obtener_solicitudes_de_servicio
from .views import actualizar_solicitud_servicio

urlpatterns = [
    path('', home, name="home"),
    path('solicitudes', solicitudes, name="solicitudes"),
    path('solicitudes_servicio', solicitudes_servicio, name="solicitudes_servicio"),
    path('historial/', obtener_facturas, name="compras"),
    path('historial_ventas', historial_ventas, name="historial_ventas"),
    path('admin_solicitudes', admin_solicitudes, name="admin_solicitudes"),
    path('solicitudes_tecnico', solicitudes_tecnico, name="solicitudes_tecnico"),
    path('tienda', tienda, name="tienda"),
    path('administrar_productos/<action>/<id>', administrar_productos, name="administrar_productos"),
    path('ficha/<id>', ficha, name="ficha"),
    path('iniciar_pago/<id>', iniciar_pago, name="iniciar_pago"),
    path('pago_exitoso/', pago_exitoso, name="pago_exitoso"),
    path('iniciar_sesion/', iniciar_sesion, name="iniciar_sesion"),
    path('cerrar_sesion/', cerrar_sesion, name='cerrar_sesion'),
    path('registrar_usuario/', registrar_usuario, name="registrar_usuario"),
    path('password_cambiada/', TemplateView.as_view(template_name='core/password_cambiada.html'), name='password_cambiada'),
    path('cambiar_password/', auth_views.PasswordChangeView.as_view(template_name='core/cambiar_password.html', success_url='/password_cambiada'), name='cambiar_password'),
    path('perfil_usuario/', perfil_usuario, name="perfil_usuario"),
    path('obtener_solicitudes_de_servicio/', obtener_solicitudes_de_servicio, name="obtener_solicitudes_de_servicio"),
    path('modificar/<int:nrosol>/', actualizar_solicitud_servicio, name='modificar'),
]