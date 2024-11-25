from typing import Optional
from uuid import uuid4

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import ThemeForm
from .models import Execution, Theme


def list_themes_for_execution_run(
    request: HttpRequest, execution_id: Optional[uuid4] = None
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
    return render(
        request,
        "list_themes.html",
        {
            "selected_execution": selected_execution,
            "themes": themes,
            "all_execution_runs": all_execution_runs,
        },
    )


def edit_theme(request: HttpRequest, theme_id: uuid4) -> HttpResponse:
    theme = Theme.objects.get(id=theme_id)

    if request.method == "POST":
        form = ThemeForm(request.POST, instance=theme)
        if form.is_valid():
            form.save()
            return redirect(reverse("edit_theme", args=(theme.id,)))
    else:
        form = ThemeForm(instance=theme)

    return render(request, "edit_theme.html", {"form": form, "theme": theme})


def delete_theme(request: HttpRequest, theme_id: uuid4) -> HttpResponse:
    if request.method == "POST":
        theme = Theme.objects.get(id=theme_id)
        theme.delete()
        return redirect(reverse("list_themes"))
    return HttpResponse(status=405)  # Method not allowed


def create_theme(request: HttpRequest, execution_id: uuid4) -> HttpResponse:
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
