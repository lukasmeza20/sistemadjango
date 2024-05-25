from django.urls import path
from django.contrib import admin
from .views import producto_create, producto_read, producto_read_all
from .views import producto_update, producto_delete, login, obtener_equipos_en_bodega, obtener_productos, autenticar

urlpatterns = [
    path('producto_create/', producto_create.as_view(), name="producto_create"),
    path('producto_update/', producto_update.as_view(), name="producto_update"),
    path('producto_read/<id>/', producto_read, name="producto_read"),
    path('producto_read_all/', producto_read_all, name='producto_read_all'),
    path('producto_delete/<id>/', producto_delete, name="producto_delete"),
    path('login', login, name='login'),
    path('obtener_equipos_en_bodega', obtener_equipos_en_bodega, name='obtener_equipos_en_bodega'),
    path('obtener_productos', obtener_productos, name='obtener_productos'),
    path('autenticar/<tipousu>/<username>/<password>', autenticar, name="autenticar"),
]
