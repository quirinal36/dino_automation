# 부록 B: 용어 사전

이 문서는 워크북에서 사용하는 기술 용어들을 정리합니다.

---

## A

### Array (배열)
같은 타입의 데이터를 순서대로 저장하는 자료구조. NumPy에서는 다차원 배열을 효율적으로 처리합니다.
```python
import numpy as np
arr = np.array([1, 2, 3])       # 1차원 배열
arr2d = np.array([[1,2], [3,4]])  # 2차원 배열
```

---

## B

### BGR
Blue-Green-Red의 약자. OpenCV에서 사용하는 색상 채널 순서. RGB와 반대 순서입니다.
```python
# BGR에서 빨간색
red_bgr = [0, 0, 255]  # B=0, G=0, R=255
```

### Boolean (불리언)
참(True) 또는 거짓(False)만 가지는 자료형.
```python
is_obstacle = True
```

### Brightness (밝기)
픽셀의 밝은 정도. 0(검정)~255(흰색) 범위로 표현됩니다.

---

## C

### Calibration (캘리브레이션)
보정, 조정의 의미. 이 프로젝트에서는 사용자 화면에 맞게 ROI 좌표를 설정하는 과정입니다.

### Callback (콜백)
특정 이벤트가 발생했을 때 호출되는 함수.
```python
def mouse_callback(event, x, y, flags, param):
    pass  # 마우스 이벤트 발생 시 호출됨
```

### Channel (채널)
이미지의 색상 구성 요소. RGB 이미지는 R, G, B 3개 채널을 가집니다.

### Class (클래스)
객체 지향 프로그래밍에서 데이터와 기능을 묶는 구조.
```python
class DinoGameBot:
    def __init__(self):
        self.jump_count = 0
```

### Cooldown (쿨다운)
동작 후 일정 시간 대기. 연속 실행을 방지합니다.

### cv2
OpenCV의 Python 모듈 이름.
```python
import cv2
```

---

## D

### Dictionary (딕셔너리)
키-값 쌍으로 데이터를 저장하는 Python 자료구조.
```python
roi = {'x1': 100, 'y1': 200, 'x2': 300, 'y2': 400}
```

### dtype
NumPy 배열의 데이터 타입. 이미지는 보통 `uint8` (0-255).
```python
print(arr.dtype)  # uint8
```

---

## E

### Event (이벤트)
마우스 클릭, 키보드 입력 등 사용자의 동작.

### Exception (예외)
프로그램 실행 중 발생하는 에러.
```python
try:
    # 코드
except FileNotFoundError:
    # 파일 없음 처리
```

---

## F

### Fail-Safe (페일세이프)
비상 정지 기능. PyAutoGUI에서 마우스를 구석으로 이동하면 프로그램이 중지됩니다.

### First Principles Thinking (제1원칙 사고방식)
문제를 가장 기본적인 요소로 분해하고 그로부터 해결책을 도출하는 사고 방식.

### FPS (Frames Per Second)
초당 프레임 수. 1초에 몇 번 화면을 처리하는지 나타냅니다.

---

## G

### Grayscale (그레이스케일)
흑백 이미지. 각 픽셀이 하나의 밝기 값(0-255)만 가집니다.
```python
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
```

---

## I

### ImageGrab
Pillow 라이브러리에서 화면을 캡처하는 모듈.
```python
from PIL import ImageGrab
screenshot = ImageGrab.grab()
```

### import
Python에서 모듈을 불러오는 키워드.
```python
import cv2
from PIL import ImageGrab
```

### indent (들여쓰기)
코드의 계층 구조를 나타내는 공백. JSON에서 가독성을 위해 사용.

---

## J

### JSON (JavaScript Object Notation)
데이터를 저장하고 전송하는 텍스트 형식.
```json
{
    "roi": {
        "x1": 100,
        "y1": 200
    }
}
```

---

## K

### KeyboardInterrupt
사용자가 Ctrl+C를 눌렀을 때 발생하는 예외.

---

## L

### Loop (루프)
반복 실행되는 코드 블록.
```python
while True:
    # 반복 실행
```

---

## M

### mean (평균)
값들의 합을 개수로 나눈 값.
```python
avg = np.mean(arr)
```

### Module (모듈)
관련된 코드를 묶은 Python 파일.

### Mouse Event (마우스 이벤트)
마우스 동작 (클릭, 이동 등)으로 발생하는 이벤트.

---

## N

### NumPy
수치 연산을 위한 Python 라이브러리. 배열 처리에 최적화되어 있습니다.
```python
import numpy as np
```

---

## O

### OpenCV
오픈소스 컴퓨터 비전 라이브러리.
```python
import cv2
```

---

## P

### Pillow
Python 이미지 처리 라이브러리. PIL의 후속 프로젝트.
```python
from PIL import Image, ImageGrab
```

### Pixel (픽셀)
디지털 이미지의 최소 단위. 화면의 한 점.

### PyAutoGUI
키보드와 마우스를 자동화하는 Python 라이브러리.
```python
import pyautogui
pyautogui.press('space')
```

---

## R

### Ratio (비율)
전체 대비 부분의 비. 백분율로 표현하기도 함.
```python
ratio = dark_pixels / total_pixels  # 0.05 = 5%
```

### RGB
Red-Green-Blue의 약자. 빛의 삼원색으로 색상을 표현하는 방식.
```python
# RGB에서 빨간색
red_rgb = [255, 0, 0]  # R=255, G=0, B=0
```

### ROI (Region of Interest)
관심 영역. 전체 이미지 중 분석할 특정 사각형 영역.
```python
roi = img[y1:y2, x1:x2]
```

---

## S

### Shape (형태)
NumPy 배열의 각 차원 크기.
```python
img.shape  # (1080, 1920, 3) = 높이, 너비, 채널
```

### Slicing (슬라이싱)
배열의 일부를 추출하는 방법.
```python
arr[start:end]    # start부터 end-1까지
img[y1:y2, x1:x2] # 2차원 슬라이싱
```

---

## T

### Threshold (임계값)
기준값. 이 값을 기준으로 참/거짓을 판단.
```python
is_dark = pixel < 128  # 128이 임계값
```

### Tuple (튜플)
변경 불가능한 순서가 있는 자료구조.
```python
point = (100, 200)  # x, y 좌표
```

---

## U

### uint8
8비트 부호 없는 정수. 0-255 범위. 이미지 픽셀 값의 기본 타입.

---

## V

### Variable (변수)
데이터를 저장하는 이름이 붙은 공간.
```python
jump_count = 0
```

### Virtual Environment (가상 환경)
프로젝트별로 독립된 Python 환경.
```bash
python -m venv venv
```

---

## W

### Window (윈도우)
GUI에서 이미지나 컨텐츠를 표시하는 창.
```python
cv2.namedWindow("창 이름")
```

---

## 수학 기호

### < (미만)
왼쪽이 오른쪽보다 작음.
```python
gray < 128  # 128 미만인 픽셀
```

### > (초과)
왼쪽이 오른쪽보다 큼.
```python
ratio > 0.05  # 5% 초과
```

### // (정수 나눗셈)
나눗셈 후 정수 부분만 반환.
```python
10 // 3  # 결과: 3
```

---

[← 목차로 돌아가기](../README.md)
