from django.contrib import admin
from .models import UserDetail, Slider, Contact, Cart,TutorRating
from saler.models import Product, ProductSize, SalerDetail, category, dow, SellerSlider, MyCart, WholeSaleProduct, Orders, trend,WholeSaleProductOrders

admin.site.site_header = 'LOKOLiNGO | admin panel'


class UserDetailAdmin(admin.ModelAdmin):
    list_display = ("mobile","user")

class TutorRatingAdmin(admin.ModelAdmin):
    list_display = ("tutor","student","rating","review","date_added")

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


