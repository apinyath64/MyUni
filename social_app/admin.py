from django.contrib import admin
from home.models import Profile, Post, PostComment, Reply, LikedPost, LikedComment, LikedReply, PlaceImage

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    filter_horizontal = ('follows',)

admin.site.register(Profile, ProfileAdmin)
admin.site.register(PostComment)
admin.site.register(Reply)
admin.site.register(LikedPost)
admin.site.register(LikedComment)
admin.site.register(LikedReply)
admin.site.register(PlaceImage)
