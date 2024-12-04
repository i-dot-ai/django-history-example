from django.contrib import admin

from consult.consultations.models import Execution, Framework, Theme

admin.site.register(Execution)
admin.site.register(Theme)
admin.site.register(Framework)
