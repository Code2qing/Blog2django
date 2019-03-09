from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from blog.models import Post
from .models import Comment
from .forms import CommentForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
import json

from comments.tasks import comment_notice


# Create your views here.

def post_comment(request,post_id):
	post = get_object_or_404(Post,pk=post_id)

	if request.method == 'POST':
		form = CommentForm(request.POST)

		if form.is_valid():
			comment = form.save(commit=False)  # 不将数据提交到数据库，仅生成模型实例
			comment.post = post
			comment.save()

			# 使用异步任务发送邮件
			comment_notice.delay(comment.id)

			return redirect(reverse('blog:detail',args=(post_id,))+'#comments')

		else:
			comment_list =post.comment_set.order_by('-created_time').all()
			context={
			'post':post,
			'form':form,
			'comment_list':comment_list
			}

			return render(request,'blog/detail.html',context)

	else:
		return redirect(reverse('blog:detail',args=(post_id,))+'#comments')

@login_required
@permission_required('comments.change_comment')
def check_comment(request, comment_id):
	"""
	审核评论
	:param request:
	:param comment_id:
	:return:
	"""
	try:
		comment = Comment.objects.get(id=comment_id)
		comment.is_check = True
		comment.save()
		post_id = comment.post.id
		return redirect(reverse('blog:detail',args=(post_id,))+'#comments')
	except:
		return HttpResponse(json.dumps({"status": "ERROR"}))
