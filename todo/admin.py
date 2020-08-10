from django.contrib import admin
from .models import Todo


# since in our Todo Model we have a filed called created what is not editable that's why django does not show in the
#  admin panel but we just want to see it only, that is why the below class created what is all most a constant with
#  the field name inside the parenthesis
class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)


admin.site.register(Todo, TodoAdmin)
