from django.contrib import admin

from .models import GeneratedImage, SocialPost


@admin.register(GeneratedImage)
class GeneratedImageAdmin(admin.ModelAdmin):
    list_display = ("image_url", "created_at")


@admin.register(SocialPost)
class SocialPostAdmin(admin.ModelAdmin):
    list_display = ("image", "shared_to", "shared_at", "was_successful")

