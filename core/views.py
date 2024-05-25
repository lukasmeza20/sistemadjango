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
    datos_productos = []

    with connection.cursor() as cursor:
        cursor.execute("EXEC SP_OBTENER_STOCK ")
        columnas = [col[0] for col in cursor.description]
        productos = [dict(zip(columnas, row)) for row in cursor.fetchall()]
    
    for producto in productos:
        datos_producto = {
            'idprod': producto['idprod'],
            'nomprod': producto['nomprod'],
            'descprod': producto['descprod'],
            'precio': producto['precio'],
            'imagen': producto['imagen'],
            'cantidad': producto['cantidad'],
            'disponibilidad': producto['disponibilidad'],
        }
        datos_productos.append(datos_producto)

    data = {
        'datos_productos': datos_productos,
    }

    return render(request, "core/tienda.html", data)


#https://www.transbankdevelopers.cl/documentacion/como_empezar#como-empezar
#https://www.transbankdevelopers.cl/documentacion/como_empezar#codigos-de-comercio
#https://www.transbankdevelopers.cl/referencia/webpay

# Tipo de tarjeta   Detalle                        Resultado
#----------------   -----------------------------  ------------------------------
# VISA              4051885600446623
#                   CVV 123
#                   cualquier fecha de expiración  Genera transacciones aprobadas.
# AMEX              3700 0000 0002 032
#                   CVV 1234
#                   cualquier fecha de expiración  Genera transacciones aprobadas.
# MASTERCARD        5186 0595 5959 0568
#                   CVV 123
#                   cualquier fecha de expiración  Genera transacciones rechazadas.
# Redcompra         4051 8842 3993 7763            Genera transacciones aprobadas (para operaciones que permiten débito Redcompra y prepago)
# Redcompra         4511 3466 6003 7060            Genera transacciones aprobadas (para operaciones que permiten débito Redcompra y prepago)
# Redcompra         5186 0085 4123 3829            Genera transacciones rechazadas (para operaciones que permiten débito Redcompra y prepago)


@csrf_exempt
def ficha(request, id):

    dolar = obtener_valor_usd()
    prod = Producto.objects.get(idprod = id)
    precio_convertido = prod.precio * dolar 

    cantidad_facturas = Factura.objects.filter(idprod=id).count()
    data = {"mesg": "", "producto": None,"precio_convertido":precio_convertido ,"cantidad_facturas":cantidad_facturas}

    # Cuando el usuario hace clic en el boton COMPRAR, se ejecuta el METODO POST del
    # formulario de ficha.html, con lo cual se redirecciona la página para que
    # llegue a esta VISTA llamada "FICHA". A continuacion se verifica que sea un POST 
    # y se valida que se trate de un usuario autenticado que no sea de estaff, 
    # es decir, se comprueba que la compra sea realizada por un CLIENTE REGISTRADO.
    # Si se tata de un CLIENTE REGISTRADO, se redirecciona a la vista "iniciar_pago"
    if request.method == "POST":
        if request.user.is_authenticated and not request.user.is_staff:
            # data["mesg"] = "¡Función no disponible hasta programar WEBPAY de TRANSBANK!"
            # iniciar_pago()
            return redirect(iniciar_pago, id)
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

def obtener_valor_usd():
    url = 'https://api.exchangerate-api.com/v4/latest/CLP'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            datos = response.json()
            valor_usd = datos['rates']['USD']
            return valor_usd
    except:
        pass
    return 0

@csrf_exempt
def iniciar_pago(request, id):

    # Esta es la implementacion de la VISTA iniciar_pago, que tiene la responsabilidad
    # de iniciar el pago, por medio de WebPay. Lo primero que hace es seleccionar un 
    # número de orden de compra, para poder así, identificar a la propia compra.
    # Como esta tienda no maneja, en realidad no tiene el concepto de "orden de compra"
    # pero se indica igual
    print("Webpay Plus Transaction.create")
    buy_order = str(random.randrange(1000000, 99999999))
    session_id = request.user.username
    amount = Producto.objects.get(idprod=id).precio
    return_url = 'http://127.0.0.1:8000/pago_exitoso/'

    # response = Transaction.create(buy_order, session_id, amount, return_url)
    commercecode = "597055555532"
    apikey = "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C"

    tx = Transaction(options=WebpayOptions(commerce_code=commercecode, api_key=apikey, integration_type="TEST"))
    response = tx.create(buy_order, session_id, amount, return_url)
    print(response['token'])

    perfil = PerfilUsuario.objects.get(user=request.user)
    form = PerfilUsuarioForm()

    context = {
        "buy_order": buy_order,
        "session_id": session_id,
        "amount": amount,
        "return_url": return_url,
        "response": response,
        "token_ws": response['token'],
        "url_tbk": response['url'],
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "email": request.user.email,
        "rut": perfil.rut,
        "dirusu": perfil.dirusu,
    }

    return render(request, "core/iniciar_pago.html", context)

@csrf_exempt
def pago_exitoso(request):

    if request.method == "GET":
        token = request.GET.get("token_ws")
        print("commit for token_ws: {}".format(token))
        commercecode = "597055555532"
        apikey = "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C"
        tx = Transaction(options=WebpayOptions(commerce_code=commercecode, api_key=apikey, integration_type="TEST"))
        response = tx.commit(token=token)
        print("response: {}".format(response))

        user = User.objects.get(username=response['session_id'])
        perfil = PerfilUsuario.objects.get(user=user)
        form = PerfilUsuarioForm()

        context = {
            "buy_order": response['buy_order'],
            "session_id": response['session_id'],
            "amount": response['amount'],
            "response": response,
            "token_ws": token,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "rut": perfil.rut,
            "dirusu": perfil.dirusu,
            "response_code": response['response_code']
        }

        return render(request, "core/pago_exitoso.html", context)
    else:
        return redirect(home)


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
    if(perfil.tipousu == 'Cliente' or perfil.tipousu == 'Tecnico' or perfil.tipousu == 'Vendedor'):
        form.fields['tipousu'].initial = perfil.tipousu
        form.fields['tipousu'].disabled = True
    form.fields['tipousu'].initial = perfil.tipousu
    form.fields['dirusu'].initial = perfil.dirusu
    data["form"] = form
    return render(request, "core/perfil_usuario.html", data)


def obtener_facturas(request):
    try:
        perfil = PerfilUsuario.objects.get(user=request.user)
        rut = perfil.rut
        tipousu = perfil.tipousu

        print(f'Usuario: {request.user}, RUT: {rut}, Tipo de Usuario: {tipousu}')  # Depuración

        if request.method == 'GET':
            with connection.cursor() as cursor:
                if tipousu in ['Administrador', 'Superusuario']:
                    cursor.execute("EXEC SP_OBTENER_FACTURAS %s", [None])
                elif tipousu in ['Cliente']:
                    cursor.execute("EXEC SP_OBTENER_FACTURAS %s", [rut])
                else:
                    data = {'list': None, 'tipousu': 'Usuario No Permitido'}
                    return render(request, "core/compras.html", data)
                
                results = cursor.fetchall()
                print(f'Resultados crudos: {results}')  # Depuración

                if not results:
                    print("No se encontraron resultados.")  # Depuración
                    data = {'list': [], 'tipousu': tipousu}
                    return render(request, "core/compras.html", data)

                facturas = []
                for row in results:
                    print(f'Fila: {row}')  # Depuración
                    facturas.append({
                        'nrofac': row[0],
                        'nomcli': row[1],
                        'fechafac': row[2],
                        'descfac': row[3],
                        'monto': row[4],
                        'nrogd': row[5],
                        'estadogd': row[6],
                        'nrosol': row[7],
                        'estadosol': row[8]
                    })

            data = {'list': facturas, 'tipousu': tipousu}
            return render(request, "core/compras.html", data)
    except PerfilUsuario.DoesNotExist:
        data = {'list': None, 'tipousu': 'Usuario No Encontrado'}
        return render(request, "core/compras.html", data)
    except Exception as e:
        data = {'list': None, 'tipousu': f'Error: {str(e)}'}
        return render(request, "core/compras.html", data)

def obtener_solicitudes_de_servicio(request):

    rut = PerfilUsuario.objects.get(user=request.user).rut
    tipousu = PerfilUsuario.objects.get(user=request.user).tipousu
    print(f'Usuario: {request.user}, RUT: {rut}, Tipo de Usuario: {tipousu}')  # Depuración
 
    if request.method == 'GET':
        cursor = connection.cursor()

        # Ejecutar el procedimiento almacenado
        if tipousu in ['Administrador', 'Superusuario'] :
            cursor.execute(f"EXEC SP_OBTENER_SOLICITUDES_DE_SERVICIO 'Todos', ''")
        elif tipousu in ['Cliente', 'Tecnico'] :
            cursor.execute(f"EXEC SP_OBTENER_SOLICITUDES_DE_SERVICIO '{tipousu}', '{rut}'")
        else:
            data = {'lista': None, 'tipousu': 'Usuario No Permitido' }
            return render(request, "core/obtener_solicitudes_de_servicio.html", data)

        # Obtener los resultados
        results = cursor.fetchall()

        # Convertir los resultados en una lista de diccionarios
        solicitudes_de_servicio = []
        for row in results:
            solicitudes_de_servicio.append({
                'nrosol': row[0],
                'nomcli': row[1],
                'tiposol': row[2],
                'fechavisita': row[3],
                'hora': row[4],
                'nomtec': row[5],
                'descser': row[6],
                'estadosol': row[7]
            })

        data = {'lista': solicitudes_de_servicio, 'tipousu': tipousu }

        return render(request, "core/obtener_solicitudes_de_servicio.html", data)