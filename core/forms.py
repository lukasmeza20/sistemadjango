from django import forms
from django.forms import ModelForm, fields, Form
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Producto, PerfilUsuario

class ProductoForm(ModelForm):
    class Meta:
        model = Producto
        fields = ['idprod', 'nomprod', 'descprod', 'precio', 'imagen']

class IniciarSesionForm(Form):
    username = forms.CharField(label="Correo", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        fields = ['username', 'password']

class RegistrarUsuarioForm(UserCreationForm):
    rut = forms.CharField(max_length=20, required=True, label="Rut")
    tipousu = forms.CharField(max_length=50, required=True, label="Tipo de usuario", widget=forms.TextInput(attrs={'readonly': 'readonly'}), initial='Cliente')
    dirusu = forms.CharField(max_length=300, required=True, label="Dirección")
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'tipousu', 'rut', 'dirusu']

class PerfilUsuarioForm(Form):
    rut = forms.CharField(max_length=20, required=False, label="Rut", widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=150, required=True, label="Nombres", widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=150, required=True, label="Apellidos", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(max_length=254, required=True, label="Correo", widget=forms.TextInput(attrs={'class': 'form-control'}))
    dirusu = forms.CharField(max_length=300, required=False, label="Dirección", widget=forms.TextInput(attrs={'class': 'form-control'}))
    tipousu = forms.CharField(max_length=50, required=True, label="Tipo de usuario", widget=forms.TextInput(attrs={'class': 'form-control'}))
    

    class Meta:
        fields = '__all__'

class IngresarSolicitudServicioForm(Form):
    TIPO_SOLICITUD_CHOICES = [
        ('Mantención', 'Mantención'),
        ('Reparación', 'Reparación'),
    ]
    monto = forms.IntegerField(required=False,label="Precio de la visita",initial=25000,widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    tiposol = forms.ChoiceField(choices=TIPO_SOLICITUD_CHOICES,required=True,label="Tipo de solicitud",widget=forms.Select(attrs={'class': 'form-control'}))
    descsol = forms.CharField(max_length=100,required=True,label="Descripción",widget=forms.Textarea(attrs={'class': 'form-control'}))
    fechavisita = forms.DateField(required=True,label="Fecha de la visita",widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    horavisita = forms.TimeField(required=False,label="Hora de la visita",widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}))
    
    class Meta:
        fields = '__all__'