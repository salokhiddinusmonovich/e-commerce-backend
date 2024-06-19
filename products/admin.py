from django.contrib import admin
from .models import *
from parler.admin import TranslatableAdmin



# admin.site.register(Category)
# admin.site.register(Product)
admin.site.register(Images)
admin.site.register(Comment)

@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    list_display = ['pk']

@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ('name', 'order', 'type')
