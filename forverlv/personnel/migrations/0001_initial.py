# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import personnel.models.department_fields
import django.utils.timezone
import personnel.models.position_fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Create Time', null=True, editable=False, blank=True)),
                ('delete_time', models.DateTimeField(verbose_name='Delete Time', null=True, editable=False, blank=True)),
                ('update_time', models.DateTimeField(verbose_name='Update Time', null=True, editable=False, blank=True)),
                ('create_user', models.CharField(verbose_name='Create User', max_length=30, null=True, editable=False, blank=True)),
                ('delete_user', models.CharField(verbose_name='Delete User', max_length=30, null=True, editable=False, blank=True)),
                ('update_user', models.CharField(verbose_name='Update User', max_length=30, null=True, editable=False, blank=True)),
                ('obj_status', models.SmallIntegerField(default=0, verbose_name='Object Status', null=True, editable=False, blank=True)),
                ('number', models.CharField(unique=True, max_length=30, verbose_name='Department Number')),
                ('name', models.CharField(max_length=30, verbose_name='Department Name')),
                ('parent_department', personnel.models.department_fields.DepartmentForeignKey(related_name='children', verbose_name='Parent Department', blank=True, to='personnel.Department', null=True)),
            ],
            options={
                'default_permissions': ('browser', 'add', 'change', 'delete'),
                'verbose_name': 'Department',
                'verbose_name_plural': 'Department',
                'permissions': (('modeladd_department', 'Can ModelAdd Department'), ('modeldelete_department', 'Can ModelDelete Department'), ('modeledit_department', 'Can ModelEdit Department')),
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Create Time', null=True, editable=False, blank=True)),
                ('delete_time', models.DateTimeField(verbose_name='Delete Time', null=True, editable=False, blank=True)),
                ('update_time', models.DateTimeField(verbose_name='Update Time', null=True, editable=False, blank=True)),
                ('create_user', models.CharField(verbose_name='Create User', max_length=30, null=True, editable=False, blank=True)),
                ('delete_user', models.CharField(verbose_name='Delete User', max_length=30, null=True, editable=False, blank=True)),
                ('update_user', models.CharField(verbose_name='Update User', max_length=30, null=True, editable=False, blank=True)),
                ('obj_status', models.SmallIntegerField(default=0, verbose_name='Object Status', null=True, editable=False, blank=True)),
                ('number', models.CharField(unique=True, max_length=30, verbose_name='Employee Number')),
                ('first_name', models.CharField(help_text='The first name', max_length=30, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=30, verbose_name='Last Name')),
                ('department', personnel.models.department_fields.DepartmentForeignKey(verbose_name='Department', to='personnel.Department')),
            ],
            options={
                'default_permissions': ('browser', 'add', 'change', 'delete'),
                'verbose_name': 'Employee',
                'verbose_name_plural': 'Employee',
                'permissions': (('modeladd_employee', 'Can ModelAdd Employee'), ('modeldelete_employee', 'Can ModelDelete Employee'), ('modeledit_employee', 'Can ModelEdit Employee'), ('adjustdepartment_employee', 'Can AdjustDepartment Employee')),
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Create Time', null=True, editable=False, blank=True)),
                ('delete_time', models.DateTimeField(verbose_name='Delete Time', null=True, editable=False, blank=True)),
                ('update_time', models.DateTimeField(verbose_name='Update Time', null=True, editable=False, blank=True)),
                ('create_user', models.CharField(verbose_name='Create User', max_length=30, null=True, editable=False, blank=True)),
                ('delete_user', models.CharField(verbose_name='Delete User', max_length=30, null=True, editable=False, blank=True)),
                ('update_user', models.CharField(verbose_name='Update User', max_length=30, null=True, editable=False, blank=True)),
                ('obj_status', models.SmallIntegerField(default=0, verbose_name='Object Status', null=True, editable=False, blank=True)),
                ('number', models.CharField(unique=True, max_length=30, verbose_name='Position Number')),
                ('name', models.CharField(max_length=30, verbose_name='Position Name')),
                ('department', personnel.models.department_fields.DepartmentForeignKey(verbose_name='Department', to='personnel.Department')),
                ('parent_position', personnel.models.position_fields.PositionForeignKey(verbose_name='Parent Position', blank=True, to='personnel.Position', null=True)),
            ],
            options={
                'default_permissions': ('browser', 'add', 'change', 'delete'),
                'verbose_name': 'Position',
                'verbose_name_plural': 'Position',
                'permissions': (('modeladd_position', 'Can ModelAdd Position'), ('modeldelete_position', 'Can ModelDelete Position'), ('modeledit_position', 'Can ModelEdit Position')),
            },
        ),
        migrations.AddField(
            model_name='employee',
            name='position',
            field=personnel.models.position_fields.PositionForeignKey(verbose_name='Position', to='personnel.Position'),
        ),
    ]
