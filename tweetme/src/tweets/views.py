# MOVED TO mixins.py
# from django import forms
# from django.forms.utils import ErrorList
from django.contrib.auth.mixins import LoginRequiredMixin # to force the user to be logged in
from django.db.models import Q # django q lookups
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy #, reverse
from django.views.generic import (
				CreateView, 
				DetailView,
				DeleteView, 
				ListView, 
				UpdateView
				)

from .forms import TweetModelForm
from .mixins import FormUserNeededMixin, UserOwnerMixin
from .models import Tweet

# Create your views here.

# CRUD Create Retrieve Update Delete
# List Search

# Create
#class based view
class TweetCreateView(FormUserNeededMixin, CreateView): #(LoginRequiredMixin, FormUserNeededMixin, CreateView):
	form_class = TweetModelForm
	template_name = 'tweets/create_view.html'
	# success_url = reverse_lazy("tweet:detail")  # reverse() # "/tweet/create/" # replaced with get_absolute_url in models.py
	# login_url = '/admin/'

	# MOVED TO mixins.py
	# def form_valid(self, form):
	# 	if self.request.user.is_authenticated():
	# 		form.instance.user = self.request.user
	# 		return super(TweetCreateView, self).form_valid(form)
	# 	else:
	# 		form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList(["User must be logged in to continue."])
	# 		return self.form_invalid(form)

# #function based view
# def tweet_create_view(request):
# 	form = TweetModelForm(request.POST or None)
# 	if form.is_valid():
# 		instance = form.save(commit=False)
# 		instance.user = request.user
# 		instance.save()
# 	context = {
# 		"form": form
# 	}
# 	return render(request, 'tweets/create_view.html', context)

# Update
class TweetUpdateView(LoginRequiredMixin, UserOwnerMixin, UpdateView):
    queryset = Tweet.objects.all()
    form_class = TweetModelForm
    template_name = 'tweets/update_view.html'
    # success_url = "/tweet/"


# Delete
class TweetDeleteView(LoginRequiredMixin, DeleteView):
	model = Tweet
	template_name = 'tweets/delete_confirm.html'
	success_url = reverse_lazy("tweet:list") # reverse("tweet:list") # ("home")   # reverse()

# Retrieve
# two ways to retrieve: class-based views / function-based views

class TweetDetailView(DetailView):
	# template_name = "tweets/detail_view.html"
	queryset = Tweet.objects.all()

	# def get_object(self):
	# 	print(self.kwargs)
	# 	pk = self.kwargs.get("pk") # or self.kwargs["pk"], it is a dictionary
	# 	obj = get_object_or_404(Tweet, pk=pk)
	# 	# return Tweet.objects.get(id=pk)
	# 	return obj

class TweetListView(ListView):
	# template_name = "tweets/list_view.html"
	# queryset = Tweet.objects.all() # replaced by get_queryset() for advanced searching

	def get_queryset(self, *args, **kwargs):
		qs = Tweet.objects.all()
		query = self.request.GET.get("q", None)
		if query is not None:
			# qs = qs.filter(content__icontains=query) # replaced by q lookups below
			qs = qs.filter(
				Q(content__icontains=query) |
				Q(user__username__icontains=query)
				)
		return qs

	def get_context_data(self, *args, **kwargs):
		context = super(TweetListView, self).get_context_data(*args, **kwargs)
		context['create_form'] = TweetModelForm() # parans means it is not gonna get requesting data but just giving some context there
		context['create_url'] = reverse_lazy("tweet:create")
		# context["another_list"] = Tweet.objects.all()
		# print(context)		
		return context

def tweet_detail_view(request, pk=None): # pk == id
	# obj = Tweet.objects.get(pk=pk) # GET object from database
	obj = get_object_or_404(Tweet, pk=pk)
	print(obj)
	context = {
		"object": obj,
		# "abc": obj,
	}
	return render(request, "tweets/detail_view.html", context)

# def tweet_list_view(request):
# 	queryset = Tweet.objects.all() # GET list of all objects from the model
# 	print(queryset)
# 	for obj in queryset:
# 		print(obj.content)
# 	context = {
# 		"object_list": queryset
# 	}
# 	return render(request, "tweets/list_view.html", context)