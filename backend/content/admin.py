from django.contrib import admin

from .models import GeneratedImage, SocialPost, GeneratedMeme


@admin.register(GeneratedImage)
class GeneratedImageAdmin(admin.ModelAdmin):
    list_display = ("image_url", "created_at")


@admin.register(SocialPost)
class SocialPostAdmin(admin.ModelAdmin):
    list_display = ("image", "shared_to", "shared_at", "was_successful")


@admin.register(GeneratedMeme)
class GeneratedMemeAdmin(admin.ModelAdmin):
    list_display = ("user", "tone", "created_at")

