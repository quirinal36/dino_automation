# 챕터 4: 이미지 배열

> "이미지는 숫자의 바다다"

---

## 학습 목표

- 디지털 이미지가 숫자 배열임을 이해한다
- PIL 이미지를 NumPy 배열로 변환한다
- RGB 색상 모델을 이해한다
- 배열의 shape(형태)을 해석한다
- 개별 픽셀에 접근한다

---

## 디지털 이미지의 본질

### 이미지 = 숫자 격자

컴퓨터에게 이미지는 **숫자들의 2차원 격자**입니다.

```
흑백 이미지 예시 (5x5):

┌────┬────┬────┬────┬────┐
│ 255│ 255│ 255│ 255│ 255│   255 = 흰색
├────┼────┼────┼────┼────┤
│ 255│  0 │  0 │  0 │ 255│     0 = 검은색
├────┼────┼────┼────┼────┤
│ 255│  0 │ 128│  0 │ 255│   128 = 회색
├────┼────┼────┼────┼────┤
│ 255│  0 │  0 │  0 │ 255│
├────┼────┼────┼────┼────┤
│ 255│ 255│ 255│ 255│ 255│
└────┴────┴────┴────┴────┘
```

### 픽셀 값의 범위

- **0** = 완전히 어두움 (검정)
- **255** = 완전히 밝음 (흰색)
- **1-254** = 중간 밝기들

---

## RGB 색상 모델

### 컬러 이미지의 구조

컬러 이미지는 3개의 채널(Channel)로 구성됩니다:

- **R (Red)**: 빨강 채널
- **G (Green)**: 초록 채널
- **B (Blue)**: 파랑 채널

각 채널의 값 조합으로 모든 색상을 표현합니다.

### 색상 예시

| 색상 | R | G | B |
|------|---|---|---|
| 빨강 | 255 | 0 | 0 |
| 초록 | 0 | 255 | 0 |
| 파랑 | 0 | 0 | 255 |
| **흰색** | **255** | **255** | **255** |
| **검정** | **0** | **0** | **0** |
| 노랑 | 255 | 255 | 0 |
| 회색 | 128 | 128 | 128 |

---

## NumPy 배열로 변환

### NumPy란?

**NumPy**는 Python에서 수치 계산을 위한 핵심 라이브러리입니다.

- 다차원 배열을 효율적으로 처리
- 이미지 처리에 필수적

### 변환 방법

```python
# 힌트: np.array() 함수 사용
import numpy as np
from PIL import ImageGrab

screenshot = ImageGrab.grab()
img_array = np.______(screenshot)
```

---

## 배열의 Shape (형태)

### Shape이란?

배열의 **shape**는 각 차원의 크기를 나타내는 튜플입니다.

### 이미지 배열의 Shape

```python
print(img_array.shape)
# 출력: (1080, 1920, 3)
```

이 숫자들의 의미:

```
(1080, 1920, 3)
   │     │    │
   │     │    └── 채널 수 (R, G, B)
   │     └─────── 가로 픽셀 수 (너비)
   └───────────── 세로 픽셀 수 (높이)
```

**주의**: 순서가 **(높이, 너비, 채널)**입니다!

### 왜 높이가 먼저일까?

배열에서 첫 번째 인덱스는 **행(row)**을 나타냅니다.
행은 세로 방향이므로 높이가 먼저 옵니다.

```
     열 0   열 1   열 2   ...
행 0  [■]   [■]   [■]   ...
행 1  [■]   [■]   [■]   ...
행 2  [■]   [■]   [■]   ...
...
```

---

## 픽셀 접근하기

### 단일 픽셀 접근

```python
# 힌트: array[y, x] 형태로 접근
pixel = img_array[______, ______]  # y=100, x=200 위치의 픽셀
print(pixel)  # [R, G, B] 배열 출력
```

**중요**: 순서는 `[y, x]`입니다! (`[x, y]`가 아님)

### 왜 y가 먼저일까?

배열에서:
- 첫 번째 인덱스 = 행 = y (세로 위치)
- 두 번째 인덱스 = 열 = x (가로 위치)

```
img_array[y, x]
          │  │
          │  └── 열 번호 (가로, x)
          └───── 행 번호 (세로, y)
```

### 개별 채널 접근

```python
pixel = img_array[100, 200]  # [R, G, B]
red = pixel[0]    # 빨강 값
green = pixel[1]  # 초록 값
blue = pixel[2]   # 파랑 값

# 또는 한 번에
red, green, blue = img_array[100, 200]
```

---

## 생각해보기

### 질문 1: 메모리 계산

1920x1080 RGB 이미지의 NumPy 배열이 차지하는 메모리는?

- 총 픽셀: 1920 × 1080 = ?
- 픽셀당 바이트: 3 (R, G, B 각 1바이트)
- 총 바이트: ?
- MB로 환산: ? / 1024 / 1024 = ?

### 질문 2: 좌표 순서

아래 코드의 결과는?

```python
img_array.shape  # (1080, 1920, 3)
pixel = img_array[500, 1000]
```

이 픽셀은 화면의 어디에 있을까요?

### 질문 3: 흰색 확인

게임 배경이 흰색인지 확인하려면 R, G, B 값이 각각 어떤 범위여야 할까요?

---

## 실습 과제

### Exercise 4.1: 배열 변환

화면을 캡처하고 NumPy 배열로 변환하세요.

**파일명**: `array_test.py`

```python
import numpy as np
from PIL import ImageGrab

# 1. 화면 캡처
screenshot = ______

# 2. NumPy 배열로 변환
img_array = ______

# 3. 타입 확인
print(f"타입: {type(img_array)}")

# 4. Shape 확인
print(f"Shape: {______}")

# 5. 데이터 타입 확인 (dtype)
print(f"데이터 타입: {img_array.______}")
```

### Exercise 4.2: Shape 해석

실행 결과로 나온 shape을 해석하세요:

```
Shape: (????, ????, ????)
         │     │     │
         │     │     └── ?????
         │     └──────── ?????
         └────────────── ?????
```

### Exercise 4.3: 픽셀 접근

특정 위치의 픽셀 값을 확인하세요.

```python
# 화면 중앙 픽셀 접근
height, width, _ = img_array.______
center_y = height // 2
center_x = width // 2

center_pixel = img_array[______, ______]
print(f"중앙 픽셀 RGB: {center_pixel}")
print(f"  빨강(R): {center_pixel[0]}")
print(f"  초록(G): {center_pixel[1]}")
print(f"  파랑(B): {center_pixel[2]}")
```

### Exercise 4.4: 여러 픽셀 확인

화면 네 모서리의 픽셀 값을 확인하세요.

```python
# 네 모서리
top_left = img_array[0, 0]
top_right = img_array[0, width-1]
bottom_left = img_array[height-1, 0]
bottom_right = img_array[______, ______]

print(f"왼쪽 위: {top_left}")
print(f"오른쪽 위: {top_right}")
print(f"왼쪽 아래: {bottom_left}")
print(f"오른쪽 아래: {bottom_right}")
```

### Exercise 4.5: 흰색 픽셀인지 확인

픽셀이 "거의 흰색"인지 확인하는 함수를 작성하세요.

```python
def is_white(pixel, threshold=200):
    """
    픽셀이 흰색에 가까운지 확인

    Args:
        pixel: [R, G, B] 배열
        threshold: 이 값 이상이면 흰색으로 판단

    Returns:
        True if 흰색, False otherwise
    """
    r, g, b = pixel
    return r > threshold ______ g > threshold ______ b > threshold

# 테스트
test_pixel = img_array[100, 100]
print(f"픽셀 {test_pixel}는 흰색? {is_white(test_pixel)}")
```

---

## 예상 결과

### Exercise 4.1 실행 결과 예시

```
타입: <class 'numpy.ndarray'>
Shape: (1080, 1920, 3)
데이터 타입: uint8
```

`uint8` = unsigned integer 8-bit = 0-255 범위의 정수

### Exercise 4.3 실행 결과 예시

```
중앙 픽셀 RGB: [245 245 245]
  빨강(R): 245
  초록(G): 245
  파랑(B): 245
```

---

## 핵심 정리

### 변환 과정

```
PIL Image  ──np.array()──►  NumPy Array
```

### Shape 구조

```
(높이, 너비, 채널)
(height, width, channels)
(   y,     x,     3   )
```

### 픽셀 접근

```python
pixel = array[y, x]      # [R, G, B]
red = array[y, x, 0]     # R 값만
green = array[y, x, 1]   # G 값만
blue = array[y, x, 2]    # B 값만
```

### 좌표 주의사항

| 개념 | 화면/이미지 | 배열 |
|------|-------------|------|
| 표기 | (x, y) | [y, x] |
| 순서 | 가로, 세로 | 세로, 가로 |

---

## 체크포인트

- [ ] 이미지가 숫자 배열임을 이해한다
- [ ] RGB 색상 모델을 설명할 수 있다
- [ ] PIL 이미지를 NumPy 배열로 변환할 수 있다
- [ ] shape의 각 숫자 의미를 설명할 수 있다
- [ ] 특정 좌표의 픽셀 값을 읽을 수 있다

---

## 다음 챕터 미리보기

**챕터 5: 관심 영역 (ROI)**에서는 전체 이미지에서 특정 영역만 추출하는 방법을 배웁니다. NumPy의 배열 슬라이싱을 사용해서 ROI를 추출합니다.

[다음 챕터로 이동 →](../05-관심영역/chapter-05-roi.md)
