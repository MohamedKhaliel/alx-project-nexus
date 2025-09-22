from django.contrib import admin
from .models import Poll, Option, Vote


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'expires_at')
    search_fields = ('title',)
    list_filter = ('created_at', 'expires_at')


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'poll', 'text')
    search_fields = ('text',)
    list_filter = ('poll',)


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'poll', 'option', 'voter_id', 'cast_at')
    search_fields = ('voter_id',)
    list_filter = ('poll', 'option')

# Register your models here.
