# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import public.auth.base
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Create Time', null=True, editable=False, blank=True)),
                ('delete_time', models.DateTimeField(verbose_name='Delete Time', null=True, editable=False, blank=True)),
                ('update_time', models.DateTimeField(verbose_name='Update Time', null=True, editable=False, blank=True)),
                ('create_user', models.CharField(verbose_name='Create User', max_length=30, null=True, editable=False, blank=True)),
                ('delete_user', models.CharField(verbose_name='Delete User', max_length=30, null=True, editable=False, blank=True)),
                ('update_user', models.CharField(verbose_name='Update User', max_length=30, null=True, editable=False, blank=True)),
                ('obj_status', models.SmallIntegerField(default=0, verbose_name='Object Status', null=True, editable=False, blank=True)),
                ('username', models.CharField(unique=True, max_length=30, verbose_name='User Name')),
                ('email', models.EmailField(max_length=254, verbose_name='email address', blank=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined', editable=False)),
            ],
            options={
                'default_permissions': ('browser', 'add', 'change', 'delete'),
                'verbose_name': 'User',
                'verbose_name_plural': 'User',
                'permissions': (('modeladd_user', 'Can ModelAdd User'), ('modeldelete_user', 'Can ModelDelete User'), ('modeledit_user', 'Can ModelEdit User')),
            },
            managers=[
                ('objects', public.auth.base.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
            ],
            options={
                'default_permissions': ('browser', 'add', 'change', 'delete'),
                'verbose_name': 'Group',
                'proxy': True,
                'verbose_name_plural': 'Group',
            },
            bases=('auth.group',),
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
        ),
    ]
