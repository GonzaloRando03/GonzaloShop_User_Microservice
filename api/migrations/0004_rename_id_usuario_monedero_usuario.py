# Generated by Django 4.1.4 on 2022-12-22 12:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_monedero_id_usuario'),
    ]

    operations = [
        migrations.RenameField(
            model_name='monedero',
            old_name='id_usuario',
            new_name='usuario',
        ),
    ]