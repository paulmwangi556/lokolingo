from django.contrib import admin
from .models import discountCode
# Register your models here.
class discountAdmin(admin.ModelAdmin):
	list_display = ['code','valid_from','valid_to','discounts','active']
	list_filter = ['active','valid_from','valid_to']
	search_fields = ['code']

admin.site.register(discountCode,discountAdmin)