from django.contrib.auth.models import User
from .models import Post,Tag
from rest_framework import serializers

class PostSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Post
		fields = ('url','id','title','created_time','author','body','tags')

class TagSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Tag
		fields = ('url','id','name','posts')

class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ('url','id','username','posts')