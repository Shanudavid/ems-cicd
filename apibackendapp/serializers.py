from rest_framework import serializers
from.models import Department,Employee,Project,UserDetails
from datetime import date
import re
from django.contrib.auth.models import User,Group
from django.contrib.auth.hashers import make_password

#validation 1: dateOfJoining current date
#validation 2: empolyeeName should ve character, no special character

#validation of dateOfJoining
def date_of_joining_restriction(dateOfJoining):
    today=date.today()
    if dateOfJoining!=today:
        raise serializers.ValidationError("The date of joining must be today")
    return dateOfJoining

#validation for empolyeeName
def name_validation(employeeName):
    if len(employeeName)<3 or not re.match("^[A-Za-z]+$",employeeName):
        raise serializers.ValidationError("Name must be atleast 3 letters and contain \n only alphabetic characters")
    return employeeName

#validation for DepartmentName
def deptname_validation(departmentName):
    if len(departmentName) < 3 or not re.match("^[A-Za-z]+$", departmentName):
        raise serializers.ValidationError("Department name must be at least 3 letters and contain only alphabets")
    return departmentName

#validation for contact 
def contact_validation(contact):
    if not re.match(r'^[0-9]{10}$',contact):
        raise serializers.ValidationError("Contact must contain exactly 10 digits")
    return contact

#validation for designation
def designation_validation(designation):
    if len(designation.strip())<2:
        raise serializers.ValidationError("Designation must contain atlease 2 characters")
    if not re.match(r'[A-Za-z]+$',designation):
        raise serializers.ValidationError("Designation must contain only alphabets")
    return designation

#validation for projectName
def projectName_validation(name):
    if len(name.strip())<3:
        raise serializers.ValidationError("Project name must contain atlease 3 characters")
    return name

#Department serializer
class DepartmentSerializer(serializers.ModelSerializer):
    DepartmentName=serializers.CharField(max_length=200,validators=[deptname_validation])
    class Meta:
        model=Department
        fields='__all__'
#Employee serializer
class EmployeeSerializer(serializers.ModelSerializer):
    Department=DepartmentSerializer(source='DepartmentId',read_only=True)

#adding the validation fields
    DateOfJoining=serializers.DateField(validators=[date_of_joining_restriction])
    EmployeeName=serializers.CharField(max_length=200,validators=[name_validation])
    Contact=serializers.CharField(validators=[contact_validation])
    Designation=serializers.CharField(validators=[designation_validation])
    #show project details
    project_details=serializers.StringRelatedField(source='projects',many=True,read_only=True)
    class Meta:
        model=Employee
        fields=('EmployeeId','EmployeeName','Designation','DateOfJoining','Contact','IsActive',
                'DepartmentId','Department','project_details')

#PRoject Serializer
class ProjectSerializer(serializers.ModelSerializer):
    #employees-->get the data for employee_details from the employees field of the project model
    employee_details=EmployeeSerializer(source='employees',required=False,many=True,read_only=True)

    #adding projectName validation
    name=serializers.CharField(validators=[projectName_validation])

    class Meta:
        model=Project
        fields=('id','name','employees','employee_details')
        

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
       model=UserDetails
       fields='__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id','username')

# receives the registration data, validates it and hashes the password, creates the user
#and assign the user to a group and finally returns the created user
class SignupSerializer(serializers.ModelSerializer):
    group_name=serializers.CharField(write_only=True,required=False)
    def create(self,validated_data):
        group_name=validated_data.pop("group_name",None)

        #Hash the password
        validated_data["password"]=make_password(validated_data.get("password"))

        #create the user
        user=super(SignupSerializer,self).create(validated_data)

        if group_name:
            group,createed=Group.objects.get_or_create(name=group_name)
            user.groups.add(group)
        return user
    class Meta:
        model=User
        fields=['username','password','group_name']

class LoginSerializer(serializers.ModelSerializer):
    #field to get username from user
    username=serializers.CharField()
    #field to get password from user
    password=serializers.CharField(write_only=True)

    class Meta:
        model=User
        fields=['username','password'
        
        ]
        


        
      
