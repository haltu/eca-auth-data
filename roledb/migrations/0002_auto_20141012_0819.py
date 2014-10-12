# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roledb', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userattribute',
            old_name='name',
            new_name='attribute',
        ),
    ]
