from ninja import NinjaAPI, ModelSchema
from django.shortcuts import get_object_or_404
from consult.consultations.models import Theme
from pydantic import BaseModel
from uuid import UUID



api = NinjaAPI()


class ThemeSchema(ModelSchema):
    class Meta:
        model = Theme
        fields = ['id', 'name', 'description']


@api.get("/theme/{theme_id}", response=ThemeSchema)
def get_theme(request, theme_id: UUID):
    theme = get_object_or_404(Theme, id=theme_id)
    return theme

