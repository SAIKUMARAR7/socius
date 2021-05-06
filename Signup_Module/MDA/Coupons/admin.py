from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Coupon_SU


class SuperUserAdmin(UserAdmin):
    list_display = ('code', 'category', 'valid_from', 'valid_till')
    search_fields = ('category', )
    readonly_fields = ('valid_from', 'valid_till')

    ordering = ('code',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register((Coupon_SU))