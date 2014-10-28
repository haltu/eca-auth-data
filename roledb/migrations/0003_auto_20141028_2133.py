# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roledb', '0002_auto_20141012_0819'),
    ]

    operations = [
        migrations.AddField(
            model_name='municipality',
            name='source',
            field=models.ForeignKey(default=1, to='roledb.Source'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='school',
            name='source',
            field=models.ForeignKey(default=1, to='roledb.Source'),
            preserve_default=False,
        ),
    ]
