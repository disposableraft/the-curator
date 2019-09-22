from django.contrib import admin

from .models import Artist, Exhibition


class ArtistInline(admin.TabularInline):
    fields = ('display_name', 'token', 'moma_url')
    model = Artist
    extra = 0


class ExhibitionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'moma_url']}),
        ('Meta', {
            'fields': ['moma_id', 'moma_number'],
            'classes': ['collapse'],
        }),
    ]
    search_fields = ['title']
    list_display = [
        'title', 'artist_count', 'moma_url',
    ]
    inlines = [ArtistInline]
    def artist_count(self, obj):
        return len(obj.artist_set.all())

admin.site.register(Exhibition, ExhibitionAdmin)