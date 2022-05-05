from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


class UserAdmin(BaseUserAdmin):
    """add field to admin form"""

    fieldsets = (
        *BaseUserAdmin.fieldsets,  # original form fieldsets
        (  # new fieldsets
            "Custom Fields",  # group heading
            {
                "fields": (
                    "about",
                    "country",
                    "image",
                ),
            },
        ),
    )


admin.site.register(User, UserAdmin)
