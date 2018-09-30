from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages
from django.db.models import Q 
from urllib.parse import quote_plus

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render

# Create your views here.
#function based views.
from .forms import PostForm
from .models import Post

def post_create(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	form = PostForm(request.POST or None,  request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		messages.success(request, "Successfully Created")
		return HttpResponseRedirect(instance.get_absolute_url())
	
		
	 	


	context = {
	     "form": form,
	}
	return render(request, "post_form.html", context)
def post_detail(request, pk=None):
	instance = get_object_or_404(Post, pk=pk)
	share_string = quote_plus(instance.content)

	context = {
	    "title": instance.title,
	    "instance": instance,
	    "share_string": share_string,
	}
	return render(request, "post_detail.html", context)
def post_list(request):
	queryset_list = Post.objects.all()
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
			Q(title__icontains=query)|
			Q(content__icontains=query)|
			Q(user__first_name__icontains=query)|
			Q(user__last_name__icontains=query)
			).distinct()

	paginator = Paginator(queryset_list, 5) # Show 25 contacts per page

	page = request.GET.get('page')
	queryset = paginator.get_page(page)
    



   
	context = {
	   "object_list": queryset,
	   "title": "list"
	}
	return render(request, "post_list.html", context)


	







def post_update(request, pk=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post, pk=pk)
	form = PostForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)

		instance.save()
		messages.success(request, "Item Saved")
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
	      "title": instance.title,
	      "instance": instance,
	      "form": form,
	}
	return render(request, "post_form.html", context)


def post_delete(request, pk=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post, pk=pk)
	instance.delete()
	messages.success(request, "Successfully deleted")

	return redirect("posts:list") 


