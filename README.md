# studio_lab
This is my internship record for 2 months(studiolab ML team)

## Main tasks
1. Color Extraction
2. Crawler 관리 페이지 개발(Django Rest Framework)

# Color Extraction

의류 상세 페이지 내 의류 이미지가 어떤 색상의 옷인지에 대한 정보 제공을 위해서 의류 이미지 색상 추출 업무를 진행
RGB 이미지의 각 픽셀을 기준으로 K-means clustering을 통해 의류 이미지의 객체에 대해 k개의 색상 추출을 진행

- **K-means**
    
    K-means 알고리즘은 데이터를 k개의 군집(cluster)로 clustering하는 알고리즘이다. K-means 알고리즘에서 k는 묶을 군집(클러스터)의 개수를 의미하고 means는 평균을 의미한다. 즉, K-means 알고리즘은 비슷한 특성을 지닌 데이터들끼리 묶어 k개의 군집으로 군집화하는 대표적인 군집화 기법이다. K-means 알고리즘은 군집의 개수 k를 설정한 후 초기 중심점(centriod)를 설정하고 데이터를 각 군집에 할당한다. 데이터가 할당되면 데이터의 평균을 계산해 군집 중심점을 갱신하고 데이터를 각 군집에 재할당한다. 이 과정을 멈춤 조건(군집 중심점의 갱신이 더 이상 이뤄지지 않을 때)을 만족할 때까지 반복한다. 
    
    ```python
    grid = GridSearchCV(estimator, param_grid = param_grid) 
    grid.fit(img_data)
    print(grid.best_params_)
    
    cluster_num = grid.best_params_['n_clusters']
    
    clustering = KMeans(n_clusters = cluster_num, init = 'k-means++')
    clustering.fit(img_data)
    ```
    
기존에 이미 구현된 Python의 라이브러리 extcolors를 사용해서 색상 추출을 진행한 결과와 비교했을 때 속도는 좀 더 느리지만, 성능이 더 좋다고 판단된다. 색상 추출 결과는 Image segmentation의 성능에 따라서 달라질 수 있는데, 결과를 비교해보면 extcolors에 비해 좀 더 robust하다고 판단할 수 있다.

```python
import extcolors
from PIL import Image

img = Image.open('/Users/kyebeomjeon/workspace/Studio_Lab/saved_png/removed_bg_28.png').convert('RGBA')
colors, pixel_count = extcolors.extract_from_image(img, limit = 5)
```
대상 의류 이미지<br/>
<img src="https://user-images.githubusercontent.com/96854885/227513732-3576047f-5fa5-4849-a2df-e29899119b0d.png" width="300" height="300"/>
<img src="https://user-images.githubusercontent.com/96854885/227514346-89ded40c-4fc5-4f8a-a6a7-02bd18eb38ab.png" width="300" height="300"/><br/>

extcolors 라이브러리를 사용한 결과<br/>
<img src="https://user-images.githubusercontent.com/96854885/227513789-dedd9b2e-2699-4842-aa78-ef35b68fb719.png" width="300" height="300"/>
<img src="https://user-images.githubusercontent.com/96854885/227514393-6572956a-9ae7-417b-acc4-23d85993403e.png" width="300" height="300"/><br/>

직접 색상 추출을 진행한 결과<br/>
<img src="https://user-images.githubusercontent.com/96854885/227513846-eccf583f-6f27-429f-9f76-43cde3040eae.png" width="300" height="300"/>
<img src="https://user-images.githubusercontent.com/96854885/227514443-d943c672-3146-4be6-8e93-041076687303.png" width="300" height="300"/><br/>

해당 이미지는 쇼핑몰의 의류 이미지를 크롤링한 이미지 데이터로 이미지 내 객체에 대해서만 색상을 추출하기 위해서 image segmentation을 통해 이미지에 대해 전처리하는 과정을 진행한 후 clustering 진행

색상 추출 과정 중 이미지에 배경이 포함되는 경우에 배경색이 결과에 포함될 수 있기 때문에 모든 이미지에 대해 객체를 제외하고 배경을 제거하는 전처리 과정을 진행 
→ 이미지 pixel 전체에 걸쳐 객체를 구분하고, 객체를 제외한 부분은 masking 처리해 제거 (GrabCut 알고리즘 적용)
- GrabCut 알고리즘
        
openCV의 cv2.grabCut 활용
        
grabcut은 그래프 컷(graph cut)기반 영역 분할 알고리즘으로 그래프 알고리즘에서 사용되는 미니멀 컷 알고리즘을 이용해서 영역을 분할한다. 
        
→ 영상의 픽셀을 그래프 정점으로 간주하고, 픽셀들을 두 개의 그룹(객체 그룹, 배경 그룹)으로 분할하는 최적의 컷(Max Flow Minimum Cut)을 찾는 방식
        
Canny edge detection을 활용해 이미지 내 객체의 윤곽선을 검출한 후 해당 객체를 최대한 포함하면서, 가장 작은 bounding box를 찾아 배경과 객체를 구분해 grabcut 알고리즘을 적용한다. 이때, 이미지에서 노이즈가 있을 경우 윤곽선 검출이 어려울 수 있기 때문에 gaussian filter를 적용해 이미지의 노이즈를 줄인다. 이후 openCV의 cv2.Canny를 활용해 윤곽선을 검출한다.

Canny를 활용한 윤곽선 검출<br/>
![a](https://user-images.githubusercontent.com/96854885/227515784-aadbc162-50fc-457d-8218-14e184ceb336.png)  
    
bounding box 예시<br/>
![b](https://user-images.githubusercontent.com/96854885/227515860-f155b0f6-c343-4a1e-be81-1482b8395d83.png)
 
원본 이미지<br/>
![Untitled4](https://user-images.githubusercontent.com/96854885/227515144-fd24f783-aeef-4d6d-baab-8ce99648b2b8.png)
    
마스크 이미지<br/>
![Untitled5](https://user-images.githubusercontent.com/96854885/227515193-ac86b502-8b71-4297-aac7-8b9d111d4f06.png)
 
전처리 후 이미지<br/>
![Untitled6](https://user-images.githubusercontent.com/96854885/227515239-a151daf6-08c4-419f-bab7-2f50aaf5fc11.png)  
    
문제점) 하지만, grabcut의 경우 배경이 완벽하게 제거되지 않는다는 문제점과 초기 bounding box에 의해 성능이 좌우된다는 문제점이 있어, 좀 더 배경을 완벽하게 제거하기 위해 기존에 구현된 rembg 라이브러리를 활용해 전처리 진행했다. rembg는 딥러닝 모델 중 U2-net을 활용해 배경을 제거한다. 총 830장의 label이 없는 RGB 3 채널 의류 이미지에 대해  rembg 라이브러리를 활용해 RGBA 4 채널 의류 이미지 PNG파일로 변환했다.
    
```python
import numpy as np
from rembg import remove
import cv2
if __name__ == "__main__":
    input_path = '/content/drive/MyDrive/Studio_Lab/test_image_2.jpeg'
    output_path = '/content/drive/MyDrive/Studio_Lab/remove_bg_test.png'
    input = cv2.imread(input_path)
    output = remove(input)
    cv2.imwrite(output_path, output)
```
<결과 이미지>   
<img src="https://user-images.githubusercontent.com/96854885/227516160-80701473-10d3-41f9-8d42-4b9f6e763ac1.png" width="300" height="300"/>

하지만, clustering의 경우 unsupervised learning에 해당하기 때문에 추출된 색상이 얼마나 잘 추출된 것인지에 대한 평가 기준이 모호했고, 도출된 결과를 평가하기 위한 방법을 고민하는 과정에서 정량적인 방법은 아니지만 clustering된 전체 픽셀 중에서 각각의 특정 색상(cluster)에 속하는 픽셀을 제외하고 masking처리를 한다면 어떤 픽셀을 어떤 색상에 clustering한 것인지 설명이 가능하도록 하는 것이 가능할 것이라고 생각했다. 이를 기준으로 결과를 평가했다. 이를 활용해 이미지에서 어둡거나 그늘진 부분이나 이미지 전처리 과정에서 발생한 오류를 결과에서 배제하기 위해 일부 픽셀을 제거하고 clustering을 반복적으로 진행함으로써 성능을 개선했다. 하지만, K-means 알고리즘의 특성 상 결과가 k에 의존적이라는 근본적인 문제점은 있었다. 적절한 k를 찾기 위해 사이킷런의 gridsearch 방법을 활용했고 이미지에서 최대 5개의 색상을 추출하는 업무를 진행했다. 

**<최종 결과>**

대상 이미지에서 어떤 픽셀을 참고해 5개의 색상을 최종적으로 추출했는지 알 수 있다. 최종적으로는 RGB 값을 hex코드로 변환했다. 추출된 색상과 팬톤 컬러를 매칭해 정보를 제공할 예정이다.

```python
def rgb_to_hex(r, g, b) :
    r, g, b = int(r), int(g), int(b)
    return '#' + hex(r)[2:].zfill(2) + hex(g)[2:].zfill(2) + hex(b)[2:].zfill(2)
```

대상 이미지 및 색상 추출 결과<br/>
<img src="https://user-images.githubusercontent.com/96854885/227522056-5ccef4ca-d29f-4646-ae2f-14842ad5d2f7.png" width="300" height="300"/>
<img src="https://user-images.githubusercontent.com/96854885/227522117-ea5a907b-6372-4f49-82a2-a08ae83690bc.png" width="300" height="300"/>

hex code = [#133490, #161b27, #e6371e, #255fde, #3e773e]<br/>
<img src="https://user-images.githubusercontent.com/96854885/227522201-16316e60-a2f3-4bd7-9823-2b81b10ce3be.png" width="200" height="200"/>
<img src="https://user-images.githubusercontent.com/96854885/227522243-32cb3af1-d08f-4bb3-9faf-5cab09a5c272.png" width="200" height="200"/>
<img src="https://user-images.githubusercontent.com/96854885/227522297-118e1c3b-d345-4478-a4be-7802f1dfb8ef.png" width="200" height="200"/>
<img src="https://user-images.githubusercontent.com/96854885/227522347-cac8b9af-5034-431b-939f-281ab973609e.png" width="200" height="200"/>
<img src="https://user-images.githubusercontent.com/96854885/227522386-e202305d-5cde-4252-9874-3685494032a3.png" width="200" height="200"/>


# crawler 관리페이지 개발  
초기에는 다양한 쇼핑몰의 크롤러를 개발해 하나의 컴퓨터에서 multi-thread을 활용해 병렬적으로 처리하거나 AWS의 EC2를 활용해 여러 개의 크롤러를 동시에 구현  
하지만, 크롤링된 이미지를 데이터팀과 공유하고 이미지들을 pose-compositon model을 활용해 filtering하는 과정에서 비효율적인 업무를 자동화하기 위해 다수의 크롤러를 생성하고 구동하는 것을 시작으로 크롤링된 이미지를 필터링, 다운로드까지 하나의 pipeline으로 진행하기 위해 django와 django rest framework를 활용해 크롤러 관리 페이지 개발<br/>
<DB 구조>
<img width="478" alt="스크린샷 2023-04-11 시간: 17 44 07" src="https://user-images.githubusercontent.com/96854885/231106121-0ca9aef3-67c9-42cc-9890-be62f0745512.png">

<서버 실행><br/>
```bash
python manage.py runserver
```
- 주요 기능 소개  
1. swagger
2. 여러 쇼핑몰 내 이미지와 텍스트 크롤링할 수 있는 크롤러 다중 생성(하나의 프로젝트에 여러 개 크롤러 생성 가능, 여러 프로젝트에 여러 개 크롤러 생성 가능)  
3. 쇼핑몰 별, 어트리뷰트(플레어스커트, 펜슬스커트 등) 별, 이미지 또는 텍스트 별 프로젝트 다중 생성(Project 예시: farfetch몰의 플레어스커트 이미지 크롤링) -- 어트리뷰트는 사전 정의된 어트리뷰트 사용 
4. 프로젝트 단위로 크롤러 생성 관리 및 크롤링된 이미지 및 텍스트 데이터 관리(각 크롤러는 비동기 방식으로 처리)  
5. 크롤링된 이미지 및 텍스트 조회 및 삭제 기능  
6. batch program 구현(5초마다 각 크롤러들의 상태(run, stopped 등), 수집된 데이터 수, 진행 시간, 남은 시간 업데이트) -- python manage.py run_batch 명령어 실행   
```bash
python manage.py run_batch
```
7. 크롤링된 이미지 DB에 저장 및 mysql 연동  
8. 크롤링된 이미지 어트리뷰트 기준 또는 모델 유무, 모델의 포즈 기준으로 필터링 후 .zip 파일로 다운로드  
9. 최종 개발 완료된 페이지 배포(AWS)
