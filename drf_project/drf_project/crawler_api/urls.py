from django.urls import re_path,path,include
from crawler_api import views

urlpatterns=[
    # DRF에서는 url name에 list와 detail 사용
    # url에 pk가 없는 경우에는 list
    path('project/', views.ProjectListCreateAPIView.as_view(), name='project-list'),
    #path('project/<int:pk>', views.ProjectRetrieveAPIView.as_view(), name='project-detail'),
    #path('project/<int:project_pk>/crawler',views.CrawlerListCreateAPIView.as_view(), name='crawler-list'),
    #path('project/<int:project_pk>/crawler/',views.CrawlerListCreateAPIView.as_view(), name='crawler-list'),
    re_path(r'^project/(?P<project_pk>\d+)/crawler/?$', views.CrawlerListCreateAPIView.as_view(), name='crawler-list'),
    
    #path('project/<int:project_pk>/crawler/<int:pk>', views.CrawlerRetrieveUpdateAPIView.as_view(), name='crawler-detail'),
    #path('project/<int:project_pk>/image', views.ImageListAPIView.as_view(),name='image-list'),
    #path('project/<int:project_pk>/image/', views.ImageListAPIView.as_view(),name='image-list'),
    re_path(r'^project/(?P<project_pk>\d+)/image/?$', views.ImageListAPIView.as_view(), name='image-list'),
    re_path(r'^project/(?P<project_pk>\d+)/image/download/?$', views.ImageDownloadAPIView.as_view(), name='image-download'),
    #path('project/<int:project_pk>/tag', views.TagListAPIView.as_view(),name='tag-list'),
    #path('project/<int:project_pk>/tag/', views.TagListAPIView.as_view(),name='tag-list'),
    re_path(r'^project/(?P<project_pk>\d+)/tag/?$', views.TagListAPIView.as_view(), name='tag-list'),
    #path('project/<int:project_pk>/image/filtering', views.FilteredImageListAPIView.as_view(),name='filtered_image-list'),
]