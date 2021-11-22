# -*- coding: utf-8 -*-
from django.contrib.postgres.operations import UnaccentExtension
from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('myproject', '0034_monhoc_soluongtl'),
    ]

    operations = [
        UnaccentExtension()
    ]