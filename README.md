# studio_lab
This is my internship record for 2 months(studiolab ML team)

## Main tasks
1. color extraction  
<https://www.notion.so/Color-Extraction-02eba4ada63745b891b58b3684986103?pvs=4>  
쇼핑몰의 의류 상세 페이지 내 의류 이미지가 어떤 색상의 옷인지에 대한 정보 제공을 위해서 의류 이미지 색상 추출 업무를 진행  
RGB 이미지의 각 픽셀을 기준으로 K-means clustering을 통해 의류 이미지의 객체에 대해 k개의 색상 추출을 진행 
의류 이미지는 쇼핑몰의 의류 이미지를 크롤링한 이미지 데이터로 이미지 내 객체에 대해서만 색상을 추출하기 위해서 image segmentation을 통해 이미지에 대해 전처리하는 과정을 진행한 후 clustering 진행
최종적으로 추출된 결과를 디자인팀과 회의를 통해 결정된 최종 32개의 컬러 라벨 중 하나로 매칭    
기존에 이미 구현된 Python의 라이브러리 extcolors를 사용해서 색상 추출을 진행한 결과와 비교했을 때 속도는 좀 더 느리지만, 성능이 더 좋다고 판단된다. 색상 추출 결과는 Image segmentation의 성능에 따라서 달라질 수 있는데, 결과를 비교해보면 extcolors에 비해 좀 더 robust하다고 판단할 수 있다.  
문제점 및 해결방안)  
하지만, clustering의 경우 unsupervised learning에 해당하기 때문에 추출된 색상이 얼마나 잘 추출된 것인지에 대한 평가 기준이 모호했고, 도출된 결과를 평가하기 위한 방법을 고민하는 과정에서 정량적인 방법은 아니지만 clustering된 전체 픽셀 중에서 각각의 특정 색상(cluster)에 속하는 픽셀을 제외하고 masking처리를 한다면 어떤 픽셀을 어떤 색상에 clustering한 것인지 설명이 가능하도록 하는 것이 가능할 것이라고 생각했다. 이를 기준으로 결과를 평가했다. 이를 활용해 이미지에서 어둡거나 그늘진 부분이나 이미지 전처리 과정에서 발생한 오류를 결과에서 배제하기 위해 일부 픽셀을 제거하고 clustering을 반복적으로 진행함으로써 성능을 개선했다. 하지만, K-means 알고리즘의 특성 상 결과가 k에 의존적이라는 근본적인 문제점은 있었다. 적절한 k를 찾기 위해 사이킷런의 gridsearch 방법을 활용했고 이미지에서 최대 5개의 색상을 추출하는 업무를 진행했다.  
결과 예시)  
전처리 후 예시 이미지는 다음과 같다  
![test_image_1](https://user-images.githubusercontent.com/96854885/223710985-8f586d8b-7e28-473e-9ef0-2f4b4dd6cdf8.png)  
위에서 언급한 Python의 라이브러리 extcolors를 사용한 결과는 다음과 같다  
![result_1](https://user-images.githubusercontent.com/96854885/223711127-4916273d-2b1d-4b98-a855-bb1f6d7be1b2.png)  
직접 색상을 추출한 결과는 다음과 같다  
![result_2](https://user-images.githubusercontent.com/96854885/223711811-a1c268ca-8eb1-4110-8499-391a830ac981.png)  

2. crawler 관리페이지 개발  
초기에는 다양한 쇼핑몰의 크롤러를 개발해 하나의 컴퓨터에서 multi-processing을 활용해 병렬적으로 처리하거나 AWS의 EC2를 활용해 여러 개의 크롤러를 동시에 구현  
하지만, 크롤링된 이미지를 데이터팀과 공유하고 이미지들을 pose-compositon model을 활용해 filtering하는 과정에서 비효율적인 업무를 자동화하기 위해 다수의 크롤러를 생성하고 구동하는 것을 시작으로 크롤링된 이미지를 필터링, 다운로드까지 하나의 pipeline으로 진행하기 위해 django와 django rest framework를 활용해 크롤러 관리 페이지 개발  
- 주요 기능 소개  
1. swagger 작성
2. 여러 쇼핑몰 내 이미지와 텍스트 크롤링할 수 있는 크롤러 다중 생성(하나의 프로젝트에 여러 개 크롤러 생성 가능, 여러 프로젝트에 여러 개 크롤러 생성 가능)  
3. 쇼핑몰 별, 어트리뷰트(플레어스커트, 펜슬스커트 등) 별, 이미지 또는 텍스트 별 프로젝트 다중 생성(Project 예시: farfetch몰의 플레어스커트 이미지 크롤링) -- 어트리뷰트는 사전 정의된 어트리뷰트 사용 
4. 프로젝트 단위로 크롤러 생성 관리 및 크롤링된 이미지 및 텍스트 데이터 관리(각 크롤러는 비동기 방식으로 처리)  
5. 크롤링된 이미지 및 텍스트 조회 및 삭제 기능  
6. batch program 구현(5초마다 각 크롤러들의 상태(run, stopped 등), 수집된 데이터 수, 진행 시간, 남은 시간 업데이트)   
7. 크롤링된 이미지 DB에 저장 및 mysql 연동  
8. 크롤링된 이미지 어트리뷰트 기준 또는 모델 유무, 모델의 포즈 기준으로 필터링 후 .zip 파일로 다운로드  
9. 최종 개발 완료된 페이지 배포(AWS)

