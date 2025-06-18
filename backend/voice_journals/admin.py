from django.contrib import admin
from .models import VoiceJournal


@admin.register(VoiceJournal)
class VoiceJournalAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at")
