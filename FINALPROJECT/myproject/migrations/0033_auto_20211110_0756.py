# Generated by Django 3.2.8 on 2021-11-10 00:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myproject', '0032_auto_20211110_0248'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='informationuser',
            name='Avatar',
        ),
        migrations.RemoveField(
            model_name='informationuser',
            name='Email',
        ),
        migrations.RemoveField(
            model_name='informationuser',
            name='FullName',
        ),
    ]
