# Generated by Django 5.0.4 on 2024-05-17 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfilusuario',
            name='tipousu',
            field=models.CharField(choices=[('Cliente', 'Cliente'), ('Tecnico', 'Tecnico'), ('Bodeguero', 'Bodeguero'), ('Administrador', 'Administrador'), ('Superusuario', 'Superusuario'), ('Vendedor', 'Vendedor')], max_length=50),
        ),
    ]