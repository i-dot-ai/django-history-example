"""
URL configuration for consult project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path

from consult.accounts.views import homepage
from consult.api import api
from consult.consultations.views import (
    create_theme,
    delete_theme,
    edit_theme,
    list_themes_for_execution_run,
    edit_themes_for_framework
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", homepage, name="homepage"),
    path(
        "execution/<uuid:execution_id>/",
        list_themes_for_execution_run,
        name="list_themes_for_execution",
    ),
    path("execution/", list_themes_for_execution_run, name="list_themes"),
    path("theme/<uuid:theme_id>/", edit_theme, name="edit_theme"),
    path("delete-theme/<uuid:theme_id>/", delete_theme, name="delete_theme"),
    path("create-theme/<uuid:execution_id>/", create_theme, name="create_theme"),
    path("create-themes-framework/", edit_themes_for_framework, name="create_theme_for_framework"),
    path("edit-themes-framework/<int:framework_id>/", edit_themes_for_framework, name="edit_theme_for_framework"),
    path("api/", api.urls),
]

urlpatterns += [
    path("accounts/", include("django.contrib.auth.urls")),
]
