from django.db import models
import datetime
from jsonfield import JSONField

class Project(models.Model):
    MODE_CHOICES=[
        ('Keyword','Keyword'),
        ('Tag','Tag')
    ]
    STATE_CHOICES=[
        ('Initialized','Initialized'),
        ('Running','Running'),
        ('Done','Done'),
        ('Stopped','Stopped')
    ]
    
    title = models.CharField('NAME',max_length=100, unique=True,help_text="생성할 프로젝트의 이름")
    mode = models.CharField('MODE',choices=MODE_CHOICES, max_length=20,help_text="생성할 프로젝트의 모드 (keyword/tag)")
    #keyword = models.TextField('KEYWORD',blank=True,help_text="프로젝트가 keyword 모드일 경우 수집할 검색어 목록(쉼표로 구분), tag 모드일 경우 빈칸") # save 시: list-> json, read 시: json->list
    state = models.CharField('STATE',choices=STATE_CHOICES,max_length=20, default='Initialized',help_text="프로젝트 진행 상태 (initialized/ running/ done/ stopped)")
    expected_total = models.IntegerField('TOTAL IMAGE',default=0,help_text="예상되는 이미지 수집 수")
    collected = models.IntegerField('COLLECTED',default=0,help_text="수집한 이미지/단어 개수")
    create_dt = models.DateTimeField('CREATE DT', auto_now_add=True,help_text="프로젝트 생성 날짜")
    elapsed = models.DurationField('ELAPSED TIME', default=datetime.timedelta(seconds=0),help_text="프로젝트 생성 후 경과 시간")
    remaining = models.DurationField('REMAINING TIME', default=datetime.timedelta(seconds=0),blank=True, help_text="프로젝트 실행 완료까지 남은 예상 시간")
    class Meta:
        ordering = ('create_dt',)

    def __str__(self):
        return self.title
    
class Crawler(models.Model):
    MODE_CHOICES=[
        ('Keyword','Keyword'),
        ('Tag','Tag')
    ]
    STATE_CHOICES=[
        ('Initialized','Initialized'),
        ('Running','Running'),
        ('Done','Done'),
        ('Stopped','Stopped')
    ]

    WEBSITE_CHOICES = [
        ('https://www.farfetch.com/kr/shopping/women/search/items.aspx', 'farfetch-women(keyword)'),
        ('https://www.farfetch.com/kr/shopping/men/search/items.aspx', 'farfetch-men(keyword)'),
        ('https://www.farfetch.com/kr/shopping/women/clothing-1/items.aspx', 'farfetch-women(tag)'),
        ('https://www.farfetch.com/kr/shopping/men/clothing-2/items.aspx', 'farfetch-men(tag)')
    ]
    
    project = models.ForeignKey('Project', on_delete=models.CASCADE,help_text="해당 크롤러가 할당되어있는 프로젝트의 키값")
    #mode = models.CharField('MODE',choices=MODE_CHOICES,max_length=200,help_text="해당 크롤러의 모드 (할당된 프로젝트의 모드와 같음)")
    keyword = models.TextField('KEYWORD',blank=True, help_text="프로젝트가 keyword 모드일 경우 수집할 검색어 목록(쉼표로 구분), tag 모드일 경우 빈칸") # list 아니고 string
    state = models.CharField('STATE',choices=STATE_CHOICES,max_length=20, default='Running',help_text="크롤러의 동작 상태 (iniialized/ running/ done/ stopped)")
    expected_total = models.IntegerField('TOTAL IMAGE',default=0,help_text="예상되는 이미지 수집 수")
    collected= models.IntegerField('COLLECTED',default=0,help_text="수집한 이미지/단어 개수")
    create_dt = models.DateTimeField('CREATE DT', auto_now_add=True,help_text="크롤러 생성 날짜")
    website = models.CharField('WEBSITE',choices=WEBSITE_CHOICES,max_length=200,help_text="크롤러가 수집하는 웹사이트 url")
    pid = models.IntegerField('PID', default=-1,help_text="크롤러 실행 중인 프로세스 ID")
    elapsed = models.DurationField('ELAPSED TIME',  default=datetime.timedelta(seconds=0),help_text="크롤러 생성 후 경과 시간")
    remaining = models.DurationField('REMAINING TIME',  default=datetime.timedelta(seconds=0),help_text="크롤러 실행 완료까지 남은 예상 시간")
    
    
    def __str__(self):
        return str(self.project) +" > "+ self.keyword + " > "+self.website +":" +self.state
    
class Image(models.Model):
    CUT_CHOICES=[
        ('Unfiltered', 'Unfiltered'), ('Outfit','Outfit'), ('Dummy','Dummy'),('Product','Product'),('Detail','Detail'),('Etc','Etc')
    ]
    PART_CHOICES=[
        ('Unfiltered', 'Unfiltered'), ('Full','Full'), ('Top','Top'),('Bottom','Bottom')
    ]
    DIRECTION_CHOICES=[
        ('Unfiltered', 'Unfiltered'), ('Front','Front'), ('Left_45','Left_45'),('Left','Left'),('Back','Back'),('Right','Right'),('Right_45','Right_45')
    ]
    POSE_CHOICES=[
        ('Unfiltered', 'Unfiltered'), ('Stand','Stand'),('Sit_in_chair','Sit_in_chair'),('Sit_in_floor','Sit_in_floor'),('Etc','Etc')
    ]
    IS_HEAD_CHOICES=[
        ('Unfiltered', 'Unfiltered'), ('Is_head','Is_head'), ('Not_head', 'Not_head')
    ]
    PERSON_COUNT_CHOICES=[
        ('Unfiltered', 'Unfiltered'), ('One','One'), ('Two_more','Two_more')
    ]
    
    project = models.ForeignKey('Project', on_delete=models.CASCADE, help_text="해당 이미지가 수집된 프로젝트의 키값")
    crawler = models.ForeignKey('Crawler', on_delete=models.CASCADE, help_text="해당 이미지가 수집된 크롤러의 키값")
    url = models.URLField('URL',help_text="이미지 원본 url") #img src url
    save_path = models.TextField('SAVE PATH', default='./images',help_text="이미지가 저장되어 있는 path")
    
    cut = models.CharField('CUT',default='Unfiltered',choices=CUT_CHOICES, max_length=20,blank=True, help_text="Outfit, Dummy, Product, Detail, Etc 중 택1")
    part = models.CharField('PART',default='Unfiltered',choices= PART_CHOICES, max_length=20,blank=True, help_text="Full, Top, Bottom 중 택1")
    direction = models.CharField('DIRECTION',default='Unfiltered',choices=DIRECTION_CHOICES, max_length=20,blank=True,help_text="Front, Left_45, Left, Back, Right, Right_45 항목 중 택1")
    pose = models.CharField('POSE',default='Unfiltered',choices=POSE_CHOICES, max_length=20,blank=True,help_text="Stand, Sit_in_chair, Sit_in_floor, Etc 중 택1")
    is_head = models.CharField('IS HEAD',default='Unfiltered',choices= IS_HEAD_CHOICES, max_length=20,blank=True,help_text="Head, Not_head 중 택1")
    person_count = models.CharField('PERSON COUNT',default='Unfiltered',choices=PERSON_COUNT_CHOICES,max_length=20, blank=True,help_text="One, Two_more 중 택1")
    
    def __str__(self):
        return self.url
    
class Tag(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    crawler = models.ForeignKey('Crawler', on_delete=models.CASCADE)
    tag = JSONField('TAG', default=dict, blank=True) 
    #top_n = models.IntegerField('TOP_N', default=0)

    def __str__(self):
        return self.crawler.website

