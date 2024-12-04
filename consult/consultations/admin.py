from django.contrib import admin

from consult.consultations.models import Execution, FrameworkTheme, Theme

admin.site.register(Execution)
admin.site.register(Theme)
admin.site.register(FrameworkTheme)
