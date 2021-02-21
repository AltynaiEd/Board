from rest_framework import serializers
from .models import Post, Vote, Comments


class PostSerializer(serializers.ModelSerializer):
    poster = serializers.ReadOnlyField(source='poster.email')
    poster_id = serializers.ReadOnlyField(source='poster.id')
    votes = serializers.SerializerMethodField()
    # commentsa = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'category', 'title', 'url', 'video', 'image', 'body', 'poster', 'poster_id', 'created', 'votes', 'post_comments']

    def get_votes(self, post):
        return Vote.objects.filter(post=post).count()

    # def get_commentsa(self, post):
    #     return Comments.objects.filter(post=post)


class VoteSerializer(serializers.ModelSerializer):
    # votes = serializers.SerializerMethodField()
    class Meta:
        model = Vote
        fields = '__all__'


class CommentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields = '__all__'

