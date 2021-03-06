from rest_framework import permissions
class IsAuthorOrReadOnly(permissions.BasePermission):
	def has_object_permisson(self,request,vies,obj):
		# SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
		if request.method in permissions.SAFE_METHODS:
			return True

		return obj.author == request.user