from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


# Register your models here.
from calc.models import contact_us_model
from calc.models import subscribe_model

class contact_us_model_admin(ImportExportModelAdmin):
    pass

class subscribe_model_admin(ImportExportModelAdmin):
    pass

class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = ('id','username','first_name', 'last_name', 'email')

# class UserAdmin(ExportMixin, UserAdmin):
#     resource_class = UserResource
#     pass

class UserAdmin(ImportExportModelAdmin):
    list_display = ('id','username','first_name', 'last_name', 'email')
    # list_filter = ('created_at',)
    resource_class = UserResource
    pass



admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(contact_us_model, contact_us_model_admin)
admin.site.register(subscribe_model, subscribe_model_admin)

