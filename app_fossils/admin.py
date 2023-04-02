from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import DBSpecies, DBFossil

admin.site.register(DBSpecies)

def sell(modeladmin, request, queryset):
    queryset.update(fossil_status="Sold")
sell.short_description = "Sell selected fossils"

class DBFossilAdmin(admin.ModelAdmin):
    list_display = ('fossil_name', 'fossil_species', 'fossil_owner', 'fossil_status', 'fossil_age_mln')
    list_filter = ('fossil_status', 'fossil_species__species_name')
    actions = [sell]
admin.site.register(DBFossil, DBFossilAdmin)

def sell(modeladmin, request, queryset):
    queryset.update(fossil_status="Sold")
sell.short_description = "Sell selected fossils"

class CustomUserAdmin(UserAdmin):
    ordering = ('-last_login',)
    list_display = (
        'id',
        'is_active',        
        'usr',      
        'email',
        'additional_email',
        'species',
        'fossils',
        'last_login',
        'website',       
        )

    def id(self, obj):
        return obj.id
    
    def is_active(self, obj):
        return obj.is_active

    def usr(self, obj):
        return obj.username
    
    def email(self, obj):
        return obj.email
    
    def additional_email(self, obj):
        return obj.profile.user_additional_email
       
    def species(self, obj):
        return obj.species_owner.count()
    
    def fossils(self, obj):
        return obj.fossil_owner.count()
    
    def last_login(self, obj):
        return obj.last_login    

    def website(self, obj):
        return obj.profile.user_website

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

