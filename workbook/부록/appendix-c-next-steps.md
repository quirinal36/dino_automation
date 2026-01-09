# 부록 C: 다음 단계

축하합니다! 기본 Dino Game Bot을 완성했습니다. 이 문서는 프로젝트를 더 발전시킬 수 있는 아이디어들을 제시합니다.

---

## 난이도별 개선 아이디어

### 초급 개선

#### 1. 설정 파일 확장

현재 ROI만 저장하고 있지만, 더 많은 설정을 추가할 수 있습니다.

```json
{
    "roi": { "x1": 450, "y1": 320, "x2": 550, "y2": 370 },
    "detection": {
        "brightness_threshold": 128,
        "ratio_threshold": 0.05
    },
    "timing": {
        "check_interval": 0.05,
        "jump_cooldown": 0.3
    }
}
```

**힌트:**
- main.py에서 이 값들을 로드해서 사용
- 게임 속도에 따라 값을 조정 가능

#### 2. 통계 기록

게임 결과를 파일로 저장합니다.

```python
import csv
from datetime import datetime

def save_stats(jump_count, duration):
    with open("game_stats.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now(), jump_count, duration])
```

**활용:**
- 시간대별 성과 분석
- 최고 기록 추적

#### 3. 소리 알림

점프할 때 소리를 재생합니다.

```python
import winsound  # Windows only

def beep():
    winsound.Beep(1000, 100)  # 1000Hz, 100ms
```

---

### 중급 개선

#### 4. 새(Pterodactyl) 대응

새는 높은 위치와 낮은 위치로 날아옵니다.

**아이디어:**
- 두 번째 ROI를 높은 위치에 추가
- 낮은 새: 점프로 피함
- 높은 새: 숙이기(down arrow)로 피함

```python
class DinoGameBot:
    def __init__(self):
        self.roi_ground = {...}  # 지면 장애물용
        self.roi_air = {...}     # 새용

    def run(self):
        # 지면 감지
        ground_obstacle = self.check_ground()
        # 공중 감지
        air_obstacle = self.check_air()

        if air_obstacle:
            self.duck()  # 숙이기
        elif ground_obstacle:
            self.jump()
```

#### 5. 야간 모드 대응

게임이 야간 모드로 바뀌면 색상이 반전됩니다.

**아이디어:**
- 평균 밝기로 모드 감지
- 야간: 밝은 픽셀을 장애물로 인식

```python
def detect_mode(self, roi_img):
    avg = np.mean(roi_img)
    return "night" if avg < 100 else "day"

def is_obstacle_detected(self, roi_img):
    mode = self.detect_mode(roi_img)
    gray = cv2.cvtColor(roi_img, cv2.COLOR_RGB2GRAY)

    if mode == "day":
        # 어두운 픽셀 감지
        return np.sum(gray < 128) / gray.size > 0.05
    else:
        # 밝은 픽셀 감지 (야간)
        return np.sum(gray > 128) / gray.size > 0.05
```

#### 6. 동적 임계값 조정

게임 진행에 따라 자동으로 임계값을 조정합니다.

```python
class AdaptiveDetector:
    def __init__(self):
        self.brightness_history = []

    def update_threshold(self, current_brightness):
        self.brightness_history.append(current_brightness)
        if len(self.brightness_history) > 100:
            self.brightness_history.pop(0)

        # 최근 평균 기준으로 임계값 조정
        avg = np.mean(self.brightness_history)
        return avg * 0.7  # 평균의 70%
```

---

### 고급 개선

#### 7. 점수 인식 (OCR)

화면에서 점수를 읽어옵니다.

**도구:** Tesseract OCR, EasyOCR

```python
import easyocr

reader = easyocr.Reader(['en'])

def read_score(score_roi):
    result = reader.readtext(score_roi)
    if result:
        return int(result[0][1])
    return 0
```

**활용:**
- 점수별 전략 변경
- 고득점 달성 시 알림

#### 8. 게임 속도 적응

게임 속도가 빨라지면 반응도 빨라져야 합니다.

**아이디어:**
- 장애물 간 시간 간격 측정
- 간격이 짧아지면 체크 간격 감소

```python
class SpeedAdapter:
    def __init__(self):
        self.last_obstacle_time = None
        self.intervals = []

    def record_obstacle(self):
        now = time.time()
        if self.last_obstacle_time:
            interval = now - self.last_obstacle_time
            self.intervals.append(interval)
        self.last_obstacle_time = now

    def get_check_interval(self):
        if len(self.intervals) < 5:
            return 0.05  # 기본값

        avg_interval = np.mean(self.intervals[-10:])
        # 장애물 간격이 짧으면 더 자주 체크
        return min(0.05, avg_interval / 10)
```

#### 9. 머신러닝 기반 감지

딥러닝으로 장애물을 더 정확하게 인식합니다.

**접근법:**
1. 디버그 이미지로 학습 데이터 수집
2. CNN 모델 학습 (장애물 있음/없음 분류)
3. 학습된 모델로 실시간 감지

**도구:** TensorFlow, PyTorch, scikit-learn

#### 10. GUI 인터페이스

Tkinter나 PyQt로 사용자 친화적 UI를 만듭니다.

**기능:**
- 실시간 ROI 프리뷰
- 설정 슬라이더 (임계값 조정)
- 시작/정지 버튼
- 통계 그래프

```python
import tkinter as tk
from PIL import Image, ImageTk

class BotGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Dino Game Bot")

        # ROI 프리뷰
        self.preview_label = tk.Label(self.root)
        self.preview_label.pack()

        # 시작 버튼
        self.start_btn = tk.Button(
            self.root,
            text="Start",
            command=self.start_bot
        )
        self.start_btn.pack()
```

---

## 완전히 새로운 프로젝트 아이디어

### 다른 게임 자동화

같은 기술로 다른 게임도 자동화할 수 있습니다:

1. **Flappy Bird 클론**
   - 장애물 감지 → 클릭/탭

2. **2048**
   - 타일 인식 → 최적 방향 결정 → 키 입력

3. **테트리스**
   - 블록 인식 → 최적 위치 계산 → 이동/회전

### 실생활 자동화

1. **화면 모니터링**
   - 특정 패턴 감지 시 알림

2. **자동 클리커**
   - 특정 이미지 찾아서 클릭

3. **데이터 입력 자동화**
   - 화면 읽기 → 키보드 입력

---

## 학습 자료

### 컴퓨터 비전

- [OpenCV 공식 튜토리얼](https://docs.opencv.org/master/d9/df8/tutorial_root.html)
- [OpenCV-Python Tutorials](https://opencv-python-tutroials.readthedocs.io/)

### 머신러닝

- [scikit-learn 공식 문서](https://scikit-learn.org/)
- [TensorFlow 튜토리얼](https://www.tensorflow.org/tutorials)

### 게임 AI

- [OpenAI Gym](https://gym.openai.com/) - 강화학습 환경
- [PyGame](https://www.pygame.org/) - 게임 개발

---

## 마무리

이 워크북에서 배운 것들:

1. **제1원칙 사고방식** - 문제를 근본부터 분해
2. **화면 캡처** - Pillow로 시각 데이터 획득
3. **이미지 처리** - NumPy, OpenCV로 분석
4. **패턴 감지** - 임계값 기반 로직
5. **자동화** - PyAutoGUI로 입력 시뮬레이션
6. **설정 관리** - JSON으로 데이터 영속화
7. **프로그램 구조화** - 클래스와 모듈

이 기술들은 게임 자동화를 넘어 다양한 분야에 적용할 수 있습니다.

**계속 만들고, 계속 배우세요!**

---

[← 목차로 돌아가기](../README.md)
