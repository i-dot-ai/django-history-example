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

from consult.api import api
from consult.consultations.views import (
    create_theme,
    delete_theme,
    edit_response_mapping,
    edit_theme,
    edit_themes_for_framework,
    homepage,
    list_themes_for_execution_run,
    run_generate_framework,
    run_generate_mapping,
    show_all_frameworks,
    show_all_response_mappings,
    show_framework,
    show_framework_theme,
    show_response_mapping,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", homepage, name="homepage"),
    # Execution runs and themes - potentially these models will no longer be used
    path(
        "execution/<uuid:execution_id>/",
        list_themes_for_execution_run,
        name="list_themes_for_execution",
    ),
    path("execution/", list_themes_for_execution_run, name="list_themes"),
    path("theme/<uuid:theme_id>/", edit_theme, name="edit_theme"),
    path("delete-theme/<uuid:theme_id>/", delete_theme, name="delete_theme"),
    path("create-theme/<uuid:execution_id>/", create_theme, name="create_theme"),
    # Frameworks & themes - each theme generated will be a FrameworkTheme.
    # A "Framework" is a collection of themes - framework_id says which framework it is.
    path("all-frameworks/", show_all_frameworks, name="show_all_frameworks"),
    path("create-themes-framework/", edit_themes_for_framework, name="create_theme_for_framework"),
    path(
        "edit-themes-framework/<int:framework_id>/",
        edit_themes_for_framework,
        name="edit_theme_for_framework",
    ),
    path("theme-framework/<uuid:id>/", show_framework_theme, name="theme-framework"),
    path("framework/<int:framework_id>/", show_framework, name="show_framework"),
    # Run parts of the pipeline
    path("generate-framework/", run_generate_framework, name="generate_framework"),
    path("generate-mapping/", run_generate_mapping, name="generate_mapping"),
    # Response mappings
    path(
        "response-mapping/<uuid:response_mapping_id>/",
        show_response_mapping,
        name="response_mapping",
    ),
    path("all-response-mappings/", show_all_response_mappings, name="all_response_mappings"),
    path(
        "edit-response-mapping/<uuid:response_mapping_id>/",
        edit_response_mapping,
        name="edit_response_mapping",
    ),
    # API
    path("api/", api.urls),
]

urlpatterns += [
    path("accounts/", include("django.contrib.auth.urls")),
]
