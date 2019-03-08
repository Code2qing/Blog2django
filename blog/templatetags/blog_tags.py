from ..models import Post,Category,Tag
from django import template
from django.db.models.aggregates import Count
import html
from django.middleware.csrf import get_token

register=template.Library()


@register.simple_tag
def get_posts_count():
	return Post.objects.all().count()


@register.simple_tag
def get_recent_posts(num=5):
	return Post.objects.all().order_by('-created_time')[:num]


@register.simple_tag
def get_archives():
	return Post.objects.dates('created_time','month',order='DESC')


@register.simple_tag
def get_categories():
	return Category.objects.annotate(num_posts=Count('posts')).filter(num_posts__gt=0)
	# return Category.objects.all()


@register.simple_tag
def get_tags():	
	return Tag.objects.annotate(num_posts=Count('posts')).filter(num_posts__gt=0)
	# return Tag.objects.all()


@register.simple_tag
def show_children_comments(comment, request):
	csrf_token = get_token(request)
	html_fill = """<div class="comment-children">
					<ul class="comment-list list-unstyled">
					{0}
					</ul>
					</div>
				"""

	li_html_fill = """
					<li class="comment-item">
					<span class="nickname">{0}</span>
					<time class="submit-date">{1}</time>
					<div class="text">
					<p>{2}</p>
					</div>
					{3}
					{4}
					</li>
					"""

	form_heml_fill = """
					<div id="comment-{0}" onclick="hold('comment-form-{1}')">
					<i class="fa fa-reply-all"></i>&nbsp; 回复</div>
					<div id="comment-form-{2}" style="display: none;">
					<div class="bootstrap-frm">
					<form action="/comment/post/{3}/" method="post" class="STYLE-NAME">
					<h1>发表回复
					<span>请填写全部信息</span>
					</h1>
					<input type='hidden' name='csrfmiddlewaretoken' value='{4}' />
					<input type='hidden' name='is_reply' value=2 />
					<input type='hidden' name='reply' value={5} />
					<label for="id_nickname"><span>*名字：</span></label>
					<input type="text" name="nickname" maxlength="100" required id="id_nickname" />
					
					<label for="id_email"><span>*邮箱：</span></label>
					
					<input type="email" name="email" maxlength="100" required id="id_email" />
					
					
					<label for="id_url"><span>网址：</span></label>
					
					<input type="url" name="url" maxlength="200" id="id_url" />
					
					
					<label for="id_text"><span>*评论：</span></label>
					
					<textarea name="text" cols="40" rows="10" required id="id_text"></textarea>
					
					<label>
					<span>&nbsp;</span>
					<button type="submit" class="button">发表</button>
					</label>
					</form>
					</div>
					</div>
					"""

	def join_html(comment_):
		li_ = ''
		if comment_.comment_set.count() == 0:
			return ''
		for cmt in comment_.comment_set.all():
			form_ = form_heml_fill.format(cmt.id, cmt.id, cmt.id, comment.post.id, csrf_token, cmt.id)
			li_ += li_html_fill.format(cmt.nickname, cmt.created_time, html.escape(cmt.text), form_, join_html(cmt))
		return html_fill.format(li_)

	return join_html(comment)
