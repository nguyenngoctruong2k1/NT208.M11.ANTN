# Generated by Django 3.2.8 on 2021-11-25 16:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myproject', '0043_thongbao'),
    ]

    operations = [
        migrations.RenameField(
            model_name='thongbao',
            old_name='KiemDuyet',
            new_name='Xem',
        ),
    ]