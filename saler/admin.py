from django.contrib import admin
from . import models
# Register your models here.


class AddSkillCategoryAdmin(admin.ModelAdmin):
    list_display = ("category",)
    
class SkillsAdmin(admin.ModelAdmin):
    list_display=("title","tutor")  
    
    
class BookingAdmin(admin.ModelAdmin):
    list_display=("student","duration")
    
class BookingPaymentsAdmin(admin.ModelAdmin):
    list_display=("id","payment_method","amount","date","confirmation_code","payment_status_description","booking")

class MainFinanceAccountAdmin(admin.ModelAdmin):
    list_display=("id","last_deposit_amount","last_withdraw","last_deposit","amount_balance","get_transaction_type_display",)
 
 
class TutorFinanceAccountAdmin(admin.ModelAdmin):
    list_display=("id","last_deposit_amount","last_withdraw","last_deposit","amount_balance")   

class WithdrawalRequestAdmin(admin.ModelAdmin):
    list_display = ("id","date_initiated","amount","status")   
    
# class TotorAccountAdmin(admin.ModelAdmin):
#     list_display=("tutor","balance","last_deposit_amount")
    
admin.site.register(models.SkillCategory,AddSkillCategoryAdmin)
admin.site.register(models.Skill,SkillsAdmin)
admin.site.register(models.Booking,BookingAdmin)
admin.site.register(models.BookingPayments,BookingPaymentsAdmin)
# admin.site.register(models.TutorAccount,TotorAccountAdmin)

admin.site.register(models.TutorFinanceAccount,TutorFinanceAccountAdmin)
admin.site.register(models.MainFinanceAccount,MainFinanceAccountAdmin)
admin.site.register(models.WithdrawFunds,WithdrawalRequestAdmin)
admin.site.register(models.Course)
# admin.site.register(m)
