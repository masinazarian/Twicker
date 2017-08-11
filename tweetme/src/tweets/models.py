from django.conf import settings
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.

from .validators import validate_content


class Tweet(models.Model):
	user 		= models.ForeignKey(settings.AUTH_USER_MODEL)
	content 	= models.CharField(max_length=140, validators=[validate_content])
	updated  	= models.DateTimeField(auto_now=True)
	timestamp  	= models.DateTimeField(auto_now_add=True)

	# # For example, to store numbers up to 999 with a resolution of 2 decimal places, you’d use:
	# predictedPrice	= models.DecimalField(..., max_digits=5, decimal_places=2)

	def __str__(self):
		return str(self.content) 
		# return str(self.id) 

	# def clean(self, *args, **kwargs):
	# 	content = self.content
	# 	if content == "abc":
	# 		raise ValidationError("Content cannot be ABC")
	# 	return super(Tweet, self).clean(*args, **kwargs)

	def get_absolute_url(self):
		return reverse("tweet:detail", kwargs={"pk":self.pk})

	# another way to reverse the odering of tweets appearing 
	# class Meta:
	# 	ordering = ['-timestamp', 'content']

	# yet another way to reverse the odering of tweets appearing 
	# would be to use model manager to override the Tweet.objects.all() method to reverse the order