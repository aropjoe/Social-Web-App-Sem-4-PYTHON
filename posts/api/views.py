from rest_framework.generics import ListAPIView,CreateAPIView,DestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions,status
from ..models import Post
from .serializers import PostModelSerializer
from django.db.models import Q
from .pagination import StandardResultsPagination
from django.shortcuts import get_object_or_404

class LikeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,pk,format=None):
        post_qs=Post.objects.filter(pk=pk)
        message="Not allowed"
        if request.user.is_authenticated:
            is_liked=Post.objects.like_toggle(request.user,post_qs.first())
            return Response({'liked':is_liked})
        return Response({"message":message},status=400)

class PostDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,pk):
        post_qs=get_object_or_404(Post,pk=pk)
        serializer= PostModelSerializer(post_qs)
        return Response(serializer.data)
    def delete(self, request,pk):
        print("PK is",pk)
        post_qs=get_object_or_404(Post,pk=pk)
        post_qs.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PostCreateAPIView(CreateAPIView):
    serializer_class = PostModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PostListAPIView(ListAPIView):
    serializer_class = PostModelSerializer
    pagination_class = StandardResultsPagination

    def get_serializer_context(self,*args,**kwargs):
        context=super(PostListAPIView,self).get_serializer_context(*args,**kwargs)
        context['request']=self.request
        return context

    def get_queryset(self, *args, **kwargs):
        im_following=self.request.user.profile.get_following()
        qs1 = Post.objects.filter(user__in=im_following)
        qs2 = Post.objects.filter(user=self.request.user)
        qs=(qs1 | qs2).distinct().order_by("-updated_on")
        print(self.request.GET)
        query =self.request.GET.get("q",None)
        if query is not None:
            qs=qs.filter(
                Q(content__icontains=query) |
                Q(user__username__icontains=query)
            )
        return qs

class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostModelSerializer
    lookup_field = 'pk'
