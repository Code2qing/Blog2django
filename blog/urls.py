from django.urls import path,include
from . import views
from blog.feeds import AllPostsRssFeed
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'posts',views.PostViewSet)
router.register(r'tags',views.TagViewSet)
router.register(r'users',views.UserViewSet)

app_name='blog'
urlpatterns=[
	path(r'',views.IndexView.as_view(),name='index'),
	path(r'post/<int:pk>/',views.PostDetailView.as_view(),name='detail'),
	path(r'archives/<int:year>/<int:month>/',views.ArchivesView.as_view(),name='archives'),
	path(r'archives/',views.archives_list,name='archives_list'),
	path(r'category/<int:pk>',views.CategoryView.as_view(),name='category'),
	path(r'category/',views.category_list,name='category_list'),
	path(r'tag/<int:pk>',views.TagView.as_view(),name='tag'),
	path(r'tags/',views.tags_list,name='tag_list'),
	path(r'rss/',AllPostsRssFeed(),name='rss'),
	#path(r'search/',views.search,name='search')
	path(r'api/',include(router.urls)),
	path('api/api-auth/',include('rest_framework.urls')),
]