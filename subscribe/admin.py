from django.contrib import admin
from subscribe.models import EmailVerify,LineInformList
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register your models here.

admin.site.register(EmailVerify)
admin.site.register(LineInformList)




from .models import LineUserInfo

class LineUserInfoInline(admin.StackedInline):
    model = LineUserInfo
    can_delete = False
    verbose_name_plural = 'LineUserInfo'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (LineUserInfoInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
