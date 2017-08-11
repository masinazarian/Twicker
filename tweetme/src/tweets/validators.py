from django.core.exceptions import ValidationError

# also to prevent profanity
def validate_content(value):
	content = value
	if content == "":
		raise ValidationError("Content cannot be blank")
	return value