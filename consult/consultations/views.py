from typing import Optional
from uuid import uuid4

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import Execution, Theme
from .forms import ThemeForm


def list_themes_for_execution_run(
    request: HttpRequest, execution_id: Optional[uuid4] = None
) -> HttpResponse:
    if request.POST:
        execution_id = request.POST.get("execution-run")
        return redirect(reverse("list_themes_for_execution", args=(execution_id,)))
    all_execution_runs = Execution.objects.all()
    if not execution_id:
        execution_id = Execution.objects.first().id  # pick the first as default
    themes = Theme.objects.filter(execution__id=execution_id)
    return render(
        request,
        "list_themes.html",
        {
            "selected_execution_run": execution_id,
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

