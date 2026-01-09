# 챕터 11: 게임 루프

> "모든 것을 하나로 연결하자"

---

## 학습 목표

- 메인 게임 루프를 설계한다
- 타이밍 제어를 구현한다
- 디버그 기능을 추가한다
- 안전한 종료를 처리한다

---

## 게임 루프란?

### 기본 개념

게임 루프는 **반복적으로 실행되는 핵심 사이클**입니다.

```
while 실행중:
    1. 입력 처리 (화면 캡처)
    2. 상태 분석 (장애물 감지)
    3. 출력 실행 (점프)
    4. 대기
```

### 우리 봇의 루프

```
┌─────────────────┐
│   화면 캡처      │
└────────┬────────┘
         ▼
┌─────────────────┐
│   ROI 추출       │
└────────┬────────┘
         ▼
┌─────────────────┐
│  그레이스케일     │
└────────┬────────┘
         ▼
┌─────────────────┐
│   밝기 분석      │
└────────┬────────┘
         ▼
    ┌────────┐
    │장애물?  │
    └────┬───┘
    Yes  │   No
    ▼    │
┌──────┐ │
│ 점프! │ │
└──┬───┘ │
   │쿨다운│
   ▼     │
┌──────────────────┐
│    대기 (50ms)    │◄───┘
└────────┬─────────┘
         │
         └─────────► (반복)
```

---

## 타이밍 제어

### 두 가지 타이밍

1. **체크 간격 (Check Interval)**
   - 화면을 얼마나 자주 확인하는가
   - 권장: 50ms (초당 20회)

2. **점프 쿨다운 (Jump Cooldown)**
   - 점프 후 얼마 동안 다시 점프하지 않는가
   - 권장: 300ms

### 왜 이 값들인가?

```
체크 간격 50ms:
- 너무 빠르면: CPU 낭비
- 너무 느리면: 장애물 놓침
- 50ms = 적당한 반응 속도

점프 쿨다운 300ms:
- 너무 짧으면: 같은 장애물에 여러 번 반응
- 너무 길면: 연속 장애물에 대응 불가
- 300ms = 점프 동작 완료 시간
```

---

## 코드 구조

### 기본 틀

```python
import time
import cv2
import numpy as np
import pyautogui
from PIL import ImageGrab

def run_game_loop(roi, check_interval=0.05, jump_cooldown=0.3):
    """
    게임 자동화 메인 루프

    Args:
        roi: ROI 좌표 딕셔너리 {'x1':, 'y1':, 'x2':, 'y2':}
        check_interval: 체크 간격 (초)
        jump_cooldown: 점프 쿨다운 (초)
    """
    running = True
    jump_count = 0

    x1, y1 = roi['x1'], roi['y1']
    x2, y2 = roi['x2'], roi['y2']

    try:
        while running:
            # 1. 화면 캡처
            # 2. ROI 추출
            # 3. 그레이스케일 변환
            # 4. 장애물 감지
            # 5. 점프 (필요시)
            # 6. 대기

            time.sleep(check_interval)

    except KeyboardInterrupt:
        print(f"\n종료! 총 점프: {jump_count}번")
```

---

## 디버그 기능

### 왜 필요한가?

- 봇이 제대로 작동하는지 확인
- 문제가 생겼을 때 원인 파악
- 임계값 조정에 참고

### 디버그 이미지 저장

```python
def save_debug_image(roi_img, jump_count):
    """점프 시 ROI 이미지 저장"""
    import os
    from datetime import datetime

    # 폴더 생성
    os.makedirs("debug_captures", exist_ok=True)

    # 파일명 생성
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
    filename = f"debug_captures/jump_{jump_count:04d}_{timestamp}.png"

    # 저장 (RGB → BGR)
    bgr = cv2.cvtColor(roi_img, cv2.COLOR_RGB2BGR)
    cv2.imwrite(filename, bgr)

    return filename
```

### 콘솔 출력

```python
print(f"점프! (총 {jump_count}번)")
print(f"  - 평균 밝기: {brightness:.1f}")
print(f"  - 어두운 비율: {ratio * 100:.1f}%")
```

---

## 안전한 종료

### KeyboardInterrupt

`Ctrl+C`를 누르면 발생하는 예외입니다.

```python
try:
    while True:
        # 루프 내용
        pass
except KeyboardInterrupt:
    print("사용자가 종료했습니다.")
```

### 종료 시 정리

```python
except KeyboardInterrupt:
    print("\n" + "=" * 40)
    print("게임 봇 종료")
    print("=" * 40)
    print(f"총 점프 횟수: {jump_count}")
    print(f"실행 시간: {time.time() - start_time:.1f}초")
```

---

## 생각해보기

### 질문 1: 체크 간격 최적화

체크 간격을 어떻게 결정해야 할까요?
게임 속도가 빨라지면 어떻게 대응할까요?

### 질문 2: 디버그 이미지 관리

디버그 이미지가 계속 쌓이면?
- 자동 삭제?
- 개수 제한?
- 저장 조건 설정?

### 질문 3: 성능 모니터링

루프가 얼마나 빨리 돌아가는지 어떻게 측정할까요?
실제 체크 간격이 설정값과 다를 수 있을까요?

---

## 실습 과제

### Exercise 11.1: 기본 루프 구조

기본 게임 루프를 작성하세요.

**파일명**: `game_loop_test.py`

```python
import time

def simple_loop(duration=5):
    """단순 루프 테스트 (duration초 동안 실행)"""
    count = 0
    start = time.time()

    try:
        while time.time() - start < duration:
            count += 1
            print(f"루프 #{count}")
            time.sleep(______)  # 0.5초 대기

    except KeyboardInterrupt:
        print("\n중단됨!")

    print(f"총 {count}회 실행")

simple_loop(5)
```

### Exercise 11.2: 캡처 + 분석 루프

캡처와 분석을 반복하세요.

```python
import cv2
import numpy as np
from PIL import ImageGrab
import time

def capture_loop(roi, duration=10):
    """캡처 및 분석 루프"""
    x1, y1 = roi['x1'], roi['y1']
    x2, y2 = roi['x2'], roi['y2']

    count = 0
    start = time.time()

    try:
        while time.time() - start < duration:
            # 캡처
            screenshot = ImageGrab.______()
            img = np.array(screenshot)

            # ROI 추출
            roi_img = img[______:______, ______:______]

            # 그레이스케일
            gray = cv2.cvtColor(roi_img, cv2.COLOR_______)

            # 밝기 분석
            avg_brightness = np.______(gray)

            count += 1
            print(f"#{count} 밝기: {avg_brightness:.1f}")

            time.sleep(0.1)  # 100ms

    except KeyboardInterrupt:
        print("\n중단됨!")

# 테스트 (ROI는 본인 화면에 맞게)
test_roi = {'x1': 450, 'y1': 320, 'x2': 550, 'y2': 370}
capture_loop(test_roi, 5)
```

### Exercise 11.3: 장애물 감지 추가

감지 로직을 추가하세요.

```python
def is_obstacle_detected(gray_roi, threshold=128, ratio_threshold=0.05):
    """장애물 감지"""
    dark_pixels = np.sum(gray_roi < threshold)
    total_pixels = gray_roi.size
    dark_ratio = dark_pixels / total_pixels
    avg_brightness = np.mean(gray_roi)

    return dark_ratio > ratio_threshold, avg_brightness, dark_ratio


def detection_loop(roi, duration=10):
    """감지 루프"""
    x1, y1, x2, y2 = roi['x1'], roi['y1'], roi['x2'], roi['y2']
    detected_count = 0

    start = time.time()
    try:
        while time.time() - start < duration:
            # 캡처 → ROI → 그레이스케일
            screenshot = ImageGrab.grab()
            img = np.array(screenshot)
            roi_img = img[y1:y2, x1:x2]
            gray = cv2.cvtColor(roi_img, cv2.COLOR_RGB2GRAY)

            # 감지
            detected, brightness, ratio = ______(gray)

            if detected:
                detected_count += 1
                print(f"감지! 밝기={brightness:.1f}, 비율={ratio*100:.1f}%")

            time.sleep(0.05)

    except KeyboardInterrupt:
        pass

    print(f"\n총 {detected_count}번 감지됨")
```

### Exercise 11.4: 점프 통합

점프 기능을 추가하세요.

```python
import pyautogui

def game_loop(roi, duration=30):
    """게임 루프 (점프 포함)"""
    x1, y1, x2, y2 = roi['x1'], roi['y1'], roi['x2'], roi['y2']

    jump_count = 0
    check_interval = 0.05
    jump_cooldown = 0.3

    print("3초 후 시작! 게임을 준비하세요...")
    time.sleep(3)
    print("시작!")

    start = time.time()
    try:
        while time.time() - start < duration:
            # 캡처 및 분석
            screenshot = ImageGrab.grab()
            img = np.array(screenshot)
            roi_img = img[y1:y2, x1:x2]
            gray = cv2.cvtColor(roi_img, cv2.COLOR_RGB2GRAY)

            # 감지
            detected, brightness, ratio = is_obstacle_detected(gray)

            if detected:
                # 점프!
                pyautogui.______('space')
                jump_count += 1
                print(f"점프 #{jump_count}! (밝기: {brightness:.1f})")

                # 쿨다운
                time.sleep(______)
            else:
                time.sleep(______)

    except KeyboardInterrupt:
        pass

    print(f"\n총 {jump_count}번 점프!")

# 실행
game_loop(test_roi, 30)
```

### Exercise 11.5: 디버그 기능 추가

디버그 이미지 저장을 추가하세요.

```python
import os
from datetime import datetime

def save_debug(roi_img, jump_count):
    """디버그 이미지 저장"""
    os.makedirs("debug_captures", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
    filename = f"debug_captures/jump_{jump_count:04d}_{timestamp}.png"

    # RGB → BGR 변환 후 저장
    bgr = cv2.cvtColor(roi_img, cv2.______BGR)
    cv2.imwrite(filename, bgr)

    return filename


def game_loop_with_debug(roi, duration=30):
    """디버그 기능이 있는 게임 루프"""
    x1, y1, x2, y2 = roi['x1'], roi['y1'], roi['x2'], roi['y2']
    jump_count = 0

    print("3초 후 시작!")
    time.sleep(3)

    start = time.time()
    try:
        while time.time() - start < duration:
            screenshot = ImageGrab.grab()
            img = np.array(screenshot)
            roi_img = img[y1:y2, x1:x2]
            gray = cv2.cvtColor(roi_img, cv2.COLOR_RGB2GRAY)

            detected, brightness, ratio = is_obstacle_detected(gray)

            if detected:
                pyautogui.press('space')
                jump_count += 1

                # 디버그 저장
                filename = save_debug(______, ______)
                print(f"점프 #{jump_count}!")
                print(f"  밝기: {brightness:.1f}, 비율: {ratio*100:.1f}%")
                print(f"  저장: {filename}")

                time.sleep(0.3)
            else:
                time.sleep(0.05)

    except KeyboardInterrupt:
        pass

    print(f"\n종료! 총 {jump_count}번 점프")
    print(f"디버그 이미지: debug_captures/ 폴더 확인")
```

---

## 예상 결과

### Exercise 11.5 실행 예시

```
3초 후 시작!
점프 #1!
  밝기: 198.3, 비율: 12.4%
  저장: debug_captures/jump_0001_20260110_143025_234.png
점프 #2!
  밝기: 187.6, 비율: 18.7%
  저장: debug_captures/jump_0002_20260110_143028_891.png
...

종료! 총 15번 점프
디버그 이미지: debug_captures/ 폴더 확인
```

---

## 핵심 정리

### 게임 루프 구조

```python
try:
    while running:
        capture()
        analyze()
        if obstacle:
            jump()
            sleep(cooldown)
        sleep(interval)
except KeyboardInterrupt:
    cleanup()
```

### 타이밍 권장값

| 항목 | 값 | 설명 |
|------|-----|------|
| 체크 간격 | 50ms | 0.05초 |
| 점프 쿨다운 | 300ms | 0.3초 |

### 디버그 패턴

```python
os.makedirs("folder", exist_ok=True)
filename = f"prefix_{count:04d}_{timestamp}.png"
cv2.imwrite(filename, bgr_image)
```

---

## 체크포인트

- [ ] 기본 게임 루프를 작성할 수 있다
- [ ] 타이밍 제어의 중요성을 이해한다
- [ ] 디버그 이미지를 저장할 수 있다
- [ ] KeyboardInterrupt로 안전하게 종료한다
- [ ] 실제 게임에서 테스트해봤다

---

## 다음 챕터 미리보기

**챕터 12: 통합 완성**에서는 지금까지 만든 모든 것을 하나의 완성된 프로젝트로 조립합니다. 클래스로 구조화하고, 사용자 친화적인 인터페이스를 추가합니다.

[다음 챕터로 이동 →](../12-통합완성/chapter-12-final-integration.md)
