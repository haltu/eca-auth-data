# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roledb', '0003_auto_20141028_2133'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attendance',
            old_name='source',
            new_name='data_source',
        ),
        migrations.RenameField(
            model_name='municipality',
            old_name='source',
            new_name='data_source',
        ),
        migrations.RenameField(
            model_name='school',
            old_name='source',
            new_name='data_source',
        ),
        migrations.RenameField(
            model_name='userattribute',
            old_name='source',
            new_name='data_source',
        ),
    ]
