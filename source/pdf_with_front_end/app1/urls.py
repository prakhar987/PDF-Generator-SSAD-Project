from django.conf.urls import url
#from polls import views
urlpatterns=(
	url(r'^func/$','app1.views.func'),
	url(r'^mail/$','app1.views.mail'),
)

