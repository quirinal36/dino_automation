# 챕터 6: 이미지 처리

> "색을 버리고, 밝기만 남기자"

---

## 학습 목표

- OpenCV 라이브러리의 기본을 이해한다
- BGR과 RGB 색상 순서의 차이를 안다
- 이미지를 그레이스케일로 변환한다
- 그레이스케일의 장점을 이해한다

---

## OpenCV란?

### 소개

**OpenCV** (Open Source Computer Vision Library)

- 컴퓨터 비전 분야의 대표적인 오픈소스 라이브러리
- C++로 작성, Python에서도 사용 가능
- 이미지/영상 처리에 강력한 기능 제공

### Python에서 사용

```python
import cv2  # OpenCV를 cv2로 import
```

**왜 cv2일까?** OpenCV의 Python 바인딩 버전 2를 의미합니다.

---

## BGR vs RGB

### OpenCV의 특이점

OpenCV는 역사적인 이유로 **BGR** 순서를 사용합니다:

| 라이브러리 | 색상 순서 |
|-----------|----------|
| PIL/Pillow | R-G-B |
| NumPy (PIL 변환) | R-G-B |
| **OpenCV** | **B-G-R** |

### 실제 영향

```
빨간색 픽셀:
- RGB: [255, 0, 0]
- BGR: [0, 0, 255]
```

### 왜 알아야 하나?

PIL로 캡처한 이미지(RGB)를 OpenCV 함수에 사용할 때:
- 색상 관련 작업: 변환 필요
- **그레이스케일 변환**: 순서 명시 필요

---

## 그레이스케일 변환

### 왜 그레이스케일로 변환하나?

**컬러 이미지 (RGB)**:
- 픽셀당 3개 값: [R, G, B]
- 배열 shape: (height, width, **3**)
- 분석 복잡

**그레이스케일 이미지**:
- 픽셀당 1개 값: 밝기
- 배열 shape: (height, width)
- 분석 간단!

### 장점 정리

| 항목 | 컬러 (RGB) | 그레이스케일 |
|------|-----------|-------------|
| 픽셀당 데이터 | 3 바이트 | 1 바이트 |
| 메모리 사용 | 3배 | 1배 |
| 처리 속도 | 느림 | 빠름 |
| 밝기 분석 | 계산 필요 | 바로 사용 |

### 우리 프로젝트에서

장애물 감지는 **밝기**만 필요합니다:
- 배경: 밝음 (높은 값)
- 장애물: 어두움 (낮은 값)

색상 정보는 불필요!

---

## 변환 방법

### OpenCV 함수

```python
gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
```

- `cvtColor`: Color Space 변환 함수
- `COLOR_RGB2GRAY`: RGB → 그레이스케일

### 전체 코드 흐름

```python
import cv2
import numpy as np
from PIL import ImageGrab

# 1. 화면 캡처 (PIL → RGB)
screenshot = ImageGrab.grab()

# 2. NumPy 배열로 변환 (RGB)
rgb_array = np.array(screenshot)

# 3. 그레이스케일로 변환
gray = cv2.cvtColor(rgb_array, cv2.______)
```

### 변환 원리

그레이스케일 값은 RGB의 가중 평균입니다:

```
Gray = 0.299×R + 0.587×G + 0.114×B
```

인간의 눈이 초록색에 더 민감하기 때문에 G의 가중치가 높습니다.

---

## Shape 변화 확인

### 변환 전후 비교

```python
print(f"RGB shape: {rgb_array.shape}")    # (1080, 1920, 3)
print(f"Gray shape: {gray.shape}")         # (1080, 1920)
```

3차원 배열 → 2차원 배열로 변환됨!

### 픽셀 접근 변화

```python
# RGB
pixel_rgb = rgb_array[100, 200]  # [R, G, B]

# 그레이스케일
pixel_gray = gray[100, 200]      # 단일 값 (0-255)
```

---

## 생각해보기

### 질문 1: 색상 순서

아래 코드의 문제점은?

```python
# PIL로 캡처 (RGB)
screenshot = ImageGrab.grab()
img = np.array(screenshot)

# OpenCV로 저장 (BGR 기대)
cv2.imwrite("test.png", img)
```

저장된 이미지의 색상은 어떻게 될까요?

### 질문 2: 다른 변환 코드

다음 두 코드의 차이점은?

```python
# 코드 A
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

# 코드 B
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
```

### 질문 3: 야간 모드

Dino 게임 야간 모드에서:
- 배경: 검정 (0에 가까움)
- 장애물: 흰색 (255에 가까움)

그레이스케일 변환 후에도 감지 로직이 작동할까요?

---

## 실습 과제

### Exercise 6.1: 그레이스케일 변환

화면을 캡처하고 그레이스케일로 변환하세요.

**파일명**: `grayscale_test.py`

```python
import cv2
import numpy as np
from PIL import ImageGrab, Image

# 1. 화면 캡처
screenshot = ImageGrab.grab()
rgb_array = np.array(screenshot)

# 2. 그레이스케일 변환
gray = cv2.cvtColor(rgb_array, cv2.COLOR_______)

# 3. Shape 비교
print(f"RGB shape: {rgb_array.______}")
print(f"Gray shape: {gray.______}")

# 4. 그레이스케일 이미지 저장
gray_image = Image.fromarray(gray)
gray_image.save("screenshot_gray.png")
print("그레이스케일 이미지 저장 완료!")
```

### Exercise 6.2: 픽셀 값 비교

같은 위치의 RGB 값과 그레이스케일 값을 비교하세요.

```python
y, x = 100, 200

# RGB 픽셀
rgb_pixel = rgb_array[y, x]
print(f"RGB 픽셀: R={rgb_pixel[0]}, G={rgb_pixel[1]}, B={rgb_pixel[2]}")

# 그레이스케일 픽셀
gray_pixel = gray[y, x]
print(f"Gray 픽셀: {gray_pixel}")

# 수동 계산 (가중 평균)
manual_gray = 0.299 * rgb_pixel[0] + 0.587 * rgb_pixel[1] + 0.114 * rgb_pixel[2]
print(f"수동 계산: {manual_gray:.1f}")
```

### Exercise 6.3: ROI 그레이스케일 변환

ROI를 추출한 후 그레이스케일로 변환하세요.

```python
# ROI 좌표
x1, y1, x2, y2 = 100, 200, 400, 350

# ROI 추출 (RGB)
roi_rgb = rgb_array[______:______, ______:______]

# ROI 그레이스케일 변환
roi_gray = cv2.cvtColor(roi_rgb, ______)

# Shape 확인
print(f"ROI RGB shape: {roi_rgb.shape}")
print(f"ROI Gray shape: {roi_gray.shape}")
```

### Exercise 6.4: 그레이스케일 변환 함수

재사용 가능한 함수를 만드세요.

```python
def rgb_to_gray(rgb_image):
    """
    RGB 이미지를 그레이스케일로 변환

    Args:
        rgb_image: RGB NumPy 배열

    Returns:
        그레이스케일 NumPy 배열
    """
    return cv2.______(rgb_image, ______)

# 테스트
gray = rgb_to_gray(rgb_array)
print(f"변환 완료: {gray.shape}")
```

### Exercise 6.5: 전체 파이프라인

화면 캡처 → ROI 추출 → 그레이스케일 변환을 하나로 연결하세요.

```python
def capture_roi_gray(x1, y1, x2, y2):
    """
    화면에서 ROI를 캡처하고 그레이스케일로 반환

    Args:
        x1, y1, x2, y2: ROI 좌표

    Returns:
        그레이스케일 NumPy 배열
    """
    # 1. 화면 캡처
    screenshot = ______
    rgb_array = np.array(______)

    # 2. ROI 추출
    roi = rgb_array[______:______, ______:______]

    # 3. 그레이스케일 변환
    gray_roi = ______

    return gray_roi

# 테스트
roi = capture_roi_gray(100, 200, 400, 350)
print(f"결과 shape: {roi.shape}")  # (150, 300)
```

---

## 예상 결과

### Exercise 6.1 실행 결과

```
RGB shape: (1080, 1920, 3)
Gray shape: (1080, 1920)
그레이스케일 이미지 저장 완료!
```

### Exercise 6.2 실행 결과 예시

```
RGB 픽셀: R=245, G=245, B=245
Gray 픽셀: 245
수동 계산: 245.0
```

---

## 핵심 정리

### 변환 함수

```python
gray = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2GRAY)
```

### Shape 변화

```
RGB:  (height, width, 3)
Gray: (height, width)
```

### 색상 순서 주의

| 상황 | 사용할 플래그 |
|------|--------------|
| PIL/ImageGrab → Gray | COLOR_RGB2GRAY |
| OpenCV 이미지 → Gray | COLOR_BGR2GRAY |

### 왜 그레이스케일?

```
✓ 메모리 1/3 사용
✓ 처리 속도 향상
✓ 밝기 분석에 최적
```

---

## 체크포인트

- [ ] OpenCV의 BGR 순서를 이해한다
- [ ] cv2.cvtColor()로 그레이스케일 변환을 할 수 있다
- [ ] 변환 전후 shape 변화를 설명할 수 있다
- [ ] RGB2GRAY와 BGR2GRAY의 차이를 안다

---

## 다음 챕터 미리보기

**챕터 7: 장애물 감지**에서는 그레이스케일 이미지의 밝기를 분석하여 장애물을 감지하는 알고리즘을 구현합니다. NumPy의 통계 함수를 사용해서 "어두운 픽셀 비율"을 계산합니다.

[다음 챕터로 이동 →](../07-장애물감지/chapter-07-obstacle-detection.md)
