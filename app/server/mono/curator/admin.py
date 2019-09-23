from django.contrib import admin

from .models import Artist, Exhibition

class MembershipInline(admin.TabularInline):
    model = Artist.exhibition.through
    extra = 0
    can_delete = False


class ArtistAdmin(admin.ModelAdmin):
    inlines = [MembershipInline]
    exclude = ('exhibition',)


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
    inlines = [MembershipInline]

    def artist_count(self, obj):
        return obj.artist_set.count()

admin.site.register(Exhibition, ExhibitionAdmin)
admin.site.register(Artist, ArtistAdmin)