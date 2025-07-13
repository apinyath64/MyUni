from django.views.generic import DetailView
from django.shortcuts import redirect
from .models import Post, PostComment
from .forms import CommentForm

class PostDetail(DetailView):
    template_name= 'post_content.html'
    model= Post

    def get_context_data(self , **kwargs):
        data = super().get_context_data(**kwargs)
        connected_comments = PostComment.objects.filter(CommentOnPost=self.get_object())
        number_of_comments = connected_comments.count()
        data['comments'] = connected_comments
        data['no_of_comments'] = number_of_comments
        data['comment_form'] = CommentForm()
        return data

    def post(self , request , *args , **kwargs):
        if self.request.method == 'POST':
            print('-------------------------------------------------------------------------------Reached here')
            comment_form = CommentForm(self.request.POST)
            if comment_form.is_valid():
                content = comment_form.cleaned_data['content']
                try:
                    parent = comment_form.cleaned_data['parent']
                except:
                    parent=None

            

            new_comment = PostComment(content=content , user = self.request.user , CommentOnPost=self.get_object() , parent=parent)
            new_comment.save()
            return redirect(self.request.path_info)