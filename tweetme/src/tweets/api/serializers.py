from django.utils.timesince import timesince
from rest_framework import serializers


from accounts.api.serializers import UserDisplaySerializer
from tweets.models import Tweet # from ..models import Tweet

class TweetModelSerializer(serializers.ModelSerializer):
	user = UserDisplaySerializer(read_only=True) # read_only=True leaves out the user data request form in aip/tweet/create # another option: write_only
	date_display = serializers.SerializerMethodField()
	timesince = serializers.SerializerMethodField()
	class Meta:
		model = Tweet
		fields = [
		'user',
		'content',
		'timestamp',
		'date_display',
		'timesince',
		]

	def get_date_display(self, obj):
		return obj.timestamp.strftime("%b %d %Y at %I:%M %p") # refer to https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior

	def get_timesince(self, obj):
		return timesince(obj.timestamp) + " ago"