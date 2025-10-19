from django import forms
from home.models import Post, Event, PostComment, Reply, Place, EventMember


class PostForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    class Meta:
        model = Post
        fields = ('title', 'content',)
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ['content']
        widgets = {
            'content' : forms.Textarea(attrs={'class': 'w-full p-2 px-4 text-sm border-transparent rounded focus:ring focus:ring-gray-300 focus:outline-none', 'placeholder': 'เขียนความคิดเห็นของคุณ ...', 'rows': 5}), 
        }
        required=True
        labels = {
            'content': '',
        }
        
class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']
        widgets = {
            'content' : forms.TextInput(attrs={'class': 'w-full p-2 px-4 text-sm border-transparent rounded focus:ring focus:ring-gray-300 focus:outline-none','placeholder': 'เขียนข้อความตอบกลับ ...'})
        }
        labels = {
            'content': '',
        }
   
   
class NestedReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']
        widgets = {
            'content' : forms.TextInput(attrs={'autofocuss': True, 'class': '!text-xs bg-gray-200 !p-0 !pl-0 !h-8','placeholder': 'ตอบกลับ ...', 'class': "!text-xs"})
        }
        labels = {
            'content': '',
        }     
        
     
class EventForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    class Meta:
        model = Event
        fields = ('title', 'detail', 'start_date', 'end_date')
        

class EventCalendarForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    start_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    end_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    
    class Meta:
        model = Event
        fields = ('title', 'detail', 'image', 'start_date', 'end_date', 'place')
        
        
    def __init__(self, *args, **kwargs):
        super(EventCalendarForm, self).__init__(*args, **kwargs)
        self.fields['place'].queryset = Place.objects.all()
        
        
class AddMemberForm(forms.ModelForm):
    class Meta:
        model = EventMember
        fields = ["member"]

        widgets = {
            'member': forms.Select(attrs={'class': 'block p-2 px-4 focus:ring-gray-300 focus:border-gray-300 shadow-sm sm:text-sm border border-[#594100] rounded'})
        }