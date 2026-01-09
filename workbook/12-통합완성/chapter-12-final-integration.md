# 챕터 12: 통합 완성

> "모든 조각을 하나로"

---

## 학습 목표

- 클래스로 코드를 구조화한다
- 완전한 프로젝트를 조립한다
- 사용자 경험을 개선한다
- 최종 테스트를 수행한다

---

## 프로젝트 구조 복습

### 최종 파일 구조

```
dino_automation/
├── calibrate.py       # ROI 캘리브레이션 도구
├── main.py            # 게임 자동화 엔진
├── roi_config.json    # 설정 파일 (자동 생성)
├── requirements.txt   # 의존성 목록
└── debug_captures/    # 디버그 이미지 (자동 생성)
```

### 실행 순서

```
1. calibrate.py 실행 → roi_config.json 생성
2. main.py 실행 → roi_config.json 읽기 → 게임 자동화
```

---

## 클래스 구조화

### 왜 클래스를 사용하는가?

함수만 사용할 때:
```python
jump_count = 0
roi = None
config_file = "roi_config.json"

def jump():
    global jump_count
    ...

def load_config():
    global roi
    ...
```

클래스 사용:
```python
class DinoGameBot:
    def __init__(self):
        self.jump_count = 0
        self.roi = None
        self.config_file = "roi_config.json"

    def jump(self):
        self.jump_count += 1
        ...
```

**장점:**
- 관련 데이터와 함수를 묶음
- 전역 변수 사용 감소
- 코드 재사용 용이

---

## DinoGameBot 클래스

### 기본 구조

```python
class DinoGameBot:
    def __init__(self, config_file="roi_config.json"):
        """봇 초기화"""
        self.config_file = config_file
        self.roi = None
        self.jump_count = 0
        self.running = False

        # 설정 로드
        self.load_roi_config()

        # 디버그 폴더 생성
        self.setup_debug_folder()

    def load_roi_config(self):
        """설정 파일 로드"""
        pass

    def setup_debug_folder(self):
        """디버그 폴더 생성"""
        pass

    def capture_roi(self):
        """ROI 캡처"""
        pass

    def is_obstacle_detected(self, gray_roi):
        """장애물 감지"""
        pass

    def jump(self):
        """점프 실행"""
        pass

    def save_debug_image(self, roi_img):
        """디버그 이미지 저장"""
        pass

    def run(self, check_interval=0.05):
        """메인 루프 실행"""
        pass
```

---

## 사용자 경험 개선

### 시작 메시지

```python
def print_startup_message(self):
    print("=" * 50)
    print("  Chrome Dino Game Bot")
    print("=" * 50)
    print(f"  ROI: ({self.roi['x1']}, {self.roi['y1']}) ~ "
          f"({self.roi['x2']}, {self.roi['y2']})")
    print(f"  크기: {self.roi['x2']-self.roi['x1']}x"
          f"{self.roi['y2']-self.roi['y1']}")
    print("=" * 50)
    print("  종료: Ctrl+C")
    print("=" * 50)
```

### 카운트다운

```python
def countdown(self, seconds=3):
    print(f"\n{seconds}초 후 시작합니다. 게임을 준비하세요!")
    for i in range(seconds, 0, -1):
        print(f"  {i}...")
        time.sleep(1)
    print("  시작!\n")
```

### 종료 요약

```python
def print_summary(self, elapsed_time):
    print("\n" + "=" * 50)
    print("  게임 종료")
    print("=" * 50)
    print(f"  총 점프: {self.jump_count}번")
    print(f"  실행 시간: {elapsed_time:.1f}초")
    if self.jump_count > 0:
        print(f"  평균: {elapsed_time / self.jump_count:.1f}초/점프")
    print("=" * 50)
```

---

## 에러 처리

### 설정 파일 없음

```python
def load_roi_config(self):
    try:
        with open(self.config_file, 'r') as f:
            config = json.load(f)
        self.roi = config['roi']
        print(f"설정 로드 완료: {self.config_file}")
    except FileNotFoundError:
        print(f"오류: {self.config_file} 파일을 찾을 수 없습니다!")
        print("먼저 calibrate.py를 실행해주세요.")
        exit(1)
```

### 실행 조건 확인

```python
def validate(self):
    """실행 전 검증"""
    if self.roi is None:
        print("오류: ROI가 설정되지 않았습니다.")
        return False

    # ROI 크기 확인
    width = self.roi['x2'] - self.roi['x1']
    height = self.roi['y2'] - self.roi['y1']
    if width < 10 or height < 10:
        print("오류: ROI가 너무 작습니다.")
        return False

    return True
```

---

## 생각해보기

### 질문 1: 개선 아이디어

현재 봇을 더 개선한다면 어떤 기능을 추가하겠습니까?

- 새(pterodactyl) 감지?
- 게임 속도 적응?
- 점수 인식?

### 질문 2: 야간 모드

게임이 야간 모드로 바뀌면 봇이 실패합니다.
어떻게 해결할 수 있을까요?

### 질문 3: 코드 분리

calibrate.py와 main.py에 중복되는 코드가 있습니다.
어떻게 공통 모듈로 분리할 수 있을까요?

---

## 실습 과제

### Exercise 12.1: DinoGameBot 클래스 틀

클래스의 기본 틀을 작성하세요.

**파일명**: `main.py`

```python
import os
import json
import time
import cv2
import numpy as np
import pyautogui
from PIL import ImageGrab
from datetime import datetime


class DinoGameBot:
    def __init__(self, config_file="roi_config.json"):
        """봇 초기화"""
        self.config_file = config_file
        self.roi = None
        self.jump_count = 0
        self.running = False

        # 설정 로드
        self.______()

        # 디버그 폴더
        self.______()

    def load_roi_config(self):
        """ROI 설정 로드"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.______(f)
            self.roi = config['roi']
            print(f"ROI 설정 로드 완료")
        except FileNotFoundError:
            print(f"오류: {self.config_file}를 찾을 수 없습니다!")
            print("먼저 calibrate.py를 실행하세요.")
            exit(1)

    def setup_debug_folder(self):
        """디버그 폴더 생성"""
        os.______(_______, exist_ok=True)


# 실행 테스트
if __name__ == "__main__":
    bot = DinoGameBot()
    print("봇 초기화 완료!")
    print(f"ROI: {bot.roi}")
```

### Exercise 12.2: 캡처 및 감지 메서드

핵심 메서드들을 구현하세요.

```python
def capture_roi(self):
    """ROI 영역 캡처"""
    screenshot = ImageGrab.______()
    img = np.array(screenshot)

    x1, y1 = self.roi['x1'], self.roi['y1']
    x2, y2 = self.roi['x2'], self.roi['y2']

    return img[______:______, ______:______]

def is_obstacle_detected(self, roi_img, threshold=128, ratio_threshold=0.05):
    """장애물 감지"""
    gray = cv2.cvtColor(roi_img, cv2.COLOR_______)

    avg_brightness = np.______(gray)
    dark_pixels = np.______(gray < threshold)
    dark_ratio = dark_pixels / gray.______

    is_detected = dark_ratio > ratio_threshold

    return is_detected, avg_brightness, dark_ratio
```

### Exercise 12.3: 점프 및 디버그 메서드

```python
def jump(self):
    """점프 실행"""
    pyautogui.______('space')
    self.jump_count += 1
    print(f"점프! (총 {self.jump_count}번)")

def save_debug_image(self, roi_img):
    """디버그 이미지 저장"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
    filename = f"debug_captures/jump_{self.jump_count:04d}_{timestamp}.png"

    bgr = cv2.cvtColor(roi_img, cv2.COLOR_RGB2______)
    cv2.imwrite(filename, bgr)

    return filename
```

### Exercise 12.4: 메인 루프 구현

```python
def run(self, check_interval=0.05, jump_cooldown=0.3):
    """메인 게임 루프"""
    self.running = True

    # 시작 메시지
    print("=" * 50)
    print("  Chrome Dino Game Bot")
    print("=" * 50)
    print(f"  ROI: {self.roi}")
    print("  종료: Ctrl+C")
    print("=" * 50)

    # 카운트다운
    print("\n3초 후 시작합니다...")
    for i in range(3, 0, -1):
        print(f"  {i}...")
        time.sleep(1)
    print("  시작!\n")

    start_time = time.time()

    try:
        while self.running:
            # 캡처
            roi_img = self.______()

            # 감지
            detected, brightness, ratio = self.______(roi_img)

            if detected:
                # 점프
                self.______()

                # 디버그 저장
                filename = self.______(roi_img)
                print(f"  밝기: {brightness:.1f}, 비율: {ratio*100:.1f}%")

                # 쿨다운
                time.sleep(______)
            else:
                time.sleep(______)

    except KeyboardInterrupt:
        pass

    # 종료 요약
    elapsed = time.time() - start_time
    print("\n" + "=" * 50)
    print("  게임 종료")
    print("=" * 50)
    print(f"  총 점프: {self.jump_count}번")
    print(f"  실행 시간: {elapsed:.1f}초")
    print("=" * 50)
```

### Exercise 12.5: 완성 및 테스트

모든 것을 조립하고 테스트하세요.

```python
class DinoGameBot:
    def __init__(self, config_file="roi_config.json"):
        self.config_file = config_file
        self.roi = None
        self.jump_count = 0
        self.running = False

        self.load_roi_config()
        self.setup_debug_folder()

    def load_roi_config(self):
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            self.roi = config['roi']
            print("ROI 설정 로드 완료")
        except FileNotFoundError:
            print(f"오류: {self.config_file}를 찾을 수 없습니다!")
            print("calibrate.py를 먼저 실행하세요.")
            exit(1)

    def setup_debug_folder(self):
        os.makedirs("debug_captures", exist_ok=True)

    def capture_roi(self):
        screenshot = ImageGrab.grab()
        img = np.array(screenshot)
        x1, y1 = self.roi['x1'], self.roi['y1']
        x2, y2 = self.roi['x2'], self.roi['y2']
        return img[y1:y2, x1:x2]

    def is_obstacle_detected(self, roi_img, threshold=128, ratio_threshold=0.05):
        gray = cv2.cvtColor(roi_img, cv2.COLOR_RGB2GRAY)
        avg_brightness = np.mean(gray)
        dark_pixels = np.sum(gray < threshold)
        dark_ratio = dark_pixels / gray.size
        return dark_ratio > ratio_threshold, avg_brightness, dark_ratio

    def jump(self):
        pyautogui.press('space')
        self.jump_count += 1
        print(f"점프! (총 {self.jump_count}번)")

    def save_debug_image(self, roi_img):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
        filename = f"debug_captures/jump_{self.jump_count:04d}_{timestamp}.png"
        bgr = cv2.cvtColor(roi_img, cv2.COLOR_RGB2BGR)
        cv2.imwrite(filename, bgr)
        return filename

    def run(self, check_interval=0.05, jump_cooldown=0.3):
        # ... (위의 코드)
        pass


if __name__ == "__main__":
    bot = DinoGameBot()
    bot.run()
```

---

## 최종 테스트

### 테스트 체크리스트

1. **calibrate.py 실행**
   - [ ] 화면이 표시되는가?
   - [ ] 마우스 드래그로 영역 선택이 되는가?
   - [ ] 's'로 저장이 되는가?
   - [ ] roi_config.json 파일이 생성되는가?

2. **main.py 실행**
   - [ ] ROI 설정이 로드되는가?
   - [ ] 카운트다운이 표시되는가?
   - [ ] 장애물 감지 시 점프하는가?
   - [ ] 디버그 이미지가 저장되는가?
   - [ ] Ctrl+C로 종료되는가?
   - [ ] 종료 요약이 표시되는가?

3. **실제 게임 플레이**
   - [ ] 30초 이상 자동 플레이 가능한가?
   - [ ] 놓치는 장애물이 적은가?
   - [ ] 오탐지(잘못된 점프)가 적은가?

---

## 예상 결과

### 정상 실행 예시

```
ROI 설정 로드 완료
==================================================
  Chrome Dino Game Bot
==================================================
  ROI: {'x1': 456, 'y1': 320, 'x2': 546, 'y2': 370}
  종료: Ctrl+C
==================================================

3초 후 시작합니다...
  3...
  2...
  1...
  시작!

점프! (총 1번)
  밝기: 198.3, 비율: 12.4%
점프! (총 2번)
  밝기: 187.6, 비율: 18.7%
점프! (총 3번)
  밝기: 192.1, 비율: 15.3%
...

==================================================
  게임 종료
==================================================
  총 점프: 47번
  실행 시간: 125.3초
==================================================
```

---

## 핵심 정리

### 클래스 구조

```python
class DinoGameBot:
    __init__()          # 초기화
    load_roi_config()   # 설정 로드
    setup_debug_folder()# 디버그 폴더
    capture_roi()       # ROI 캡처
    is_obstacle_detected() # 감지
    jump()              # 점프
    save_debug_image()  # 디버그 저장
    run()               # 메인 루프
```

### 실행 흐름

```
calibrate.py → roi_config.json → main.py → 게임 자동화
```

### 완성된 프로젝트

```
✓ 화면 캡처 (Pillow)
✓ 이미지 처리 (NumPy, OpenCV)
✓ 장애물 감지 (밝기 분석)
✓ 키보드 자동화 (PyAutoGUI)
✓ 설정 관리 (JSON)
✓ 캘리브레이션 도구
✓ 게임 루프
```

---

## 체크포인트

- [ ] DinoGameBot 클래스를 완성했다
- [ ] calibrate.py가 정상 작동한다
- [ ] main.py가 정상 작동한다
- [ ] 실제 게임에서 30초 이상 자동 플레이에 성공했다

---

## 축하합니다!

**미션 완료!**

아무것도 없는 상태에서 "비디오 게임을 대신 플레이하는 AI"를 만들었습니다.

### 배운 것들

1. **제1원칙 사고방식**: 문제를 근본부터 분해
2. **화면 캡처**: Pillow ImageGrab
3. **이미지 처리**: NumPy 배열, OpenCV
4. **장애물 감지**: 밝기 분석, 임계값
5. **키보드 자동화**: PyAutoGUI
6. **설정 관리**: JSON
7. **사용자 인터페이스**: OpenCV 윈도우, 마우스 이벤트
8. **프로그램 구조화**: 클래스, 에러 처리

### 다음 단계

[부록 C: 다음 단계](../부록/appendix-c-next-steps.md)에서 프로젝트를 더 발전시킬 아이디어를 확인하세요!

---

[← 목차로 돌아가기](../README.md)
