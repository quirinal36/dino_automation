# 챕터 7: 장애물 감지

> "어둠을 감지하라"

---

## 학습 목표

- 밝기 분석의 원리를 이해한다
- NumPy의 통계 함수를 사용한다
- 임계값(threshold) 기반 감지를 구현한다
- 장애물 감지 함수를 완성한다

---

## 감지 전략 복습

챕터 2에서 세운 전략:

```
게임 특성:
- 배경: 흰색 (밝음) → 픽셀 값 높음 (200-255)
- 장애물: 어두운 색 → 픽셀 값 낮음 (0-100)

감지 방법:
ROI에서 "어두운 픽셀"의 비율이 일정 수준 이상이면 → 장애물!
```

---

## NumPy 통계 함수

### np.mean() - 평균

```python
import numpy as np

# 예시 배열
arr = np.array([100, 150, 200, 250])

# 평균 계산
avg = np.mean(arr)  # 175.0
```

### np.sum() - 합계

```python
arr = np.array([1, 2, 3, 4, 5])
total = np.sum(arr)  # 15
```

### 불리언 배열과 합계

```python
arr = np.array([50, 150, 30, 200, 80])

# 100보다 작은지 비교
below_100 = arr < 100  # [True, False, True, False, True]

# True 개수 세기 (True=1, False=0)
count = np.sum(below_100)  # 3
```

### .size - 배열 크기

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])
print(arr.size)  # 6 (전체 원소 개수)
```

---

## 감지 알고리즘

### 단계별 분해

```
1. 그레이스케일 ROI 이미지 받기
2. 평균 밝기 계산 (참고용)
3. "어두운 픽셀" 개수 세기
4. 전체 픽셀 대비 비율 계산
5. 비율이 임계값 초과하면 → 장애물 감지!
```

### 핵심 수식

```
어두운 픽셀 비율 = 어두운 픽셀 수 / 전체 픽셀 수

if 비율 > 임계값:
    장애물 있음!
```

---

## 임계값 (Threshold) 이란?

### 밝기 임계값

"어두움"의 기준을 정하는 값입니다.

```
픽셀 값 범위: 0 (검정) ~ 255 (흰색)

밝기 임계값 = 128 이라면:
- 128 미만: 어두움
- 128 이상: 밝음
```

### 비율 임계값

"장애물 있음"을 판정하는 기준입니다.

```
비율 임계값 = 0.05 (5%) 라면:
- 어두운 픽셀이 5% 초과: 장애물 있음
- 어두운 픽셀이 5% 이하: 장애물 없음
```

### 왜 비율을 쓰나?

```
ROI 크기가 달라져도 일관된 감지가 가능합니다.

ROI 90x50 = 4500 픽셀 → 5%는 225개
ROI 60x40 = 2400 픽셀 → 5%는 120개

비율로 계산하면 ROI 크기에 무관하게 작동!
```

---

## 코드 구현

### 기본 구조

```python
def is_obstacle_detected(gray_roi, brightness_threshold=128, ratio_threshold=0.05):
    """
    ROI에서 장애물을 감지합니다.

    Args:
        gray_roi: 그레이스케일 이미지 배열
        brightness_threshold: 어두움 판정 기준 (이 값 미만이면 어두움)
        ratio_threshold: 장애물 판정 기준 (이 비율 초과하면 장애물)

    Returns:
        tuple: (감지 여부, 평균 밝기, 어두운 픽셀 비율)
    """
    # 1. 평균 밝기 계산
    avg_brightness = np.______(gray_roi)

    # 2. 어두운 픽셀 개수 세기
    dark_pixels = np.______(gray_roi < brightness_threshold)

    # 3. 전체 픽셀 수
    total_pixels = gray_roi.______

    # 4. 비율 계산
    dark_ratio = dark_pixels / total_pixels

    # 5. 감지 판정
    is_detected = dark_ratio > ratio_threshold

    return is_detected, avg_brightness, dark_ratio
```

---

## 생각해보기

### 질문 1: 임계값 선택

밝기 임계값을 어떻게 정해야 할까요?

- 너무 높으면 (예: 200): 그림자도 장애물로 감지?
- 너무 낮으면 (예: 50): 회색 장애물을 놓칠 수 있음?

### 질문 2: 비율 임계값 선택

비율 임계값은 어떻게 정해야 할까요?

- 너무 높으면 (예: 20%): 작은 장애물 놓침
- 너무 낮으면 (예: 1%): 노이즈에도 반응

### 질문 3: 야간 모드 대응

야간 모드에서는:
- 배경: 검정 (어두움)
- 장애물: 흰색 (밝음)

현재 알고리즘은 작동할까요? 어떻게 수정할 수 있을까요?

---

## 실습 과제

### Exercise 7.1: 평균 밝기 계산

그레이스케일 이미지의 평균 밝기를 계산하세요.

**파일명**: `detection_test.py`

```python
import cv2
import numpy as np
from PIL import ImageGrab

# 1. 화면 캡처 및 그레이스케일 변환
screenshot = ImageGrab.grab()
rgb = np.array(screenshot)
gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)

# 2. 전체 화면 평균 밝기
avg = np.______(gray)
print(f"화면 평균 밝기: {avg:.1f}")

# 3. ROI 평균 밝기
x1, y1, x2, y2 = 100, 200, 400, 350
roi = gray[____:____, ____:____]
roi_avg = np.______(roi)
print(f"ROI 평균 밝기: {roi_avg:.1f}")
```

### Exercise 7.2: 어두운 픽셀 세기

어두운 픽셀의 개수와 비율을 계산하세요.

```python
# 밝기 임계값
threshold = 128

# 어두운 픽셀 세기
dark_pixels = np.______(roi < threshold)
total_pixels = roi.______
dark_ratio = dark_pixels / total_pixels

print(f"전체 픽셀: {total_pixels}")
print(f"어두운 픽셀 (< {threshold}): {dark_pixels}")
print(f"어두운 픽셀 비율: {dark_ratio * 100:.2f}%")
```

### Exercise 7.3: 감지 함수 구현

장애물 감지 함수를 완성하세요.

```python
def is_obstacle_detected(gray_roi, brightness_threshold=128, ratio_threshold=0.05):
    """
    ROI에서 장애물을 감지합니다.
    """
    # 평균 밝기
    avg_brightness = ______

    # 어두운 픽셀 수
    dark_pixels = ______

    # 전체 픽셀 수
    total_pixels = ______

    # 비율 계산
    dark_ratio = ______

    # 판정
    is_detected = ______

    return is_detected, avg_brightness, dark_ratio


# 테스트
result, brightness, ratio = is_obstacle_detected(roi)
print(f"감지 결과: {result}")
print(f"평균 밝기: {brightness:.1f}")
print(f"어두운 비율: {ratio * 100:.2f}%")
```

### Exercise 7.4: 다양한 임계값 테스트

다른 임계값으로 테스트해보세요.

```python
# 여러 밝기 임계값 테스트
for b_thresh in [50, 100, 128, 150, 200]:
    _, _, ratio = is_obstacle_detected(roi, brightness_threshold=b_thresh)
    print(f"밝기 임계값 {b_thresh}: 어두운 비율 {ratio * 100:.2f}%")

print()

# 여러 비율 임계값 테스트
for r_thresh in [0.01, 0.03, 0.05, 0.10, 0.20]:
    detected, _, ratio = is_obstacle_detected(
        roi,
        brightness_threshold=128,
        ratio_threshold=r_thresh
    )
    status = "감지됨" if detected else "감지 안됨"
    print(f"비율 임계값 {r_thresh * 100:.0f}%: {status} (실제 비율: {ratio * 100:.2f}%)")
```

### Exercise 7.5: Dino 게임 테스트

실제 Dino 게임에서 테스트하세요.

```python
import time

print("5초 후 캡처합니다. Dino 게임을 준비하세요!")
print("테스트 1: 장애물 없는 상태에서 캡처")
time.sleep(5)

# 캡처 및 분석
screenshot1 = ImageGrab.grab()
rgb1 = np.array(screenshot1)
gray1 = cv2.cvtColor(rgb1, cv2.COLOR_RGB2GRAY)

# ROI 좌표 (본인 화면에 맞게 조정!)
x1, y1, x2, y2 = 450, 320, 550, 370
roi1 = gray1[y1:y2, x1:x2]

result1, bright1, ratio1 = is_obstacle_detected(roi1)
print(f"테스트 1 결과: 감지={result1}, 밝기={bright1:.1f}, 비율={ratio1 * 100:.2f}%")

print("\n5초 후 다시 캡처합니다. 장애물이 ROI 안에 있을 때 캡처하세요!")
time.sleep(5)

screenshot2 = ImageGrab.grab()
rgb2 = np.array(screenshot2)
gray2 = cv2.cvtColor(rgb2, cv2.COLOR_RGB2GRAY)
roi2 = gray2[y1:y2, x1:x2]

result2, bright2, ratio2 = is_obstacle_detected(roi2)
print(f"테스트 2 결과: 감지={result2}, 밝기={bright2:.1f}, 비율={ratio2 * 100:.2f}%")

# ROI 이미지 저장
from PIL import Image
Image.fromarray(roi1).save("roi_empty.png")
Image.fromarray(roi2).save("roi_obstacle.png")
print("\nROI 이미지가 저장되었습니다. 확인해보세요!")
```

---

## 예상 결과

### Exercise 7.5 실행 결과 예시

**장애물 없는 경우:**
```
테스트 1 결과: 감지=False, 밝기=247.3, 비율=0.12%
```

**장애물 있는 경우:**
```
테스트 2 결과: 감지=True, 밝기=198.5, 비율=18.34%
```

---

## 핵심 정리

### 감지 알고리즘

```python
# 1. 평균 밝기 (참고용)
avg = np.mean(gray_roi)

# 2. 어두운 픽셀 비율
dark_ratio = np.sum(gray_roi < threshold) / gray_roi.size

# 3. 판정
is_obstacle = dark_ratio > ratio_threshold
```

### 기본 임계값

| 항목 | 권장 값 | 설명 |
|------|--------|------|
| 밝기 임계값 | 128 | 중간값 기준 |
| 비율 임계값 | 0.05 (5%) | 너무 민감하지 않게 |

### 튜닝 포인트

```
감지가 안 되면:
  → 밝기 임계값 올리기 (더 많은 픽셀을 "어두움"으로)
  → 비율 임계값 낮추기

오탐지가 많으면:
  → 밝기 임계값 낮추기
  → 비율 임계값 올리기
```

---

## 체크포인트

- [ ] np.mean()으로 평균을 계산할 수 있다
- [ ] np.sum()과 불리언 비교로 개수를 셀 수 있다
- [ ] 임계값의 개념을 이해한다
- [ ] 장애물 감지 함수를 작성할 수 있다
- [ ] 실제 Dino 게임에서 테스트해봤다

---

## 다음 챕터 미리보기

**챕터 8: 키보드 자동화**에서는 PyAutoGUI를 사용해서 키보드 입력을 자동화합니다. 장애물을 감지했을 때 스페이스바를 눌러 공룡을 점프시킵니다.

[다음 챕터로 이동 →](../08-키보드자동화/chapter-08-keyboard-automation.md)
