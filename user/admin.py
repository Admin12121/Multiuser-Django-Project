from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
class UserModelAdmin(BaseUserAdmin):
  # The fields to be used in displaying the User model.
  # These override the definitions on the base UserModelAdmin
  # that reference specific fields on auth.User.
  list_display = ('id', 'email', 'name', 'tc', 'is_admin')
  list_filter = ('is_admin',)
  fieldsets = (
      ('User Credentials', {'fields': ('email', 'password')}),
      ('Personal info', {'fields': ('name','tc')}),
      ('Permissions', {'fields': ('is_active','is_admin','groups')}),
  )
  # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
  # overrides get_fieldsets to use this attribute when creating a user.
  add_fieldsets = (
      (None, {
          'classes': ('wide',),
          'fields': ('email', 'name' , 'tc', 'password1', 'password2'),
      }),
  )
  search_fields = ( 'name','email',)
  ordering = ('email', 'id')
  filter_horizontal = ()

class UserInfoInline(admin.StackedInline):
    model = User
    can_delete = False
    verbose_name_plural = 'User Profiles'

# Now register the new UserModelAdmin...
admin.site.register(User, UserModelAdmin)
admin.site.register(Tag)
admin.site.register(Product)
admin.site.register( Order)
admin.site.register( Saler)