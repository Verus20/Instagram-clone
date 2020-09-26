import random
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .forms import PostForm
from .models import Post, PostLike, Test
from .serializers import (
    PostSerializer, 
    PostActionSerializer,
    PostCreateSerializer, 
    PostLikeSerializer, 
    TestSerializer
)

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Create your views here.
@api_view(['GET'])
def test_view(request, *args, **kwargs):
    test_var = Test.objects.all()
    test_serializer = TestSerializer(test_var, many=True)
    return Response(test_serializer.data)

# Home page view, renders the home page to url shown below
def home_view(request, *args, **kwargs):
    print(request.user or None)
    return render(request, "pages/home.html", context={}, status=200)

@api_view(['POST']) # http method the client will send is POST
# @authentication_classes([])
@permission_classes([IsAuthenticated])
def post_create_view(request, *args, **kwargs):
    serializer = PostCreateSerializer(data=request.POST)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)

@api_view(['GET'])
def post_detail_view(request, post_id, *args, **kwargs):
    qs = Post.objects.filter(id=post_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = PostSerializer(obj)
    return Response(serializer.data, status=200)

@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def post_action_view(request, *args, **kwargs):
    """
    id is required
    Action options are: like, unlike, comment on someone's post
    delete(uncomment) on someone's post
    """
    serializer = PostActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        post_id = data.get("id")
        action = data.get("action")
        content = data.get("content")
        qs = Post.objects.filter(id=post_id)
        if not qs.exists():
            return Response({}, status=404)
        obj = qs.first()
        test = Post.objects.filter(id=post_id)
        if action == "like":
            obj.likes.add(request.user)
            serializer = PostSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == 'unlike':
            obj.likes.remove(request.user)
        elif action == "comment":
            new_comment = Post.objects.create(
                user=request.user, 
                parent=obj,
                content=content,)
            serializer = PostSerializer(new_comment)
            return Response(serializer.data, status=200)
        elif action == "uncomment":
            # to do for uncommenting (delete a comment) on someone's post
            pass    
    return Response({}, status=200)

@api_view(['GET'])
def post_list_view(request, *args, **kwargs):
    qs = Post.objects.all()
    serializer = PostSerializer(qs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def postlike_list_view(request, *args, **kwargs):
    qs_like = PostLike.objects.all()
    like_serializer = PostLikeSerializer(qs_like, many=True)
    return Response(like_serializer.data)

def post_create_view_pure_django(request, *args, **kwargs):
    """
    form = PostForm(request.POST or None) means that data can be 
    passed through the form or not
    """
    """
    REST API Create View -> Django Rest Framework
    """
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    form = PostForm(request.POST or None)
    next_url = request.POST.get('next') or None
    if form.is_valid():
        obj = form.save(commit=False)
        # do other form related logic
        obj.user = request.user
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201) # 201 == created items

        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = PostForm()
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)
    return render(request, 'components/form.html', context={"form": form})

def post_list_view_pure_django(request, *args, **kwargs):
    qs = Post.objects.all()
    posts_list = [x.serialize() for x in qs]
    data = {
        "isUser": False,
        "response": posts_list
    }
    return JsonResponse(data)

def post_detail_view_pure_django(request, post_id, *args, **kwargs):
    """
    REST API VIEW -> REST stands for Representational State Transfer
    API stands for application programming interface
    VIEW is just the view
    Consume by JavaScript or Swift/Java/iOS/Android
    return json data
    """

    data = {
        "id": post_id,
        # "image_path": obj.image.url
    }
    status = 200
    try:
        obj = Post.objects.get(id=post_id)
        data['content'] = obj.content
    except:
        data['message'] = 'Not found'
        status = 404

    return JsonResponse(data, status=status) # similar to json.dumps content_type='application/json'