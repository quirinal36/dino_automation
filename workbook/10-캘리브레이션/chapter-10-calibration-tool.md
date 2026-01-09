# 챕터 10: 캘리브레이션 도구

> "사용자 친화적인 설정 도구를 만들자"

---

## 학습 목표

- OpenCV 윈도우를 생성하고 제어한다
- 마우스 이벤트를 처리한다
- 드래그로 사각형을 선택하는 기능을 구현한다
- 완전한 캘리브레이션 도구를 완성한다

---

## 캘리브레이션 도구란?

### 목적

사용자가 **마우스로 ROI 영역을 선택**하면 자동으로 좌표를 저장하는 도구입니다.

### 사용 흐름

```
1. 도구 실행
2. 현재 화면 캡처 및 표시
3. 사용자가 마우스로 영역 드래그
4. 's' 키로 저장
5. 좌표가 roi_config.json에 저장됨
```

### 왜 필요한가?

- 화면마다 좌표가 다름
- 숫자로 좌표를 찾기 어려움
- **시각적으로** 영역을 선택하는 것이 편리

---

## OpenCV 윈도우

### 윈도우 생성

```python
import cv2

# 윈도우 생성
cv2.namedWindow("창 이름")

# 이미지 표시
cv2.imshow("창 이름", image)

# 키 입력 대기 (ms, 0=무한)
key = cv2.waitKey(0)

# 윈도우 닫기
cv2.destroyAllWindows()
```

### waitKey 이해하기

```python
# 무한 대기
key = cv2.waitKey(0)

# 1ms 대기 (루프에서 사용)
key = cv2.waitKey(1)

# 키 코드 확인
if key == ord('q'):  # 'q' 키
    print("종료!")
```

---

## 마우스 이벤트

### 콜백 함수

```python
def mouse_callback(event, x, y, flags, param):
    """
    마우스 이벤트 처리 함수

    Args:
        event: 이벤트 타입 (클릭, 이동 등)
        x, y: 마우스 좌표
        flags: 추가 정보 (Ctrl, Shift 등)
        param: 사용자 데이터
    """
    pass
```

### 주요 이벤트 타입

| 이벤트 | 설명 |
|--------|------|
| `cv2.EVENT_LBUTTONDOWN` | 왼쪽 버튼 누름 |
| `cv2.EVENT_LBUTTONUP` | 왼쪽 버튼 뗌 |
| `cv2.EVENT_MOUSEMOVE` | 마우스 이동 |

### 콜백 등록

```python
cv2.namedWindow("창 이름")
cv2.setMouseCallback("창 이름", mouse_callback)
```

---

## 드래그 구현

### 상태 변수

```python
# 드래그 상태 추적
drawing = False      # 현재 드래그 중인가?
start_point = None   # 드래그 시작점
end_point = None     # 드래그 끝점
```

### 이벤트 처리

```python
def mouse_callback(event, x, y, flags, param):
    global drawing, start_point, end_point

    if event == cv2.EVENT_LBUTTONDOWN:
        # 드래그 시작
        drawing = True
        start_point = (x, y)

    elif event == cv2.EVENT_MOUSEMOVE:
        # 드래그 중
        if drawing:
            end_point = (x, y)

    elif event == cv2.EVENT_LBUTTONUP:
        # 드래그 끝
        drawing = False
        end_point = (x, y)
```

---

## 사각형 그리기

### cv2.rectangle()

```python
cv2.rectangle(
    image,      # 그릴 이미지
    pt1,        # 왼쪽 위 (x1, y1)
    pt2,        # 오른쪽 아래 (x2, y2)
    color,      # 색상 (B, G, R)
    thickness   # 선 두께 (-1이면 채움)
)
```

### 예시

```python
# 초록색 사각형, 두께 2
cv2.rectangle(img, (100, 100), (300, 200), (0, 255, 0), 2)
```

---

## 좌표 정규화

### 문제

사용자가 어느 방향으로 드래그할지 모름:

```
Case 1: 왼쪽 위 → 오른쪽 아래 (정상)
Case 2: 오른쪽 아래 → 왼쪽 위 (반대)
Case 3: 오른쪽 위 → 왼쪽 아래
Case 4: 왼쪽 아래 → 오른쪽 위
```

### 해결

항상 x1 < x2, y1 < y2가 되도록 정규화:

```python
x1 = min(start_point[0], end_point[0])
y1 = min(start_point[1], end_point[1])
x2 = max(start_point[0], end_point[0])
y2 = max(start_point[1], end_point[1])
```

---

## 생각해보기

### 질문 1: 이미지 복사

왜 사각형을 그릴 때 원본 이미지의 복사본을 사용해야 할까요?

```python
# 왜 이렇게?
display = original.copy()
cv2.rectangle(display, ...)
```

### 질문 2: 좌표 검증

사용자가 너무 작은 영역을 선택하면?
사용자가 화면 밖을 드래그하면?

어떻게 처리해야 할까요?

### 질문 3: 다시 캡처

캘리브레이션 중에 게임 화면이 바뀌면?
다시 캡처하는 기능이 왜 필요할까요?

---

## 실습 과제

### Exercise 10.1: 기본 윈도우

OpenCV 윈도우를 생성하고 이미지를 표시하세요.

**파일명**: `calibrate_test.py`

```python
import cv2
import numpy as np
from PIL import ImageGrab

# 1. 화면 캡처
screenshot = ImageGrab.grab()
img = np.array(screenshot)

# 2. RGB → BGR (OpenCV용)
img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2______)

# 3. 윈도우 생성 및 표시
cv2.______("ROI Calibration")
cv2.______("ROI Calibration", img_bgr)

# 4. 키 입력 대기
print("아무 키나 누르면 종료...")
cv2.______(0)
cv2.______()
```

### Exercise 10.2: 마우스 클릭

마우스 클릭 좌표를 출력하세요.

```python
def mouse_callback(event, x, y, flags, param):
    if event == cv2.______:
        print(f"클릭: ({x}, {y})")

# 콜백 등록
cv2.namedWindow("Test")
cv2.______("Test", mouse_callback)
cv2.imshow("Test", img_bgr)

print("클릭해보세요. 'q'를 누르면 종료.")
while True:
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cv2.destroyAllWindows()
```

### Exercise 10.3: 드래그 추적

드래그 시작과 끝을 추적하세요.

```python
drawing = False
start_point = None
end_point = None

def mouse_callback(event, x, y, flags, param):
    global drawing, start_point, end_point

    if event == cv2.EVENT_LBUTTONDOWN:
        ______ = True
        ______ = (x, y)
        print(f"드래그 시작: {start_point}")

    elif event == cv2.EVENT_MOUSEMOVE:
        if ______:
            ______ = (x, y)

    elif event == cv2.EVENT_LBUTTONUP:
        ______ = False
        ______ = (x, y)
        print(f"드래그 끝: {end_point}")

        # 좌표 정규화
        x1 = ______(start_point[0], end_point[0])
        y1 = ______(start_point[1], end_point[1])
        x2 = ______(start_point[0], end_point[0])
        y2 = ______(start_point[1], end_point[1])
        print(f"ROI: ({x1}, {y1}) ~ ({x2}, {y2})")
```

### Exercise 10.4: 사각형 표시

드래그하는 동안 사각형을 표시하세요.

```python
original = img_bgr.copy()  # 원본 보관

def mouse_callback(event, x, y, flags, param):
    global drawing, start_point, end_point

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        start_point = (x, y)

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            end_point = (x, y)
            # 원본 복사 후 사각형 그리기
            display = ______.copy()
            cv2.______(display, start_point, end_point, (0, 255, 0), 2)
            cv2.imshow("Calibration", display)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        end_point = (x, y)

cv2.namedWindow("Calibration")
cv2.setMouseCallback("Calibration", mouse_callback)
cv2.imshow("Calibration", img_bgr)

while cv2.waitKey(1) != ord('q'):
    pass

cv2.destroyAllWindows()
```

### Exercise 10.5: 완전한 캘리브레이션 도구

저장 기능까지 추가한 완전한 도구를 만드세요.

```python
import cv2
import numpy as np
import json
from PIL import ImageGrab

class ROICalibrator:
    def __init__(self):
        self.drawing = False
        self.start_point = None
        self.end_point = None
        self.original = None
        self.window_name = "ROI Calibration"

    def capture_screen(self):
        """화면 캡처"""
        screenshot = ImageGrab.grab()
        img = np.array(screenshot)
        self.original = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        return self.original.copy()

    def mouse_callback(self, event, x, y, flags, param):
        """마우스 이벤트 처리"""
        # 여기에 구현...
        pass

    def get_roi(self):
        """정규화된 ROI 좌표 반환"""
        if self.start_point and self.end_point:
            x1 = min(self.start_point[0], self.end_point[0])
            y1 = min(self.start_point[1], self.end_point[1])
            x2 = max(self.start_point[0], self.end_point[0])
            y2 = max(self.start_point[1], self.end_point[1])
            return (x1, y1, x2, y2)
        return None

    def save_config(self, filename="roi_config.json"):
        """ROI를 JSON으로 저장"""
        roi = self.get_roi()
        if roi:
            x1, y1, x2, y2 = roi
            config = {
                "roi": {"x1": x1, "y1": y1, "x2": x2, "y2": y2},
                "width": x2 - x1,
                "height": y2 - y1
            }
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4)
            print(f"저장 완료: {filename}")
            return True
        return False

    def run(self):
        """캘리브레이션 실행"""
        print("=" * 50)
        print("ROI 캘리브레이션 도구")
        print("=" * 50)
        print("사용법:")
        print("  - 마우스 드래그: ROI 영역 선택")
        print("  - 's': 저장")
        print("  - 'r': 화면 다시 캡처")
        print("  - 'q': 종료")
        print("=" * 50)

        img = self.capture_screen()
        cv2.namedWindow(self.window_name)
        cv2.setMouseCallback(self.window_name, self.mouse_callback)
        cv2.imshow(self.window_name, img)

        while True:
            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):
                break
            elif key == ord('s'):
                if self.save_config():
                    print("ROI가 저장되었습니다!")
            elif key == ord('r'):
                img = self.capture_screen()
                cv2.imshow(self.window_name, img)
                print("화면을 다시 캡처했습니다.")

        cv2.destroyAllWindows()


if __name__ == "__main__":
    calibrator = ROICalibrator()
    calibrator.run()
```

---

## 예상 결과

### 도구 실행 화면

```
==================================================
ROI 캘리브레이션 도구
==================================================
사용법:
  - 마우스 드래그: ROI 영역 선택
  - 's': 저장
  - 'r': 화면 다시 캡처
  - 'q': 종료
==================================================
```

### 저장 성공

```
저장 완료: roi_config.json
ROI가 저장되었습니다!
```

### 생성된 파일

**roi_config.json:**
```json
{
    "roi": {
        "x1": 456,
        "y1": 320,
        "x2": 546,
        "y2": 370
    },
    "width": 90,
    "height": 50
}
```

---

## 핵심 정리

### OpenCV 윈도우

```python
cv2.namedWindow("이름")
cv2.imshow("이름", image)
cv2.waitKey(ms)
cv2.destroyAllWindows()
```

### 마우스 콜백

```python
def callback(event, x, y, flags, param):
    pass

cv2.setMouseCallback("윈도우이름", callback)
```

### 주요 이벤트

```python
cv2.EVENT_LBUTTONDOWN  # 누름
cv2.EVENT_MOUSEMOVE    # 이동
cv2.EVENT_LBUTTONUP    # 뗌
```

### 드래그 패턴

```python
if LBUTTONDOWN:
    drawing = True
    start = (x, y)
elif MOUSEMOVE and drawing:
    end = (x, y)
    # 사각형 그리기
elif LBUTTONUP:
    drawing = False
    end = (x, y)
```

---

## 체크포인트

- [ ] OpenCV 윈도우를 생성하고 제어할 수 있다
- [ ] 마우스 콜백을 등록하고 이벤트를 처리할 수 있다
- [ ] 드래그 동작을 추적할 수 있다
- [ ] 선택한 영역에 사각형을 그릴 수 있다
- [ ] 완전한 캘리브레이션 도구를 만들었다

---

## 다음 챕터 미리보기

**챕터 11: 게임 루프**에서는 지금까지 만든 모든 기능을 연결하여 실제로 게임을 플레이하는 메인 루프를 구현합니다. 캡처 → 분석 → 점프의 사이클을 반복하는 자동화 엔진을 완성합니다.

[다음 챕터로 이동 →](../11-게임루프/chapter-11-game-loop.md)
