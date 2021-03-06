from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse
from .models import Post, Category, Tag
import markdown
from comments.forms import CommentForm
from django.views import generic
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.db.models import Q
from rest_framework import viewsets, permissions, mixins
from django.contrib.auth.models import User
from .serializer import PostSerializer, TagSerializer, UserSerializer
from .permission import IsAuthorOrReadOnly
from django.views.decorators.cache import cache_page  # 缓存装饰器
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TagViewSet(mixins.CreateModelMixin,
                 mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    premission_classes = (permissions.IsAdminUser)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# @method_decorator(cache_page(60*15),name='dispatch')
# @method_decorator(csrf_protect,name='dispatch')
class IndexView(generic.ListView):
    model = Post

    template_name = 'blog/index.html'
    # context_object_name = 'post_list'
    paginate_by = 6

    def get_quertset(self):
        return Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')
        queryset = context.get('object_list')

        pagination_data = self.pagination_data(paginator, page, is_paginated)

        context.update(pagination_data)

        menu_home = True

        context.update({'menu_home': menu_home})

        for post in queryset:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            post.excerpt = md.convert(post.excerpt)

        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            return {}

        left = []
        right = []
        left_has_more = False
        right_has_more = False
        first = False
        last = False

        page_number = page.number

        total_pages = paginator.num_pages

        page_range = paginator.page_range

        if page_number == 1:
            right = page_range[page_number:page_number + 2]
            if right[-1] + 1 < total_pages:
                right_has_more = True

            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        else:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]

            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
            if right[-1] + 1 < total_pages:
                right_has_more = True

            if right[-1] < total_pages:
                last = True

        data = {'left': left, 'right': right, 'left_has_more': left_has_more, 'right_has_more': right_has_more,
                'first': first, 'last': last, }
        return data


# def detail(request,post_id):
# 	post = get_object_or_404(Post,pk=post_id)
# 	post.body=markdown.markdown(post.body,
# 								extensions=[
# 									'markdown.extensions.extra',
# 									'markdown.extensions.codehilite',
# 									'markdown.extensions.toc',
# 								])

# 	post.increase_views()

# 	form = CommentForm()
# 	comment_list = post.comment_set.all()

# 	return render(request,'blog/detail.html',context={'post':post,'form':form,'comment_list':comment_list})
# @method_decorator(cache_page(60 * 15), name='dispatch')
# @method_decorator(csrf_protect, name='dispatch')
class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'blog/detail.html'

    # 得到Post实例复写get
    def get(self, request, *args, **kwargs):
        reponse = super().get(request, *args, **kwargs)

        self.object.increase_views()
        return reponse

    # def get_object(self,queryset=None):
    # 	post = super().get_object(queryset=None)
    # 	md=markdown.Markdown(extensions=[
    # 									'markdown.extensions.extra',
    # 									'markdown.extensions.codehilite',
    # 									TocExtension(slugify = slugify),
    # 								])
    # 	#post.increase_views()
    # 	post.body=md.convert(post.body)
    # 	post.toc=md.toc
    # 	return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CommentForm()
        if self.request.user.is_superuser:
            comment_list = self.object.comment_set.filter(is_reply=False).order_by('-created_time')
        else:
            comment_list = self.object.comment_set.filter(is_reply=False, is_check=True).order_by('-created_time')
        min_id = Post.objects.all().last().id
        max_id = Post.objects.all().first().id

        context.update({'form': form, 'comment_list': comment_list,
                        'next_post': self.next_post(self.object.id, min_id),
                        'prev_post': self.prev_post(self.object.id, max_id)
                        })
        return context

    def next_post(self, pk, min_id):  # pk=self.kwargs.get('pk')
        pk = pk - 1
        if pk >= min_id:
            if Post.objects.filter(id=pk).exists():
                return Post.objects.get(id=pk)
            else:
                return self.next_post(pk, min_id)

        else:
            return False

    def prev_post(self, pk, max_id):  # 获取上一文章
        pk = pk + 1
        if pk <= max_id:
            if Post.objects.filter(id=pk).exists():
                return Post.objects.get(id=pk)
            else:
                return self.prev_post(pk, max_id)
        else:
            return False


# def archives(request,year,month):
# 	post_list = Post.objects.filter(created_time__year=year,
# 									created_time__month=month
# 									)
# 	return render(request,'blog/index.html',context={'post_list':post_list})
def archives_list(request):
    menu_archive = True
    return render(request, 'blog/archives.html', {'menu_archive': menu_archive})


class ArchivesView(generic.ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        return Post.objects.filter(created_time__year=self.kwargs.get('year'),
                                   created_time__month=self.kwargs.get('month'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = context.get('object_list')

        for post in queryset:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            post.excerpt = md.convert(post.excerpt)

        return context


# def category(request,category_id):
# 	category_ob = get_object_or_404(Category,pk=category_id)
# 	post_list = Post.objects.filter(category_id=category_id)
# 	return render(request,'blog/index.html',context={'post_list':post_list})

def category_list(request):
    return render(request, 'blog/category.html', {})


class CategoryView(generic.ListView):
    # model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        # return generic.ListView.get_queryset(self).filter(category=cate)
        return Post.objects.all().filter(category=cate)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = context.get('object_list')

        for post in queryset:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            post.excerpt = md.convert(post.excerpt)

        return context


def tags_list(request):
    menu_tag = True
    return render(request, 'blog/tags.html', {'menu_tag': menu_tag})


class TagView(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))

        return Post.objects.all().filter(tags=tag)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = context.get('object_list')

        for post in queryset:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            post.excerpt = md.convert(post.excerpt)

        return context


@csrf_protect
def search_page(request):
    return render(request, 'blog/search_page.html', )
# def search(request):
# 	q=request.GET.get('q')
# 	error_msg = ''

# 	if not q:
# 		error_msg = "请输入关键词"
# 		return render(request,'blog/index.html',{'error_msg':error_msg})

# 	post_list = Post.objects.filter(Q(title__icontains=q)|Q(body__icontains=q))
# 	return render(request,'blog/index.html',{'error_msg':error_msg,'post_list':post_list})
