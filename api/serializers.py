from rest_framework import serializers
from .models import Post, Tag, Category, Comment
from django.contrib.auth.models import User


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'  # 根据需求添加其他字段


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'email', 'content', 'created_at']


class PostSummarySerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'author', 'created_at', 'tags', 'category']


class PostDetailSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    authorname = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'author', 'content', 'created_at', 'updated_at', 'tags', 'category', 'views', 'likes', 'summary', 'comments','authorname']

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     current_user = self.context['request'].user
    #     data['current_user'] = current_user.id if current_user.is_authenticated else None
    #     return data
    
    def get_authorname(self, obj):
        return obj.author.username if obj.author else None