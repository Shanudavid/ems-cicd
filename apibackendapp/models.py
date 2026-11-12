from django.db import models
from django.contrib.auth.models import User
# a model is a python class that represents a table in a database.
# Create your models here.

class Department(models.Model):
    DepartmentId=models.AutoField(primary_key=True)
    DepartmentName=models.CharField(max_length=100)
    def __str__(self):
        return self.DepartmentName


class Employee(models.Model):
    EmployeeId=models.AutoField(primary_key=True)
    EmployeeName=models.CharField(max_length=100)
    Designation=models.CharField(max_length=100)
    DateOfJoining=models.DateField()
    DepartmentId=models.ForeignKey(Department,on_delete=models.CASCADE)
    Contact=models.CharField(max_length=15)
    IsActive=models.BooleanField(default=True)
    def __str__(self):
        return self.EmployeeName

class Project(models.Model):
    #for a many to many relationship, we cannot explicitly define 
    # an id field. Django will be referring to the default id field.
    name=models.CharField(max_length=100,unique=True)
    #define a many to many field
    # related name of this relation will be later referred in the serializer
    employees=models.ManyToManyField(Employee,related_name='projects')

    def __str__(self):
        return self.name

class UserDetails(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='user_details')
    phoneno=models.CharField(max_length=15)
    email=models.EmailField()

    def __str__(self):
        return self.user.username
    


