from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from .models import Producto, PerfilUsuario, Factura
from .forms import ProductoForm, IniciarSesionForm
from .forms import RegistrarUsuarioForm, PerfilUsuarioForm
#from .error.transbank_error import TransbankError
from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions
from django.db import connection
import random
import requests

def home(request):
    return render(request, "core/home.html")

def solicitudes(request):
    return render(request, "core/solicitudes.html")

def solicitudes_servicio(request):
    return render(request, "core/solicitudes_servicio.html")

def compras(request):
    return render(request, "core/compras.html")

def historial_ventas(request):
    return render(request, "core/historial_ventas.html")


def admin_solicitudes(request):
    return render(request, "core/admin_solicitudes.html")

def solicitudes_tecnico(request):
    return render(request, "core/solicitudes_tecnico.html")

def iniciar_sesion(request):
    data = {"mesg": "", "form": IniciarSesionForm()}

    if request.method == "POST":
        form = IniciarSesionForm(request.POST)
        if form.is_valid:
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    tipousu = PerfilUsuario.objects.get(user=user).tipousu
                    if tipousu != 'Bodeguero':
                        return redirect(home)
                    else:
                        data["mesg"] = "¡La cuenta o la password no son correctos!"    
                else:
                    data["mesg"] = "¡La cuenta o la password no son correctos!"
            else:
                data["mesg"] = "¡La cuenta o la password no son correctos!"
    return render(request, "core/iniciar_sesion.html", data)

def cerrar_sesion(request):
    logout(request)
    return redirect(home)

def tienda(request):
     # Obtener todos los productos ordenados por su ID
    productos = Producto.objects.all().order_by('idprod')
    
    # Crear una lista para almacenar los datos de cada producto junto con su cantidad de facturas
    datos_productos = []
    
    # Iterar sobre cada producto para obtener la cantidad de facturas asociadas
    for producto in productos:
        cantidad_facturas = Factura.objects.filter(idprod=producto.idprod).count()
        datos_producto = {
            'producto': producto,
            'cantidad_facturas': cantidad_facturas,
        }
        datos_productos.append(datos_producto)
    
    # Crear el diccionario de datos para pasar a la plantilla
    data = {
        'datos_productos': datos_productos,
    }
    
    # Renderizar la plantilla con los datos
    return render(request, "core/tienda.html", data)

@csrf_exempt
def ficha(request, id):
    cantidad_facturas = Factura.objects.filter(idprod=id).count()
    data = {"mesg": "", "producto": None,"cantidad_facturas":cantidad_facturas}

    # Cuando el usuario hace clic en el boton COMPRAR, se ejecuta el METODO POST del
    # formulario de ficha.html, con lo cual se redirecciona la página para que
    # llegue a esta VISTA llamada "FICHA". A continuacion se verifica que sea un POST 
    # y se valida que se trate de un usuario autenticado que no sea de estaff, 
    # es decir, se comprueba que la compra sea realizada por un CLIENTE REGISTRADO.
    # Si se tata de un CLIENTE REGISTRADO, se redirecciona a la vista "iniciar_pago"
    if request.method == "POST":
        if request.user.is_authenticated and not request.user.is_staff:
            data["mesg"] = "¡Función no disponible hasta programar WEBPAY de TRANSBANK!"
            #return redirect(iniciar_pago, id)
        else:
            # Si el usuario que hace la compra no ha iniciado sesión,
            # entonces se le envía un mensaje en la pagina para indicarle
            # que primero debe iniciar sesion antes de comprar
            data["mesg"] = "¡Para poder comprar debe iniciar sesión como cliente!"

    # Si visitamos la URL de FICHA y la pagina no nos envia un METODO POST, 
    # quiere decir que solo debemos fabricar la pagina y devolvera al browser
    # para que se muestren los datos de la FICHA
    data["producto"] = Producto.objects.get(idprod=id)
    return render(request, "core/ficha.html", data )

@csrf_exempt
def administrar_productos(request, action, id):
    if not (request.user.is_authenticated and request.user.is_staff):
        return redirect(home)

    data = {"mesg": "", "form": ProductoForm, "action": action, "id": id, "formsesion": IniciarSesionForm}

    if action == 'ins':
        if request.method == "POST":
            form = ProductoForm(request.POST, request.FILES)
            if form.is_valid:
                try:
                    form.save()
                    data["mesg"] = "¡El producto fue creado correctamente!"
                except:
                    data["mesg"] = "¡No se puede crear dos vehículos con el mismo ID!"

    elif action == 'upd':
        objeto = Producto.objects.get(idprod=id)
        if request.method == "POST":
            form = ProductoForm(data=request.POST, files=request.FILES, instance=objeto)
            if form.is_valid:
                form.save()
                data["mesg"] = "¡El producto fue actualizado correctamente!"
        data["form"] = ProductoForm(instance=objeto)

    elif action == 'del':
        try:
            Producto.objects.get(idprod=id).delete()
            data["mesg"] = "¡El producto fue eliminado correctamente!"
            return redirect(administrar_productos, action='ins', id = '-1')
        except:
            data["mesg"] = "¡El producto ya estaba eliminado!"

    data["list"] = Producto.objects.all().order_by('idprod')
    return render(request, "core/administrar_productos.html", data)

def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistrarUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            rut = request.POST.get("rut")
            tipousu = request.POST.get("tipousu")
            dirusu = request.POST.get("dirusu")
            PerfilUsuario.objects.update_or_create(user=user, rut=rut, tipousu=tipousu, dirusu=dirusu)
            return redirect(iniciar_sesion)
    form = RegistrarUsuarioForm()
    return render(request, "core/registrar_usuario.html", context={'form': form})

def perfil_usuario(request):
    data = {"mesg": "", "form": PerfilUsuarioForm}

    if request.method == 'POST':
        form = PerfilUsuarioForm(request.POST)
        if form.is_valid():
            user = request.user
            user.first_name = request.POST.get("first_name")
            user.last_name = request.POST.get("last_name")
            user.email = request.POST.get("email")
            user.save()
            perfil = PerfilUsuario.objects.get(user=user)
            perfil.rut = request.POST.get("rut")
            perfil.tipousu = request.POST.get("tipousu")
            perfil.dirusu = request.POST.get("dirusu")
            perfil.save()
            data["mesg"] = "¡Sus datos fueron actualizados correctamente!"

    perfil = PerfilUsuario.objects.get(user=request.user)
    form = PerfilUsuarioForm()
    form.fields['first_name'].initial = request.user.first_name
    form.fields['last_name'].initial = request.user.last_name
    form.fields['email'].initial = request.user.email
    form.fields['rut'].initial = perfil.rut
    form.fields['tipousu'].initial = perfil.tipousu
    form.fields['dirusu'].initial = perfil.dirusu
    data["form"] = form
    return render(request, "core/perfil_usuario.html", data)

