from django.urls import path
from . import views
from blog.feeds import AllPostsRssFeed


app_name='blog'
urlpatterns=[
	path(r'',views.IndexView.as_view(),name='index'),
	path(r'post/<int:pk>/',views.DetailView.as_view(),name='detail'),
	path(r'archives/<int:year>/<int:month>/',views.ArchivesView.as_view(),name='archives'),
	path(r'category/<int:pk>',views.CategoryView.as_view(),name='category'),
	path(r'tag/<int:pk>',views.TagView.as_view(),name='tag'),
	path(r'rss/',AllPostsRssFeed(),name='rss'),
	path(r'search/',views.search,name='search')
]