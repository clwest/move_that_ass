from django.contrib import admin

from .models import Prompt, PromptResponse


@admin.register(Prompt)
class PromptAdmin(admin.ModelAdmin):
    list_display = ("category", "created_at")


@admin.register(PromptResponse)
class PromptResponseAdmin(admin.ModelAdmin):
    list_display = ("prompt", "user", "created_at")

