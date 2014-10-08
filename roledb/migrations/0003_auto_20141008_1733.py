# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roledb', '0002_attribute_userattribute'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='facebook_id',
        ),
        migrations.RemoveField(
            model_name='user',
            name='linkedin_id',
        ),
        migrations.RemoveField(
            model_name='user',
            name='mepin_id',
        ),
        migrations.RemoveField(
            model_name='user',
            name='twitter_id',
        ),
    ]
