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

전처리 후 예시 이미지는 다음과 같다
![test_image_1](https://user-images.githubusercontent.com/96854885/223710985-8f586d8b-7e28-473e-9ef0-2f4b4dd6cdf8.png)

![result_1](https://user-images.githubusercontent.com/96854885/223711127-4916273d-2b1d-4b98-a855-bb1f6d7be1b2.png)
