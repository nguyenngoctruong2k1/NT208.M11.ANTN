# Generated by Django 3.2.8 on 2021-11-03 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myproject', '0006_alter_tailieu_mota'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monhoc',
            name='MoTa',
            field=models.TextField(),
        ),
    ]
