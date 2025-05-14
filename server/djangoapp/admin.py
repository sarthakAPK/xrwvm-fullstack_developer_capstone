from django.contrib import admin
from .models import CarMake, CarModel

class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1
    fields = ('name', 'type', 'year', 'price', 'dealer_id')
    readonly_fields = ('created_at', 'updated_at')
    show_change_link = True

@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    list_display = ('name', 'founded_year', 'headquarters', 'website_link')
    list_filter = ('founded_year',)
    search_fields = ('name', 'headquarters', 'description')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description')
        }),
        ('Company Details', {
            'fields': ('founded_year', 'headquarters', 'website'),
            'classes': ('collapse',)
        }),
    )
    
    def website_link(self, obj):
        from django.utils.html import format_html
        return format_html('<a href="{0}">{0}</a>', obj.website) if obj.website else '-'
    website_link.short_description = 'Website'

@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'car_make', 'year', 'type', 'price_display', 'dealer_id')
    list_filter = ('car_make', 'type', 'year', 'created_at')
    search_fields = ('name', 'car_make__name', 'dealer_id')
    list_select_related = ('car_make',)
    date_hierarchy = 'created_at'
    ordering = ('-year', 'car_make__name', 'name')
    fieldsets = (
        ('Identification', {
            'fields': ('car_make', 'name', 'dealer_id')
        }),
        ('Specifications', {
            'fields': ('type', 'year', 'engine', 'trim_level', 'color')
        }),
        ('Metrics', {
            'fields': ('mileage', 'price'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
    
    def full_name(self, obj):
        return f"{obj.car_make} {obj.name}"
    full_name.short_description = 'Vehicle'
    full_name.admin_order_field = 'name'
    
    def price_display(self, obj):
        return f"${obj.price:,.2f}" if obj.price else '-'
    price_display.short_description = 'Price'