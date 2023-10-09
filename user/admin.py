from django.contrib import admin
from user.models import MyCustomUser

# Register your models here.

class MyCustomUserAdmin(admin.ModelAdmin):
    readonly_fields = ('groups' , 'user_permissions' )
admin.site.register(MyCustomUser , MyCustomUserAdmin)
