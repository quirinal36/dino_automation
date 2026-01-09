# 챕터 9: 설정 저장

> "기억하는 봇을 만들자"

---

## 학습 목표

- JSON 형식을 이해한다
- Python에서 JSON 파일을 읽고 쓴다
- ROI 좌표를 설정 파일로 관리한다
- 에러 처리를 구현한다

---

## 왜 설정 파일이 필요한가?

### 문제 상황

ROI 좌표를 코드에 직접 작성하면:

```python
# main.py
x1, y1 = 450, 320
x2, y2 = 550, 370
```

**문제점:**
- 좌표를 바꾸려면 코드 수정 필요
- 다른 컴퓨터에서 다시 찾아야 함
- 캘리브레이션 결과를 저장할 수 없음

### 해결책

좌표를 **별도 파일**에 저장:

```
roi_config.json  ←  캘리브레이션 결과 저장
      ↓
   main.py  ←  파일에서 좌표 읽어옴
```

---

## JSON이란?

### 소개

**JSON** (JavaScript Object Notation)

- 데이터를 저장하고 전송하는 텍스트 형식
- 사람이 읽기 쉬움
- 대부분의 프로그래밍 언어에서 지원

### 기본 구조

```json
{
    "이름": "값",
    "숫자": 123,
    "참거짓": true,
    "배열": [1, 2, 3],
    "중첩": {
        "내부키": "내부값"
    }
}
```

### Python 딕셔너리와 비교

| JSON | Python |
|------|--------|
| `{}` | `{}` (dict) |
| `[]` | `[]` (list) |
| `"text"` | `"text"` |
| `123` | `123` |
| `true` / `false` | `True` / `False` |
| `null` | `None` |

---

## ROI 설정 파일 구조

### 우리가 사용할 형식

```json
{
    "roi": {
        "x1": 450,
        "y1": 320,
        "x2": 550,
        "y2": 370
    },
    "width": 100,
    "height": 50
}
```

**설명:**
- `roi`: 좌표 정보를 담은 객체
- `width`, `height`: 편의를 위한 크기 정보

---

## JSON 파일 쓰기

### 기본 방법

```python
import json

# 저장할 데이터
data = {
    "roi": {
        "x1": 450,
        "y1": 320,
        "x2": 550,
        "y2": 370
    }
}

# 파일에 쓰기
with open("config.json", "w", encoding="utf-8") as f:
    json.______(data, f)
```

### 보기 좋게 저장

```python
# indent로 들여쓰기 추가
json.dump(data, f, indent=4)
```

**indent=4 적용 전:**
```json
{"roi":{"x1":450,"y1":320,"x2":550,"y2":370}}
```

**indent=4 적용 후:**
```json
{
    "roi": {
        "x1": 450,
        "y1": 320,
        "x2": 550,
        "y2": 370
    }
}
```

---

## JSON 파일 읽기

### 기본 방법

```python
import json

# 파일에서 읽기
with open("config.json", "r", encoding="utf-8") as f:
    data = json.______(f)

# 사용
print(data["roi"]["x1"])  # 450
```

### 데이터 접근

```python
roi = data["roi"]
x1 = roi["x1"]
y1 = roi["y1"]
x2 = roi["x2"]
y2 = roi["y2"]
```

---

## 에러 처리

### 파일이 없을 때

```python
try:
    with open("config.json", "r") as f:
        data = json.load(f)
except FileNotFoundError:
    print("설정 파일이 없습니다!")
    data = None
```

### JSON 형식 오류

```python
try:
    with open("config.json", "r") as f:
        data = json.load(f)
except json.JSONDecodeError:
    print("JSON 형식이 잘못되었습니다!")
    data = None
```

### 통합 에러 처리

```python
def load_config(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"파일 없음: {filename}")
        return None
    except json.JSONDecodeError:
        print(f"JSON 오류: {filename}")
        return None
```

---

## 생각해보기

### 질문 1: 파일 형식

왜 JSON을 사용할까요?
- 단순 텍스트 파일 (`450,320,550,370`)
- Python pickle
- YAML

각각의 장단점은?

### 질문 2: 에러 처리

설정 파일이 없을 때 프로그램은 어떻게 해야 할까요?
- 종료?
- 기본값 사용?
- 사용자에게 안내?

### 질문 3: 추가 설정

ROI 외에 저장하면 좋을 설정은?
- 감지 임계값?
- 쿨다운 시간?
- 체크 간격?

---

## 실습 과제

### Exercise 9.1: JSON 쓰기

ROI 좌표를 JSON 파일로 저장하세요.

**파일명**: `json_test.py`

```python
import json

# ROI 좌표
x1, y1 = 450, 320
x2, y2 = 550, 370

# 데이터 구조 만들기
config = {
    "roi": {
        "x1": ______,
        "y1": ______,
        "x2": ______,
        "y2": ______
    },
    "width": ______ - ______,
    "height": ______ - ______
}

# JSON 파일로 저장
with open("roi_config.json", "____", encoding="utf-8") as f:
    json.______(config, f, indent=4)

print("설정 저장 완료!")
print("roi_config.json 파일을 열어보세요.")
```

### Exercise 9.2: JSON 읽기

저장한 파일을 읽어오세요.

```python
import json

# 파일 읽기
with open("roi_config.json", "____", encoding="utf-8") as f:
    config = json.______(f)

# 데이터 접근
roi = config["roi"]
print(f"x1: {roi['x1']}")
print(f"y1: {roi['y1']}")
print(f"x2: {roi['x2']}")
print(f"y2: {roi['y2']}")
print(f"크기: {config['width']}x{config['height']}")
```

### Exercise 9.3: 저장 함수

ROI 저장 함수를 만드세요.

```python
def save_roi_config(x1, y1, x2, y2, filename="roi_config.json"):
    """ROI 좌표를 JSON 파일로 저장"""
    config = {
        "roi": {
            "x1": ______,
            "y1": ______,
            "x2": ______,
            "y2": ______
        },
        "width": ______,
        "height": ______
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(config, f, ______=4)

    print(f"설정이 {filename}에 저장되었습니다.")


# 테스트
save_roi_config(100, 200, 300, 400)
```

### Exercise 9.4: 로드 함수

ROI 로드 함수를 만드세요.

```python
def load_roi_config(filename="roi_config.json"):
    """JSON 파일에서 ROI 좌표를 불러옴

    Returns:
        dict: ROI 좌표 딕셔너리, 실패시 None
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            config = json.______(f)
        return config["______"]
    except ______:
        print(f"설정 파일을 찾을 수 없습니다: {filename}")
        return None
    except ______:
        print(f"JSON 형식 오류: {filename}")
        return None


# 테스트
roi = load_roi_config()
if roi:
    print(f"불러온 ROI: {roi}")
else:
    print("ROI를 불러오지 못했습니다.")
```

### Exercise 9.5: 통합 테스트

저장과 로드를 함께 테스트하세요.

```python
# 1. 새 좌표 저장
print("=== 저장 테스트 ===")
save_roi_config(500, 350, 600, 420)

# 2. 불러오기
print("\n=== 로드 테스트 ===")
roi = load_roi_config()

if roi:
    print(f"x1={roi['x1']}, y1={roi['y1']}")
    print(f"x2={roi['x2']}, y2={roi['y2']}")

# 3. 없는 파일 테스트
print("\n=== 에러 테스트 ===")
roi = load_roi_config("없는파일.json")
```

---

## 예상 결과

### Exercise 9.1 실행 결과

**콘솔:**
```
설정 저장 완료!
roi_config.json 파일을 열어보세요.
```

**roi_config.json 내용:**
```json
{
    "roi": {
        "x1": 450,
        "y1": 320,
        "x2": 550,
        "y2": 370
    },
    "width": 100,
    "height": 50
}
```

### Exercise 9.5 실행 결과

```
=== 저장 테스트 ===
설정이 roi_config.json에 저장되었습니다.

=== 로드 테스트 ===
x1=500, y1=350
x2=600, y2=420

=== 에러 테스트 ===
설정 파일을 찾을 수 없습니다: 없는파일.json
```

---

## 핵심 정리

### JSON 쓰기

```python
import json

with open("file.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)
```

### JSON 읽기

```python
with open("file.json", "r", encoding="utf-8") as f:
    data = json.load(f)
```

### 에러 처리 패턴

```python
try:
    # 파일 읽기
except FileNotFoundError:
    # 파일 없음
except json.JSONDecodeError:
    # 형식 오류
```

### 우리 프로젝트의 설정 파일

```json
{
    "roi": {
        "x1": 값,
        "y1": 값,
        "x2": 값,
        "y2": 값
    },
    "width": 값,
    "height": 값
}
```

---

## 체크포인트

- [ ] JSON 형식을 이해한다
- [ ] json.dump()로 파일을 쓸 수 있다
- [ ] json.load()로 파일을 읽을 수 있다
- [ ] 에러 처리를 구현할 수 있다
- [ ] ROI 좌표 저장/로드 함수를 만들 수 있다

---

## 다음 챕터 미리보기

**챕터 10: 캘리브레이션 도구**에서는 지금까지 배운 것을 조합해서 ROI 캘리브레이션 도구를 만듭니다. OpenCV의 마우스 이벤트를 사용해서 사용자가 드래그로 영역을 선택하면 자동으로 설정 파일에 저장됩니다.

[다음 챕터로 이동 →](../10-캘리브레이션/chapter-10-calibration-tool.md)
