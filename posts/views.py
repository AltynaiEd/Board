from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics, permissions, mixins, status
from rest_framework.decorators import action

from .models import Post, Vote, Comments
from .serializers import PostSerializer, VoteSerializer, CommentsSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .paginations import Paginatin
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = Paginatin
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, ]
    search_fields = ['title', 'body']
    filterset_fields = ['category']

    def perform_create(self, serializer):
        serializer.save(poster=self.request.user)

    # @action(detail=False, methods=['get'])
    # def search(self, request, pk=None):
    #     print(request.query_params)
    #     q = request.query_params.get('q')
    #     queryset = self.get_queryset()
    #     queryset = queryset.filter(Q(title__icontains=q))
    #     serializer = PostSerializer(queryset, many=True, context={'request': request})
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     search_query = self.request.query_params.get('search')
    #     if search_query:
    #         queryset = queryset.annotate(
    #             similarity = TrigramSimilarity('title', search_query),
    #         ).filter(similarity__gt=0.2).order_by('-similarity')
    #     return queryset


class PostRetrievDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        post = Post.objects.filter(pk=kwargs['pk'], poster=self.request.user)
        if post.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError('Вы не можете удалить этот пост')

    def patch(self, request, *args, **kwargs):
        post = Post.objects.filter(pk=kwargs['pk'], poster=self.request.user)
        if post.exists():
            return self.partial_update(request, *args, **kwargs)
        else:
            raise ValidationError('Вы не можете вносить изменения в чужой пост')

    def put(self, request, *args, **kwargs):
        post = Post.objects.filter(pk=kwargs['pk'], poster=self.request.user)
        if post.exists():
            return self.partial_update(request, *args, **kwargs)
        else:
            raise ValidationError('Вы не можете обновить полностью')


class VoteCreate(generics.CreateAPIView, mixins.DestroyModelMixin):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        post = Post.objects.get(pk=self.kwargs['pk'])
        return Vote.objects.filter(voter=user, post=post)

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError('Вы уже проголосовали')
        serializer.save(voter=self.request.user, post=Post.objects.get(pk=self.kwargs['pk']))

    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError('Вы не голосовали здесь')


# class PostCommentList(generics.CreateAPIView):
#     serializer_class = CommentsSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#
#     def get_queryset(self):
#         user = self.request.user
#         post = Post.objects.get(pk=self.kwargs['pk'])
#         return Comments.filter(author=user, post=post)
#
#     def perform_create(self, serializer):
#         # if self.get_queryset().exists():
#         #     raise ValidationError('Ты уже проголосовал')
#         serializer.save(author=self.request.user, post=Post.objects.get(pk=self.kwargs['pk']))


class Comment(generics.CreateAPIView, mixins.DestroyModelMixin):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [permissions.IsAuthenticated]

    # def perform_create(self, serializer):
    #     post_pk = self.request.POST.get('post_pk')
    #     text = self.request.POST.get('text')
    #     serializer.save(author=self.request.user, post=Post.objects.get(pk=post_pk), text=text)

    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError('Ты не комментировал здесь')






class FavoritePosts(generics.ListCreateAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    pagination_class = Paginatin
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None):
        queryset = Vote.objects.filter(voter=self.request.user)
        serializer = VoteSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
#
# class FavoritePosts(generics.ListCreateAPIView):
#     queryset = Vote.objects.all()
#     serializer_class = VoteSerializer
#     pagination_class = Paginatin
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get(self, request, pk=None):
#         return Response(VoteSerializer(Vote.objects.filter(voter=self.request.user)).data, status=status.HTTP_200_OK)



