from django.contrib import admin
from personnel.models import Employee, Department, Position
# Register your models here.
admin.site.register(Employee, Employee.Admin)
admin.site.register(Department, Department.Admin)
admin.site.register(Position, Position.Admin)