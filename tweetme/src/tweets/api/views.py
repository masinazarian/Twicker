from django.db.models import Q # django q lookups
from rest_framework import generics
from rest_framework import permissions

from tweets.models import Tweet

from .pagination import StandardResultsPagination
from .serializers import TweetModelSerializer

class TweetCreateAPIView(generics.CreateAPIView):
	serializer_class = TweetModelSerializer
	permission_classes = [permissions.IsAuthenticated] # to make sure it checks the user authentication, check http://127.0.0.1:8000/api/tweet/create/ in an ingognito window to see the result

	def perform_create(self, serializer):
		serializer.save(user=self.request.user) # to handle the error: NOT NULL constraint failed: tweets_tweet.user_id

class TweetListAPIView(generics.ListAPIView):
	serializer_class = TweetModelSerializer
	pagination_class = StandardResultsPagination

	def get_queryset(self, *args, **kwargs):
		# if we did not have timestamp we could have order_by("-pk") that is auto-incrementing primary key
		# another way to achieve this would be as shown in tweets.models.py 
		qs = Tweet.objects.all().order_by("-timestamp") # order_by to reverse the order of tweets appearing
		# print(self.request.GET)
		query = self.request.GET.get("q", None)
		if query is not None:
			# qs = qs.filter(content__icontains=query) # replaced by q lookups below
			qs = qs.filter(
				Q(content__icontains=query) |
				Q(user__username__icontains=query)
				)
		return qs