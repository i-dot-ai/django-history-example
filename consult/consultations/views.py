from typing import Optional
from uuid import UUID

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import FrameworkFormSet, ResponseMappingForm, ThemeForm
from .models import Execution, FrameworkTheme, Response, ResponseMapping, Theme
from .pipeline import generate_dummy_framework, generate_mapping

# Excecution & theme views - now superseded by FrameworkTheme approach


def list_themes_for_execution_run(
    request: HttpRequest, execution_id: Optional[UUID] = None
) -> HttpResponse:
    if request.POST:
        execution_id = request.POST.get("execution-run")
        return redirect(reverse("list_themes_for_execution", args=(execution_id,)))
    all_execution_runs = Execution.objects.all()
    if execution_id:
        selected_execution = Execution.objects.get(id=execution_id)
    else:
        selected_execution = Execution.objects.first()  # pick the first as default
    themes = Theme.objects.filter(execution=selected_execution)
    initial_themes_history = selected_execution.get_initial_themes_for_execution()
    return render(
        request,
        "list_themes.html",
        {
            "selected_execution": selected_execution,
            "themes": themes,
            "all_execution_runs": all_execution_runs,
            "initial_themes_history": initial_themes_history,
        },
    )


def edit_theme(request: HttpRequest, theme_id: UUID) -> HttpResponse:
    theme = Theme.objects.get(id=theme_id)
    theme_history = theme.history.all()

    if request.method == "POST":
        form = ThemeForm(request.POST, instance=theme)
        if form.is_valid():
            form.save()
            return redirect(reverse("edit_theme", args=(theme.id,)))
    else:
        form = ThemeForm(instance=theme)

    return render(
        request, "edit_theme.html", {"form": form, "theme": theme, "theme_history": theme_history}
    )


def delete_theme(request: HttpRequest, theme_id: UUID) -> HttpResponse:
    if request.method == "POST":
        theme = Theme.objects.get(id=theme_id)
        theme.delete()
        return redirect(reverse("list_themes"))
    return HttpResponse(status=405)  # Method not allowed


def create_theme(request: HttpRequest, execution_id: UUID) -> HttpResponse:
    if request.method == "POST":
        form = ThemeForm(request.POST)
        if form.is_valid():
            theme = form.save(commit=False)
            theme.execution = Execution.objects.get(id=execution_id)
            theme.save()
            return redirect(reverse("list_themes_for_execution", args=(execution_id,)))
    else:
        form = ThemeForm()

    return render(request, "create_theme.html", {"form": form, "execution_id": execution_id})


# FrameworkTheme views
# Each row of the FrameworkTheme table is a theme belonging to a particular framework.
# Changes to the theme will be recorded with a new framework_id.


def edit_themes_for_framework(
    request: HttpRequest, framework_id: Optional[UUID] = None
) -> HttpResponse:
    all_frameworks = FrameworkTheme.objects.all().order_by("framework_id")
    next_id = FrameworkTheme.get_next_framework_id()
    print(f"next_id: {next_id}")
    if request.method == "POST":
        formset = FrameworkFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                form.instance.pk = None  # Set primary key to None to create new objects
                print(f"form.instance: {form.instance}")
                frameworktheme = form.save(commit=False)
                frameworktheme.framework_id = next_id
                frameworktheme.user = request.user
                frameworktheme.save()
            return redirect(reverse("edit_theme_for_framework", args=(next_id,)))
    else:
        if framework_id:
            formset = FrameworkFormSet(
                queryset=FrameworkTheme.objects.filter(framework_id=framework_id)
            )
        else:
            formset = FrameworkFormSet()
    return render(
        request,
        "edit_framework_themes.html",
        {"form": formset, "framework_id": framework_id, "all_frameworks": all_frameworks},
    )


def show_framework(request: HttpRequest, framework_id: int) -> HttpResponse:
    frameworks = FrameworkTheme.objects.filter(framework_id=framework_id)
    return render(
        request, "show_framework.html", {"frameworks": frameworks, "framework_id": framework_id}
    )


def show_all_frameworks(request: HttpRequest) -> HttpResponse:
    all_frameworks = FrameworkTheme.objects.all().order_by("framework_id")
    return render(request, "show_all_frameworks.html", {"all_frameworks": all_frameworks})


def show_framework_theme(request, framework_theme_id: UUID) -> HttpResponse:
    framework_theme = FrameworkTheme.objects.get(id=framework_theme_id)
    history = framework_theme.get_theme_history()
    return render(
        request,
        "show_framework_theme.html",
        {"framework_theme": framework_theme, "history": history},
    )


# Pipeline views


def run_generate_framework(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        framework_id = generate_dummy_framework()
        return redirect(reverse("show_framework", args=(framework_id,)))
    return render(request, "run_generate_framework.html")


def run_generate_mapping(request: HttpRequest) -> HttpResponse:
    framework_ids = FrameworkTheme.objects.values_list("framework_id", flat=True).distinct()
    if request.method == "POST":
        responses = Response.objects.all()
        framework_id = request.POST.get("framework_id")
        generate_mapping(responses, framework_id)
        # TODO - what to return
    return render(request, "run_generate_mapping.html", {"framework_ids": framework_ids})


# Response mapping - matching up responses to framework themes


def show_response_mapping(request: HttpRequest, response_mapping_id: UUID) -> HttpResponse:
    response_mapping = ResponseMapping.objects.get(id=response_mapping_id)
    response_mapping_history = response_mapping.history.all()
    return render(
        request,
        "show_response_mapping.html",
        {
            "response_mapping": response_mapping,
            "response_mapping_history": response_mapping_history,
        },
    )


def show_all_response_mappings(request: HttpRequest) -> HttpResponse:
    response_mappings = ResponseMapping.objects.all()
    return render(
        request, "show_all_response_mappings.html", {"response_mappings": response_mappings}
    )


def edit_response_mapping(request: HttpRequest, response_mapping_id: UUID) -> HttpResponse:
    response_mapping = ResponseMapping.objects.get(id=response_mapping_id)
    if request.method == "POST":
        form = ResponseMappingForm(request.POST, instance=response_mapping)
        if form.is_valid():
            form.save()
            return redirect(reverse("response_mapping", args=(response_mapping.id,)))
    else:
        form = ResponseMappingForm(instance=response_mapping)
    return render(
        request, "edit_response_mapping.html", {"form": form, "response_mapping": response_mapping}
    )


# Homepage
def homepage(request):
    framework_themes_ids = FrameworkTheme.objects.all().values_list("id", flat=True)
    framework_ids = FrameworkTheme.objects.all().values_list("framework_id", flat=True)
    response_mapping_ids = ResponseMapping.objects.all().values_list("id", flat=True)
    context = {
        "framework_theme_ids": framework_themes_ids,
        "framework_ids": framework_ids,
        "response_mapping_ids": response_mapping_ids,
    }
    return render(request, "homepage.html", context=context)
