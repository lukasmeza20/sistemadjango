# Generated by Django 5.0.1 on 2024-04-07 19:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AnwoStockProducto',
            fields=[
                ('nroserieanwo', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('nomprodanwo', models.CharField(max_length=100)),
                ('precioanwo', models.IntegerField()),
                ('reservado', models.CharField(choices=[('S', 'Reservado'), ('N', 'No reservado')], max_length=1)),
            ],
            options={
                'db_table': 'AnwoStockProducto',
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('idprod', models.IntegerField(primary_key=True, serialize=False, verbose_name='ID Prod')),
                ('nomprod', models.CharField(max_length=100, verbose_name='Nombre')),
                ('descprod', models.CharField(max_length=300, verbose_name='Descripción')),
                ('precio', models.IntegerField(verbose_name='Precio')),
                ('imagen', models.ImageField(default='sinfoto.jpg', upload_to='images/', verbose_name='Imagen')),
            ],
            options={
                'db_table': 'Producto',
            },
        ),
        migrations.CreateModel(
            name='PerfilUsuario',
            fields=[
                ('rut', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('tipousu', models.CharField(choices=[('Cliente', 'Cliente'), ('Técnico', 'Técnico'), ('Bodeguero', 'Bodeguero'), ('Administrador', 'Administrador'), ('Superusuario', 'Superusuario'), ('Vendedor', 'Vendedor')], max_length=50)),
                ('dirusu', models.CharField(max_length=300)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'PerfilUsuario',
            },
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('nrofac', models.IntegerField(primary_key=True, serialize=False)),
                ('fechafac', models.DateField()),
                ('descfac', models.CharField(max_length=300)),
                ('monto', models.IntegerField()),
                ('rutcli', models.ForeignKey(db_column='rutcli', on_delete=django.db.models.deletion.DO_NOTHING, to='core.perfilusuario')),
                ('idprod', models.ForeignKey(db_column='idprod', on_delete=django.db.models.deletion.DO_NOTHING, to='core.producto')),
            ],
            options={
                'db_table': 'Factura',
            },
        ),
        migrations.CreateModel(
            name='GuiaDespacho',
            fields=[
                ('nrogd', models.IntegerField(primary_key=True, serialize=False)),
                ('estadogd', models.CharField(choices=[('En bodega', 'En bodega'), ('Despachado', 'Despachado'), ('Entregado', 'Entregado')], max_length=50)),
                ('nrofac', models.ForeignKey(db_column='nrofac', on_delete=django.db.models.deletion.DO_NOTHING, to='core.factura')),
                ('idprod', models.ForeignKey(db_column='idprod', on_delete=django.db.models.deletion.DO_NOTHING, to='core.producto')),
            ],
            options={
                'db_table': 'GuiaDespacho',
            },
        ),
        migrations.CreateModel(
            name='SolicitudServicio',
            fields=[
                ('nrosol', models.IntegerField(primary_key=True, serialize=False)),
                ('tiposol', models.CharField(choices=[('Instalación', 'Instalación'), ('Mantención', 'Mantención'), ('Reparación', 'Reparación')], max_length=50)),
                ('fechavisita', models.DateField()),
                ('descsol', models.CharField(max_length=200)),
                ('estadosol', models.CharField(choices=[('Aceptada', 'Aceptada'), ('Modificada', 'Modificada'), ('Cerrada', 'Cerrada'), ('Anulada', 'Anulada')], max_length=50)),
                ('nrofac', models.ForeignKey(db_column='nrofac', on_delete=django.db.models.deletion.DO_NOTHING, to='core.factura')),
                ('ruttec', models.ForeignKey(db_column='ruttec', on_delete=django.db.models.deletion.DO_NOTHING, to='core.perfilusuario')),
            ],
            options={
                'db_table': 'SolicitudServicio',
            },
        ),
        migrations.CreateModel(
            name='StockProducto',
            fields=[
                ('idstock', models.IntegerField(primary_key=True, serialize=False)),
                ('idprod', models.ForeignKey(db_column='idprod', on_delete=django.db.models.deletion.DO_NOTHING, to='core.producto')),
                ('nrofac', models.ForeignKey(blank=True, db_column='nrofac', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.factura')),
            ],
            options={
                'db_table': 'StockProducto',
            },
        ),
    ]