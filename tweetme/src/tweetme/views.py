from django.shortcuts import render

# retrieve
# GET -- template of home.html
def home(request):
	return render(request, "home.html", {})