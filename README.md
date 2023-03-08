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
전처리 후 예시 이미지는 다음과 같다  
![test_image_1](https://user-images.githubusercontent.com/96854885/223710985-8f586d8b-7e28-473e-9ef0-2f4b4dd6cdf8.png)  
위에서 언급한 Python의 라이브러리 extcolors를 사용한 결과는 다음과 같다  
![result_1](https://user-images.githubusercontent.com/96854885/223711127-4916273d-2b1d-4b98-a855-bb1f6d7be1b2.png)  
직접 색상을 추출한 결과는 다음과 같다  
![result_2](https://user-images.githubusercontent.com/96854885/223711811-a1c268ca-8eb1-4110-8499-391a830ac981.png)
