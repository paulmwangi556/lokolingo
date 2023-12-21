from django.contrib import admin
from . import models
# Register your models here.


class AddSkillCategoryAdmin(admin.ModelAdmin):
    list_display = ("category",)
    
class SkillsAdmin(admin.ModelAdmin):
    list_display=("title","tutor")  
    
    
class BookingAdmin(admin.ModelAdmin):
    list_display=("tutor","student")
    
class BookingPaymentsAdmin(admin.ModelAdmin):
    list_display=("id","reference","amount","date","session")
    
class TotorAccountAdmin(admin.ModelAdmin):
    list_display=("tutor","balance","last_deposit_amount")
    
admin.site.register(models.SkillCategory,AddSkillCategoryAdmin)
admin.site.register(models.Skill,SkillsAdmin)
admin.site.register(models.Booking,BookingAdmin)
admin.site.register(models.BookingPayments)
admin.site.register(models.TutorAccount,TotorAccountAdmin)
