from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser

#User = get_user_model()
class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)
    
    def __str__(self):
        return self.email

class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField("home.User", on_delete=models.CASCADE, related_name='profile')
    follows= models.ManyToManyField('self',
        related_name='followed_by',
        symmetrical=False,
        blank=True)
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='default-profile.png')
    location = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.user.username

class Place(models.Model): 
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=150, default='')
    detail = models.TextField(default='')
    latitude = models.FloatField()
    longitude = models.FloatField()    
    
    def __str__(self):
        return f'{self.name}'
    
class PlaceImage(models.Model):
    id = models.AutoField(primary_key=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, null=True, related_name='images')
    image = models.ImageField(upload_to='place_images', blank=True)
    
    def __str__(self):
        return f'place image {self.place.name}'
    
class Post(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE, null=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=100, null=True)
    content = models.TextField(default='')
    likes = models.ManyToManyField(User, related_name='likedposts', through='LikedPost', default=0)
    created_at = models.DateTimeField(default=timezone.now, blank=True)
    
    def __str__(self):
        return (f'{self.title} {self.user} {self.place}')


class LikedPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username} : {self.post.title}'

class PostImage(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, related_name='images')
    image = models.ImageField(upload_to='post_images', blank=True)
    
    def __str__(self):
        return f'post image {self.post.title}'

class PostComment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, related_name='comments')
    content = models.TextField(default='')
    likes = models.ManyToManyField(User, related_name='likedcomments', through='LikedComment',default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering=['-created_at']
        
    def __str__(self):
        return f'Comment by {self.user} "{self.content}"'
    
class LikedComment(models.Model):
    comment = models.ForeignKey(PostComment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username} : {self.comment.content[:30]}'


    
class PostCommentImage(models.Model):
    id = models.AutoField(primary_key=True)
    post_comment = models.ForeignKey(PostComment, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='post_images', blank=True)
    
    def __str__(self):
        return f'post comment image {self.post_comment.id}'
   

class Reply(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE, null=True, related_name="replies")
    parent_comment = models.ForeignKey(PostComment, on_delete=models.CASCADE, related_name="replies", null=True, blank=True)
    parent_reply = models.ForeignKey('Reply', on_delete=models.CASCADE, related_name="nested_replies", null=True, blank=True)
    level = models.IntegerField(default=1)
    content = models.TextField(default='')
    likes = models.ManyToManyField(User, related_name='likedreplies', through='LikedReply', default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering=['-created_at']
        
    def __str__(self):
        return f'{self.user} "{self.content}"'
    
    
class ReplyImage(models.Model):
    id = models.AutoField(primary_key=True)
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='reply_images/', blank=True)
    
    def __str__(self):
        return f'reply image for: {self.reply.id}'
   


class LikedReply(models.Model):
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username} : {self.reply.content}'
 
class Event(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE, null=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=300)
    detail = models.TextField(default='')
    start_date = models.DateTimeField(null=True,blank=True)
    end_date = models.DateTimeField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.title}'
    
class EventImage(models.Model):
    id = models.AutoField(primary_key=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, related_name='images')
    image = models.ImageField(upload_to='event_images', blank=True)
    
    def __str__(self):
        return f'event image {self.event.title}'
    
    
class EventMember(Event):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="events")
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name="event_members")
    
    class Meta:
        unique_together = ["event", "member"]
    
    def __str__(self):
        return f'{self.member}'
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Notification for {self.user.username}: {self.message}'
    
    