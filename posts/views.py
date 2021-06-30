
from django.http.response import Http404, HttpResponseForbidden, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Post 
from .forms import PostForm
import cloudinary

def index(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save() 
            return HttpResponseRedirect('/')

        else:    
            return HttpResponseRedirect(form.errors.as_json())

    
    posts = Post.objects.order_by('created_at').reverse().all()[:20]
    return render(request, 'posts.html',
                    {'posts' : posts})

def delete(request, post_id):
    posts = Post.objects.get(id = post_id)
    posts.delete()
    return HttpResponseRedirect('/')

def edit(request, post_id):
    posts = Post.objects.get(id = post_id)
    form = PostForm(instance=posts)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=posts)
        if form.is_valid:
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'edit.html', context)


def like(request, post_id):
    posts = Post.objects.get(id = post_id)
    new_like = posts.like_count + 1
    posts.like_count = new_like
    print(posts.like_count)
    posts.save()

    return HttpResponseRedirect('/')


