from django.contrib import admin

from .models import Category, ItemType, Material, Enchantment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )
    ordering = ('name', )


@admin.register(ItemType)
class ItemTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ('name', )
    list_filter = ('category', )
    ordering = ('name', 'category')


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )
    filter_horizontal = ('applicable_to',)


@admin.register(Enchantment)
class EnchantmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'max_level')
    search_fields = ('name', )
    filter_horizontal = ('applicable_to', )
