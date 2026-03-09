from django.contrib import admin
from .models import NetworkNode, Contact, Product


class ContactInline(admin.StackedInline):
    model = Contact
    can_delete = False
    # fk_name = 'node'  # можно не указывать, Django найдёт поле автоматически


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_city', 'supplier', 'debt', 'created_at')
    list_filter = ('contact__city',)
    inlines = [ContactInline]
    actions = ['clear_debt']

    def get_city(self, obj):
        # obj.contact - обратная связь OneToOne
        return obj.contact.city if obj.contact else '-'
    get_city.short_description = 'Город'
    get_city.admin_order_field = 'contact__city'

    def clear_debt(self, request, queryset):
        updated = queryset.update(debt=0)
        self.message_user(request, f"Задолженность обнулена у {updated} объектов.")
    clear_debt.short_description = "Очистить задолженность у выбранных объектов"


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('email', 'country', 'city', 'street', 'house_number', 'node')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'release_date')