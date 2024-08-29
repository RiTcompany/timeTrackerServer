from django.contrib import admin
from .models import (
    ResultModel, 
    UserModel, 
    ArticleModel, 
    ContactModel, 
    MentorAppointmentModel, 
    CategoryModel,
    EventModel,
    Meta,
    MentorModel
)


from django.contrib.auth.admin import UserAdmin

class CustomAdminUser(UserAdmin):
    fieldsets = (
        (None, { 'fields': ('username', 'password', 'email') }),
        ('Personal Info', { 'fields': (
            'photo', 
            'telegram', 
            'name', 
            'surname', 
            'patronymic',
            'status',
            'about_me',
            'result'
        ) }),
        ('Permissions', { 'fields': ('is_staff', 'is_active', 'is_superuser') })
    )


class CustomAdminMentor(UserAdmin):
    fieldsets = (
        (None, { 'fields': ('username', 'password', 'email') }),
        ('Personal Info', { 'fields': (
            'photo', 
            'telegram',
            'name', 
            'surname', 
            'patronymic',
            'status',
            'about_me',
        ) }),
        ('Permissions', { 'fields': ('is_staff', 'is_active', 'is_superuser') })
    )


admin.site.register(ArticleModel)
admin.site.register(UserModel, CustomAdminUser),
admin.site.register(MentorModel, CustomAdminMentor),
admin.site.register(CategoryModel)
admin.site.register(ContactModel)
admin.site.register(MentorAppointmentModel)
admin.site.register(ResultModel)
admin.site.register(EventModel)
admin.site.register(Meta)