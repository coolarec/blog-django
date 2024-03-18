from django.contrib import admin
from django.urls import path, re_path, include
# from api.views import post_comments, post_list_full, post_list_summary, add_post, signin, signup, PostSummaryList, PostDetailRetrieve
# from api.views import post_comments, add_post, signin, signup, PostSummaryList, PostDetailRetrieve,UserViewSet
from api.views import  signin,PostSummaryList, PostDetailRetrieve,UserViewSet,CommentRetrieve

from .views import index
from rest_framework import routers
from rest_framework.documentation import include_docs_urls

router = routers.DefaultRouter()
router.register(r'posts', PostSummaryList,basename='posts')
router.register(r'post', PostDetailRetrieve, basename='post')  # 使用basename指定视图名称
router.register(r'user',UserViewSet,basename='user')
router.register(r'comment',CommentRetrieve,basename='comment')

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('post/id', post_list_full),
    # path('post/all', post_list_summary),
    # path('post/add/', add_post, name='add_post'),
    # path('user/register', signup),
    path('user/login', signin),
    path('api/', include(router.urls)),
    path('docs/',include_docs_urls(title='API',description='blog api速览')),
    re_path(r'^(?!api|user|docs).*$', index),
]
