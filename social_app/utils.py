from django.dispatch import receiver
from home.models import Post, Event, Notification
from django.db.models.signals import post_save

def comment_notification(user, post, comment):
    message = f"{user.username} commented on your post '{post.title}'"
    Notification.objects.create(user=post.user, message=message)
    
def reply_notification(user, comment, reply):
    message = f"{user.username} replies on your comment '{comment.content}'"
    Notification.objects.create(user=comment.user, message=message)
   
@receiver(post_save, sender=Post) 
def notify_followwers_post(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        place = instance.place
        followers = user.profile.followed_by.all()
        for follower in followers:
            message = f"{user.username} has created a new post: '{instance.title}' at {place.name}"
            Notification.objects.create(user=follower.user, message=message)
            
@receiver(post_save, sender=Event)         
def notify_followwers_event(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        place = instance.place
        followers = user.profile.followed_by.all()
        for follower in followers:
            message = f"{user.username} has created a new event: '{instance.title}' at {place.name}"
            Notification.objects.create(user=follower.user, message=message)