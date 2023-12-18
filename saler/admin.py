from django.contrib import admin
from . import models
# Register your models here.


class AddSkillCategoryAdmin(admin.ModelAdmin):
    list_display = ("category",)
    
class SkillsAdmin(admin.ModelAdmin):
    list_display=("title","tutor")  
    
admin.site.register(models.SkillCategory,AddSkillCategoryAdmin)
admin.site.register(models.Skill,SkillsAdmin)
admin.site.register(models.Booking)