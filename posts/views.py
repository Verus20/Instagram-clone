from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render

from .models import Post

# Create your views here.
def home_view(request, *args, **kwargs):
    return render(request, "pages/home.html", context={}, status=200)

def post_list_view(request, *args, **kwargs):
    qs = Post.objects.all()
    posts_list = [{"id": x.id, "content": x.content} for x in qs]
    data = {
        "isUser": False,
        "response": posts_list
    }
    return JsonResponse(data)

def post_detail_view(request, post_id, *args, **kwargs):
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