from rest_framework import serializers
from django.contrib.auth.models import User
from crawler.models import *

# Serializer: 출력 포맷이나 출력 내용에 관한 것 다 포함시킴

class ProjectCreateSerializer(serializers.ModelSerializer): # HyperlinkedModelSerializer보다 ModelSerializer를 더 많이 사용
    '''
    프로젝트 생성을 위한 serializer
    '''
    class Meta:
        model = Project
        fields = ['title','mode'] # Client에게 보낼 field 지정
        #exclude=('collected','state','create_dt')
        write_only_fields = '__all__'
        
class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__' 
    
    
# class ProjectRetrieveSerializer(serializers.ModelSerializer): 
#     class Meta:
#         model = Project
#         fields = '__all__'
        
class CrawlerCreateSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Crawler
        #fields = '__all__'
        #exclude=("project","state","collected","create_dt","pid")
        fields=['project', 'keyword','website']
        
class CrawlerListSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Crawler
        fields = '__all__'
        
# class CrawlerRetrieveSerializer(serializers.ModelSerializer): 
#     class Meta:
#         model = Crawler
#         fields = '__all__'
        
        
# class CrawlerUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Crawler
#         field=['state']
    
    
class ImageListSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Image
        fields = '__all__'

class FilteredImageListSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Image
        fields = '__all__'
        
class ImageRetrieveSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Image
        fields = '__all__'
        
class TagListSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Tag
        fields = ['tag']

# class TagRetrieveSerializer(serializers.ModelSerializer):
#     class Meta:
#         model =  Tag
#         fields = '__all__'
