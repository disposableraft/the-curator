from django.contrib import admin

from .models import Artist, Exhibition

class MembershipInline(admin.TabularInline):
    model = Artist.exhibition.through
    extra = 0
    can_delete = False
    classes = ['collapse']

    def has_change_permission(self, request, obj=None):
        return False


class ArtistAdmin(admin.ModelAdmin):
    inlines = [MembershipInline]
    exclude = ('exhibition',)
    search_fields = ['display_name', 'token']
    fields = ('display_name', 'token', 'moma_url')
    list_display = [
        'display_name', 'exhibition_count', 'moma_url', 'token',
    ]

    def exhibition_count(self, obj):
        return obj.exhibition.count()

class ExhibitionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'moma_url',]}),
        ('Meta', {
            'fields': ['moma_id', 'moma_number',],
            'classes': ['collapse'],
        }),
    ]
    search_fields = ['title', 'moma_number']
    list_display = [
        'title', 'artist_count', 'moma_url',
    ]
    inlines = [MembershipInline]

    def artist_count(self, obj):
        return obj.artist_set.count()

admin.site.register(Exhibition, ExhibitionAdmin)
admin.site.register(Artist, ArtistAdmin)