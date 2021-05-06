from django.contrib import admin
from .models import Destination
from .models import UserList,memberdirectory,DirectoryMembers
from import_export.admin import ImportExportModelAdmin

# Register your models here.

class UserListAdmin(ImportExportModelAdmin):
    list_display = ('name','email','coupon','is_superuser')





admin.site.register(Destination)

admin.site.register(memberdirectory)

admin.site.register(DirectoryMembers)

admin.site.register(UserList)


