from django_filters import FilterSet
from .models import Comment


class CommentFilter(FilterSet):
    class Meta:
        model = Comment
        fields = ['post']


