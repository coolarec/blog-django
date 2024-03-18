# views.py
from django.http import JsonResponse
from .models import Post, Category, Tag,Comment
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import json
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .serializers import PostSummarySerializer, PostDetailSerializer,UserSerializer,CommentSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
# from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, filters
# from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import make_password
from django.http import QueryDict
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator



#######################################
##                                   ##
##初稿，使用django原生程序来返回所有数据##
##                                   ##
#######################################


# def post_list_summary(request):
#     posts = Post.objects.all()

#     paginator = Paginator(posts, per_page=10)
#     page_number = request.GET.get('page', 1)  # 获取请求中的页码参数，默认为第一页
#     page_obj = paginator.get_page(page_number)

#     # 构造 JSON 响应数据
#     data = {
#         'count': paginator.count,  # 博文总数
#         'num_pages': paginator.num_pages,  # 总页数
#         'has_next': page_obj.has_next(),  # 是否有下一页
#         'has_previous': page_obj.has_previous(),  # 是否有上一页
#         'results': [
#             {
#                 'id': post.id,
#                 'title': post.title,
#                 'summary': post.summary,
#             }
#             for post in page_obj.object_list
#         ]
#     }

#     return JsonResponse(data)

# def post_list_full(request):
#     post_id = request.GET.get('id')  # 获取请求中的文章ID参数

#     try:
#         post = Post.objects.get(id=post_id)
#     except Post.DoesNotExist:
#         return JsonResponse({'error': 'Post not found'}, status=404)

#     # 构造 JSON 响应数据
#     data = {
#         'id': post.id,
#         'title': post.title,
#         'author': post.author,
#         'content': post.content,
#         'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
#         'updated_at': post.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
#         'tags': [tag.name for tag in post.tags.all()],
#         'category': post.category.name if post.category else None,
#         'views': post.views,
#         'likes': post.likes,
#         'summary': post.summary,
#         'reading_time': post.reading_time
#     }

#     return JsonResponse(data)

# def post_comments(request, post_id):
#     try:
#         post = Post.objects.get(pk=post_id)
#     except Post.DoesNotExist:
#         return JsonResponse({'error': 'Post not found'}, status=404)
#     comments = Comment.objects.filter(post=post)
#     # 构造 JSON 响应数据
#     data = {
#         'post_title': post.title,
#         'comments': [
#             {
#                 'author': comment.author,
#                 'email': comment.email,
#                 'content': comment.content,
#                 'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
#             }
#             for comment in comments
#         ]
#     }
#     return JsonResponse(data)


# def create_new_post(title, author, content, category_name=None, tag_names=None, summary='', reading_time=0):
#     # 创建博文对象
#     post = Post(title=title, author=author, content=content, summary=summary, reading_time=reading_time)
#     # 获取或创建分类对象
#     category = None
#     if category_name:
#         category, _ = Category.objects.get_or_create(name=category_name)
#         post.category = category

#     # 获取或创建标签对象
#     if tag_names:
#         tags = [Tag.objects.get_or_create(name=tag_name)[0] for tag_name in tag_names]
#         post.tags.add(*tags)

#     # 保存博文对象到数据库
#     post.save()

#     return post


# def update_post(post_id, title=None, author=None, content=None, category_name=None, tag_names=None, summary=None, reading_time=None):
#     try:
#         # 获取已存在的文章对象
#         post = Post.objects.get(pk=post_id)
#     except Post.DoesNotExist:
#         return None  # 如果文章不存在，则返回 None

#     # 更新文章的属性值
#     if title is not None:
#         post.title = title
#     if author is not None:
#         post.author = author
#     if content is not None:
#         post.content = content
#     if summary is not None:
#         post.summary = summary
#     if reading_time is not None:
#         post.reading_time = reading_time

#     # 获取或创建分类对象，并关联到文章
#     if category_name:
#         category, _ = Category.objects.get_or_create(name=category_name)
#         post.category = category

#     # 获取或创建标签对象，并关联到文章
#     if tag_names:
#         tags = [Tag.objects.get_or_create(name=tag_name)[0] for tag_name in tag_names]
#         post.tags.set(tags)

#     # 保存更新后的文章对象到数据库
#     post.save()

#     return post  # 返回更新后的文章对象

# @require_GET
# def add_post(request):
#     # 从请求参数中获取文章信息
#     title = request.GET.get('title')
#     author = request.GET.get('author')
#     content = request.GET.get('content')
#     category_name = request.GET.get('category')
#     tag_names = request.GET.getlist('tags')
#     summary = request.GET.get('summary', '')
#     reading_time = int(request.GET.get('reading_time', 0))

#     # 检查必要参数是否存在
#     if not title or not author or not content:
#         return JsonResponse({'error': 'Title, author, and content are required'}, status=400)

#     # 创建新的博文对象
#     new_post = create_new_post(title, author, content, category_name, tag_names, summary, reading_time)

#     return JsonResponse({'success': 'Post created successfully', 'post_id': new_post.id})

@ensure_csrf_cookie
def signin(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        # username = request.POST.get('username')
        # password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)  # 登录用户并创建 session

            # 设置 cookies
            response = JsonResponse({'message': 'Login successful'}, status=200)
            response.set_cookie('username', username,max_age=30*24*60*60)
            return response
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    


# def signup(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         email = request.POST['email']
#         is_staff = request.POST.get('is_staff', False)  # 默认为普通用户

#         # 创建用户
#         user = User.objects.create_user(username=username, email=email, password=password, is_staff=is_staff)
        
#         # 可以根据需要进行额外的操作，比如登录用户
#         signin(request)
#         return JsonResponse({'message': 'register successful'}, status=200)
#     else:
#         return JsonResponse({'error': 'Invalid credentials'}, status=401)


class PostModelPagination(PageNumberPagination):
    page_size = 10  # 每页的大小
    page_size_query_param = 'page_size'
    max_page_size = 1000  # 每页最大大小限制

@method_decorator(ensure_csrf_cookie, name='dispatch')
class PostSummaryList(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-updated_at')
    pagination_class = PostModelPagination
    serializer_class = PostSummarySerializer
    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return []
        else:
            return [IsAuthenticated()]
    authentication_classes = [SessionAuthentication, BasicAuthentication]



@method_decorator(ensure_csrf_cookie, name='dispatch')
class PostDetailRetrieve(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-updated_at')
    pagination_class = PostModelPagination
    serializer_class = PostDetailSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['content', 'title', 'authorname']
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        instance = serializer.save()
        instance.author = self.request.user
        instance.save()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not request.user.is_superuser and request.user != instance.author:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not request.user.is_superuser and request.user != instance.author:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
    
class CommentRetrieve(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.request.query_params.get('post_id')
        if post_id:
            return Comment.objects.filter(post=post_id).order_by('-created_at')
        return Comment.objects.all().order_by('-created_at')


@method_decorator(ensure_csrf_cookie, name='dispatch')
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create':
            return []
        return super().get_permissions()
    

    def create(self, request):
        request.data['password'] = make_password(request.data['password'])
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            login(request,user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        user = self.get_object()
        
        if request.user.is_superuser:
            mutable_data = request.data.copy()
            if isinstance(mutable_data, QueryDict):
                mutable_data._mutable = True
            if 'password' in mutable_data and mutable_data['password']:
                mutable_data['password'] = make_password(mutable_data['password'])
            serializer = UserSerializer(user, data=mutable_data)
            if isinstance(mutable_data, QueryDict):
                mutable_data._mutable = False
        else:
            # 普通用户只能修改自己的账号
            if request.user == user:
                mutable_data = request.data.copy()
                if 'password' in mutable_data and mutable_data['password']:
                    mutable_data['password'] = make_password(mutable_data['password'])
                serializer = UserSerializer(user, data=mutable_data)
            else:
                return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        user = self.get_object()
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)