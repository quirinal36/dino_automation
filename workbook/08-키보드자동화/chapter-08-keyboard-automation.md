# 챕터 8: 키보드 자동화

> "봇의 손가락을 만들자"

---

## 학습 목표

- PyAutoGUI 라이브러리를 이해한다
- 키보드 입력을 자동화한다
- 안전 기능(Fail-Safe)을 이해한다
- 점프 함수를 구현한다

---

## PyAutoGUI란?

### 소개

**PyAutoGUI**는 키보드와 마우스를 자동으로 제어하는 라이브러리입니다.

- 키보드 입력 시뮬레이션
- 마우스 이동 및 클릭
- 화면 캡처 (우리는 Pillow 사용)

### 작동 원리

```
PyAutoGUI → 운영체제 → 키보드 이벤트 생성 → 애플리케이션
```

프로그램이 직접 키보드를 "누르는" 것처럼 운영체제에 신호를 보냅니다.

---

## 기본 사용법

### 임포트

```python
import pyautogui
```

### 키 누르기

```python
# 단일 키 누르기
pyautogui.press('space')  # 스페이스바
pyautogui.press('up')     # 위 화살표
pyautogui.press('down')   # 아래 화살표
pyautogui.press('enter')  # 엔터
```

### 주요 키 이름

| 키 | PyAutoGUI 이름 |
|----|----------------|
| 스페이스바 | 'space' |
| 엔터 | 'enter' |
| 위 화살표 | 'up' |
| 아래 화살표 | 'down' |
| 왼쪽 화살표 | 'left' |
| 오른쪽 화살표 | 'right' |
| ESC | 'escape' |
| Tab | 'tab' |

---

## Fail-Safe 기능

### 왜 필요한가?

자동화 프로그램이 제어를 벗어나면?

```
무한 루프로 키보드를 계속 누름
→ 다른 작업 불가
→ 컴퓨터 사용 불능!
```

### Fail-Safe 작동 방식

**마우스를 화면 구석으로 이동하면 프로그램이 즉시 중지됩니다.**

```
┌─────────────────────────────────┐
│ ●                           ●   │  ← 네 구석 중 하나로
│                                 │     마우스를 빠르게 이동
│                                 │
│                                 │
│ ●                           ●   │
└─────────────────────────────────┘
```

### 설정

```python
# Fail-Safe 활성화 (기본값: True)
pyautogui.FAILSAFE = True

# 비활성화 (권장하지 않음!)
# pyautogui.FAILSAFE = False
```

**항상 True로 유지하세요!** 비상 탈출 수단입니다.

---

## 점프 함수 구현

### 기본 구조

```python
import pyautogui

def jump():
    """공룡을 점프시킵니다."""
    pyautogui.______(______)
    print("점프!")
```

### 카운터 추가

```python
jump_count = 0

def jump():
    """공룡을 점프시킵니다."""
    global jump_count
    pyautogui.press('space')
    jump_count += 1
    print(f"점프! (총 {jump_count}번)")
```

---

## 타이밍 제어

### 문제 상황

감지 루프가 너무 빠르면:

```
장애물 감지! → 점프
10ms 후 → 아직 장애물 있음 → 또 점프!
10ms 후 → 아직 있음 → 또 점프!
...
```

### 해결책: 쿨다운

점프 후 일정 시간 동안 다시 점프하지 않습니다.

```python
import time

last_jump_time = 0
JUMP_COOLDOWN = 0.3  # 300ms

def jump_with_cooldown():
    global last_jump_time

    current_time = time.time()

    # 쿨다운 체크
    if current_time - last_jump_time < JUMP_COOLDOWN:
        return  # 아직 쿨다운 중

    pyautogui.press('space')
    last_jump_time = current_time
    print("점프!")
```

또는 더 간단하게:

```python
def jump():
    pyautogui.press('space')
    print("점프!")
    time.sleep(0.3)  # 점프 후 300ms 대기
```

---

## 생각해보기

### 질문 1: 스페이스바 vs 위 화살표

Dino 게임에서 점프는 스페이스바와 위 화살표 모두 가능합니다.
어떤 것을 사용하는 것이 좋을까요?

### 질문 2: 쿨다운 시간

쿨다운이 너무 길면? (예: 1초)
쿨다운이 너무 짧으면? (예: 0.05초)

적절한 쿨다운 시간은 얼마일까요?

### 질문 3: 숙이기 (Duck)

새(pterodactyl)를 피하려면 숙여야 합니다.
숙이는 기능은 어떻게 추가할 수 있을까요?

---

## 실습 과제

### Exercise 8.1: 기본 키 입력

PyAutoGUI로 키를 눌러보세요.

**파일명**: `keyboard_test.py`

```python
import pyautogui
import time

# Fail-Safe 확인
print(f"Fail-Safe 활성화: {pyautogui.FAILSAFE}")

# 카운트다운
print("3초 후에 스페이스바를 누릅니다...")
print("메모장이나 텍스트 입력 창을 클릭해두세요!")

for i in range(3, 0, -1):
    print(f"{i}...")
    time.sleep(1)

# 스페이스바 누르기
pyautogui.______(______)
print("스페이스바를 눌렀습니다!")
```

### Exercise 8.2: 연속 입력

여러 번 키를 누르세요.

```python
print("5번 스페이스바를 누릅니다...")
time.sleep(3)

for i in range(5):
    pyautogui.______('space')
    print(f"{i + 1}번째 입력")
    time.sleep(0.5)  # 0.5초 간격

print("완료!")
```

### Exercise 8.3: 점프 함수

재사용 가능한 점프 함수를 만드세요.

```python
jump_count = 0

def jump():
    """공룡을 점프시킵니다."""
    global ______

    pyautogui.______('space')
    ______ += 1
    print(f"점프! (총 {______}번)")


# 테스트
print("Dino 게임을 준비하세요! 3초 후 시작...")
time.sleep(3)

for _ in range(3):
    jump()
    time.sleep(1)
```

### Exercise 8.4: 쿨다운 기능

쿨다운이 있는 점프 함수를 만드세요.

```python
import time

last_jump = 0
COOLDOWN = 0.3  # 300ms

def jump_with_cooldown():
    """쿨다운이 있는 점프"""
    global last_jump

    now = time.______()

    # 쿨다운 체크
    if now - last_jump < ______:
        print("쿨다운 중...")
        return False

    pyautogui.press('space')
    last_jump = ______
    print("점프!")
    return True


# 테스트: 빠르게 5번 호출
print("빠르게 5번 호출 테스트")
time.sleep(3)

for i in range(5):
    result = jump_with_cooldown()
    print(f"시도 {i + 1}: {'성공' if result else '스킵'}")
    time.sleep(0.1)  # 100ms 간격으로 호출
```

### Exercise 8.5: Dino 게임 테스트

실제 게임에서 테스트하세요.

```python
print("=" * 40)
print("Dino 게임 점프 테스트")
print("=" * 40)
print("\n준비:")
print("1. Chrome에서 chrome://dino 열기")
print("2. 게임 창 클릭해서 포커스 맞추기")
print("3. 게임 시작하지 않고 대기")
print("\n5초 후 자동으로 게임 시작 + 3번 점프합니다!")
print("(종료: 마우스를 화면 구석으로)")

time.sleep(5)

# 게임 시작 (첫 스페이스바)
print("\n게임 시작!")
pyautogui.press('space')
time.sleep(0.5)

# 3번 점프
for i in range(3):
    time.sleep(1.5)  # 1.5초 간격
    print(f"점프 {i + 1}!")
    pyautogui.press('space')

print("\n테스트 완료!")
```

---

## 예상 결과

### Exercise 8.4 실행 결과

```
빠르게 5번 호출 테스트
시도 1: 성공
시도 2: 스킵
시도 3: 스킵
시도 4: 성공
시도 5: 스킵
```

100ms 간격이지만 300ms 쿨다운이므로 3번 중 2번만 성공

---

## 핵심 정리

### 기본 사용법

```python
import pyautogui

# Fail-Safe (항상 True 유지!)
pyautogui.FAILSAFE = True

# 키 누르기
pyautogui.press('space')
```

### 점프 함수 패턴

```python
def jump():
    pyautogui.press('space')
    time.sleep(COOLDOWN)  # 쿨다운
```

### 쿨다운의 중요성

```
쿨다운 없음: 같은 장애물에 여러 번 반응
쿨다운 있음: 한 번 점프 후 안정화
```

### 안전 수칙

1. **FAILSAFE = True** 유지
2. 테스트 시 **짧은 시간**으로 시작
3. **마우스 구석 이동**으로 비상 정지 연습

---

## 체크포인트

- [ ] pyautogui.press()로 키를 누를 수 있다
- [ ] Fail-Safe 기능을 이해하고 활용한다
- [ ] 점프 함수를 만들 수 있다
- [ ] 쿨다운의 필요성을 이해한다
- [ ] 실제 Dino 게임에서 점프를 테스트했다

---

## 다음 챕터 미리보기

**챕터 9: 설정 저장**에서는 JSON 파일로 ROI 좌표를 저장하고 불러오는 방법을 배웁니다. 이것으로 매번 좌표를 입력하지 않고 저장된 설정을 사용할 수 있습니다.

[다음 챕터로 이동 →](../09-설정저장/chapter-09-json-config.md)
