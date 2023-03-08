from django.shortcuts import render
import subprocess
from crawler_api.params import *
from rest_framework.generics import GenericAPIView,ListAPIView,RetrieveUpdateAPIView,RetrieveAPIView,ListCreateAPIView, UpdateAPIView
from crawler_api.serializer import *
from crawler.models import Project, Crawler, Image
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from rest_framework import status
from django.views import View
from rest_framework.views import APIView
from drf_yasg.utils       import swagger_auto_schema
from drf_yasg             import openapi  
from crawler.models import *
from crawler_api.filters import *
from django.urls import re_path
import json
from io import BytesIO
import zipfile
from django.http import HttpResponse
import requests
from rest_framework.parsers import JSONParser
from io import BytesIO #IO를 담당하는 class
import asyncio
from aiohttp import ClientSession
from asgiref.sync import sync_to_async
import logging
#from swagger.serializers import GetRequestSerializer, GetResponseSerializer
logger = logging.getLogger('django')
websites={ # registered websites to crawl
            "a.com": "aa.py",
            "b.com": "bb.py"
            } 

class ProjectListCreateAPIView(ListCreateAPIView):
    queryset = Project.objects.all()
    #serializer_class = ProjectListCreateSerializer
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProjectListSerializer
        elif self.request.method == 'POST':
            return ProjectCreateSerializer
        
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        description='현재까지 생성된 프로젝트 목록',
        responses={status.HTTP_200_OK:openapi.Response(
            description= "Successful retrival of project list",
            schema=ProjectListSerializer(many=True)
        )},
        tags=['Project'],
        operation_description='현재까지 생성된 프로젝트 목록 불러오기'
    )
    def get(self, request, *args, **kwargs):
        '''
        현재까지 생성된 모든 프로젝트 리스트
        '''
       
        return self.list(request, *args, **kwargs)
   
    @swagger_auto_schema(
        description='새 프로젝트 생성',
        #manual_parameters=[
        #    projecttitle_param, projectmode_param,projectkeyword_param
        #],
        #query_serializer=ProjectCreateSerializer,
        request_body=ProjectCreateSerializer,
        #responses={status.HTTP_200_OK:ProjectCreateSerializer},
        responses={status.HTTP_201_CREATED:openapi.Response(
            description= "Successfully created new project",
            #schema=ProjectListSerializer(many=False)
        )},
        tags=['Project'],
        operation_description='새 프로젝트 생성'
    )
    def post(self, request, *args, **kwargs):
        '''
        새 프로젝트 생성
        '''
        return self.create(request, *args, **kwargs)
    

class CrawlerListCreateAPIView(ListCreateAPIView):
    queryset = Crawler.objects.all()
    #serializer_class = CrawlerListCreateSerializer
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CrawlerListSerializer
        elif self.request.method == 'POST':
            return CrawlerCreateSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return Crawler.objects.filter(project_id=self.kwargs['project_pk'])
    
    @swagger_auto_schema(
        description='특정 프로젝트에 속한 크롤러 리스트 불러오기',
        manual_parameters=[
            openapi.Parameter(
                'project_pk',openapi.IN_PATH, description="프로젝트 primary key 지정",type=openapi.TYPE_INTEGER),
        ],
        responses={status.HTTP_200_OK:openapi.Response(
            description= "Successful retrival of crawler list of a project",
            schema=CrawlerListSerializer(many=True)
        )},
        tags=['Crawler'],
        operation_description='특정 프로젝트에 속한 크롤러 리스트 불러오기'
    )   
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    
    async def run_crawler(self, instance):
            if instance.project.mode == 'Keyword' : 
                instance_id = instance.id
                instance_project_id = instance.project.id
                instance_website = instance.website
                instance_keyword = instance.keyword
                    
                process = await asyncio.create_subprocess_exec(
                    'python', './crawler/src/keyword/farfetch_crawler.py', 
                    str(instance_id),
                    str(instance_project_id),
                    str(instance_website),
                    str(instance_keyword),
                    #stdout=asyncio.subprocess.PIPE,
                    #stderr=asyncio.subprocess.PIPE
                )
                
            else : 
                instance_id = instance.id
                instance_project_id = instance.project.id
                instance_website = instance.website

                process = await asyncio.create_subprocess_exec(
                    'python', './crawler/src/tag/farfetch_crawler.py', 
                    str(instance_id),
                    str(instance_project_id),
                    str(instance_website),
                    #stdout=asyncio.subprocess.PIPE,
                    #stderr=asyncio.subprocess.PIPE
                )
            
            pid=process.pid
            print(f'Process ID: {pid} running')
            #ins = Crawler.objects.get(id=instance_id)
            
            ins = await sync_to_async(Crawler.objects.get)(id=instance_id)
            
            print(f"pid:{pid}, {type(pid)}")
            print(f"instance_id:{instance_id}, {type(instance_id)}")
            ins.pid = pid #pid값 update
            print(f"ins.pid={ins.pid}")
            await sync_to_async(ins.save)()
            
            
    def perform_create(self, serializer):
        '''
        크롤러 생성 시 생성되는 instance를 크롤러 소스 .py의 argument로 넘겨주고 실행함
        '''
        instance = serializer.save()
        print(f"instance.mode : {instance.project.mode}")
        print('start crawling...')
        asyncio.run(self.run_crawler(instance))
       
    def create(self, request, *args, **kwargs):
        copied_data=request.data.copy()
        copied_data['project']=self.kwargs['project_pk']
        serializer = self.get_serializer(data=copied_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return HttpResponseRedirect('/crawler_api/project/{}/crawler/'.format(copied_data['project']))
        
        # async def run_response():
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        # return asyncio.run(run_response())

     
    @swagger_auto_schema(
        description='크롤러 생성 요청',
        responses={status.HTTP_200_OK:openapi.Response(
            description= "Successfully created new crawler",
            #schema=CrawlerCreateSerializer(many=False)
        )},
        #responses={status.HTTP_200_OK:CrawlerCreateSerializer},
        tags=['Crawler'],
        operation_description='크롤러 생성 요청'
    )   

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
        
class ImageListAPIView(ListAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageListSerializer

    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_class = ImageFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        description='특정 프로젝트에서 수집된 이미지 목록',
        manual_parameters=[
            openapi.Parameter(
                'project_pk',openapi.IN_PATH, description="프로젝트 primary key 지정",required=True,type=openapi.TYPE_INTEGER),
            openapi.Parameter(
                'cut',openapi.IN_QUERY, description="cut 필터링 값 (Outfit, Dummy, Product, Detail, Etc 중 하나)",required=True,type=openapi.TYPE_STRING),
            openapi.Parameter(
                'part',openapi.IN_QUERY, description="part 필터링 값 (Full, Top, Bottom 중 하나)",required=True,type=openapi.TYPE_STRING),
            openapi.Parameter(
                'direction',openapi.IN_QUERY, description="direction 필터링 값 (Front, Left_45, Left, Back, Right, Right_45 중 하나)",required=True,type=openapi.TYPE_STRING),
            openapi.Parameter(
                'pose',openapi.IN_QUERY, description="pose 필터링 값 (Stand, Sit_in_chair, Sit_in_floor, Etc 중 하나)",required=True,type=openapi.TYPE_STRING),
             
            openapi.Parameter(
                'is_head',openapi.IN_QUERY, description="is_head 필터링 값 (Is_head, Not_head 중 하나)",required=True,type=openapi.TYPE_STRING),
            openapi.Parameter(
                'person_count',openapi.IN_QUERY, description="person_count 필터링 값 (One, Two_more 하나)",required=True,type=openapi.TYPE_STRING),

        ],
        responses={status.HTTP_200_OK:openapi.Response(
            description= "Successful retrieval of image list",
            schema=ImageListSerializer(many=True)
        )},
        tags=['Image'],
        operation_description='특정 프로젝트에서 수집된 이미지 목록'
    ) 
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    

class ImageRetrieveAPIView(RetrieveAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageRetrieveSerializer
    
class TagListAPIView(ListAPIView):
    #queryset = Tag.objects.all()
    serializer_class = TagListSerializer
    
    def get_queryset(self):
        queryset = Tag.objects.filter(project_id=self.kwargs['project_pk'])
        return queryset
    
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()[0]
            top_n = self.request.query_params.get('top_n', 10)
            json_data = json.loads(queryset.tag)
            sorted_tags = sorted(json_data.items(), key=lambda item: item[1], reverse=True)[:int(top_n)]
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True) # Only one instance

            return Response(sorted_tags)
        except:
            return HttpResponse('No tags crawled')
    
    @swagger_auto_schema(
        description='태그 크롤러가 수집한 태그 결과',
        manual_parameters=[
            openapi.Parameter(
                'project_pk',openapi.IN_PATH, description="프로젝트 primary key 지정",type=openapi.TYPE_INTEGER),
            openapi.Parameter(
                'top_n',openapi.IN_QUERY, description="수집된 태그 중 상위 top_n개만 나열할 때 top_n 값",required=True,type=openapi.TYPE_INTEGER),
        ],
        responses={status.HTTP_200_OK:TagListSerializer(many=True)},
        tags=['Tag'],
        operation_description='태그 크롤러가 수집한 태그 결과'
    )  
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class ImageDownloadAPIView(APIView):
    
    @swagger_auto_schema(
        description='특정 프로젝트에서 수집된 이미지 zip 파일로 다운로드',
        manual_parameters=[
            openapi.Parameter(
                'project_pk',openapi.IN_PATH, description="프로젝트 primary key 지정",required=True,type=openapi.TYPE_INTEGER),
            openapi.Parameter(
                'cut',openapi.IN_QUERY, description="cut 필터링 값 (Outfit, Dummy, Product, Detail, Etc 중 하나)",required=True,type=openapi.TYPE_STRING),
            openapi.Parameter(
                'part',openapi.IN_QUERY, description="part 필터링 값 (Full, Top, Bottom 중 하나)",required=True,type=openapi.TYPE_STRING),
            openapi.Parameter(
                'direction',openapi.IN_QUERY, description="direction 필터링 값 (Front, Left_45, Left, Back, Right, Right_45 중 하나)",required=True,type=openapi.TYPE_STRING),
            openapi.Parameter(
                'pose',openapi.IN_QUERY, description="pose 필터링 값 (Stand, Sit_in_chair, Sit_in_floor, Etc 중 하나)",required=True,type=openapi.TYPE_STRING),
             
            openapi.Parameter(
                'is_head',openapi.IN_QUERY, description="is_head 필터링 값 (Is_head, Not_head 중 하나)",required=True,type=openapi.TYPE_STRING),
            openapi.Parameter(
                'person_count',openapi.IN_QUERY, description="person_count 필터링 값 (One, Two_more 하나)",required=True,type=openapi.TYPE_STRING),

        ],
        responses={status.HTTP_200_OK:openapi.Response(
            description= "Successful download of images"
        )},
        tags=['Image'],
        operation_description='특정 프로젝트에서 수집된 이미지 zip 파일로 다운로드'
    ) 

    def get(self, request, *args, **kwargs):
        project_id=self.kwargs['project_pk']
        project_title=Project.objects.filter(id=self.kwargs['project_pk']).first().title
        
        query_params = request.query_params.dict()
        filtered_img_json = requests.get(f'http://127.0.0.1:8000/crawler_api/project/{project_id}/image', params=query_params).content
        
        filtered_img_list = JSONParser().parse(BytesIO(filtered_img_json))  # list
        print(f"response:{type(filtered_img_list)}")
        
        image_paths = [image_data.get('save_path') for image_data in filtered_img_list]
        
        
        # Create a response object
        response = HttpResponse(content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{project_title}_images.zip"'
        
        # Zip the images and write to response
        buffer = BytesIO()
        with zipfile.ZipFile(buffer, "w") as z:
            for image_path in image_paths:
                z.write(image_path)
        buffer.seek(0)
        response.write(buffer.read())
        
        return response
    