from django.contrib import admin
from.models import Department,Employee,Project,UserDetails
# from rest_framework.authtoken.models import Token
# Register your models here.
admin.site.register(Department)
# admin.site.register(Employee)
admin.site.register(Project)

#Inline class to display Many-to-Many Relationship inside Empolyee Admin

class ProjectInline(admin.TabularInline):
    #TabularInline displays the related data in a table-like format
    #This tells Django to use the intermediate(junction) table
    # .through property gives us access to the junction table
    model=Project.employees.through
    #number of empty rows shown in admin for adding new relationships
    extra=1


#customizing Employee admin panel
class EmployeeAdmin(admin.ModelAdmin):
    #This attached the inline to Empolyee admin page
    inlines=[ProjectInline]

#Register Employee model with the customized admin class
admin.site.register(Employee,EmployeeAdmin)
# admin.site.register(Token)
admin.site.register(UserDetails)