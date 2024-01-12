from django.contrib import admin
from .models import UserDetail, Slider, Contact, Cart,TutorRating
from saler.models import Product, ProductSize, SalerDetail, category, dow, SellerSlider, MyCart, WholeSaleProduct, Orders, trend,WholeSaleProductOrders
from . import models
admin.site.site_header = 'LOKOLiNGO | admin panel'


class UserDetailAdmin(admin.ModelAdmin):
    list_display = ("mobile","user")

class TutorRatingAdmin(admin.ModelAdmin):
    list_display = ("tutor","student","rating","review","date_added")

class TutorDetails(admin.ModelAdmin):
    list_display=("user",)
    
class EventAdmin(admin.ModelAdmin):
    list_display = ("id","day","start_time","end_time",)

admin.site.register(UserDetail,UserDetailAdmin)
admin.site.register(Product)
admin.site.register(ProductSize)
admin.site.register(SalerDetail)
admin.site.register(Slider)
admin.site.register(category)
admin.site.register(dow)
admin.site.register(Contact)
admin.site.register(MyCart)
admin.site.register(Cart)
admin.site.register(TutorRating,TutorRatingAdmin)

admin.site.register(models.TutorUserDetails,TutorDetails)
# admin.site.register(models.CertificateFile)
admin.site.register(models.StudentDetails)
admin.site.register(models.Event,EventAdmin)



