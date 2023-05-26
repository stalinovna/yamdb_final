from django.contrib import admin
from reviews.models import Comment, Review


class ReviewAdmin(admin.ModelAdmin):
    """Class of review."""

    list_display = (
        'pk',
        'author',
        'title',
        'text',
        'score',
        'pub_date',
    )
    empty_value_display = '-пусто-'
    search_fields = ('author', 'title', 'text',)
    list_filter = ('author',)


class CommentAdmin(admin.ModelAdmin):
    """Class of comment."""

    list_display = (
        'pk',
        'author',
        'review',
        'text',
        'pub_date',
    )
    empty_value_display = '-пусто-'
    search_fields = ('author', 'text', 'pub_date',)
    list_filter = ('author',)


admin.site.register(Comment, CommentAdmin)
admin.site.register(Review, ReviewAdmin)
