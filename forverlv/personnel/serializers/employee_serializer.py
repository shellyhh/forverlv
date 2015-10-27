# -*- coding: utf-8 -*-
__author__ = 'Arvin'
from rest_framework import serializers
from personnel.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):

    create_user = serializers.Field(source="create_user.username")

    class Meta:
        model = Employee
        fields = ('employee_id', 'first_name', 'last_name', 'create_user')