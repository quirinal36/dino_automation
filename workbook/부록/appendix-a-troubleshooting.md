# 부록 A: 문제 해결 가이드

이 문서는 Dino Game Bot을 사용하면서 발생할 수 있는 문제와 해결 방법을 정리합니다.

---

## 설치 관련 문제

### 문제: pip install 실패

**증상:**
```
ERROR: Could not find a version that satisfies the requirement opencv-python
```

**해결:**
1. Python 버전 확인 (3.7 이상 필요)
   ```bash
   python --version
   ```

2. pip 업그레이드
   ```bash
   python -m pip install --upgrade pip
   ```

3. 다시 설치
   ```bash
   pip install -r requirements.txt
   ```

### 문제: import cv2 에러

**증상:**
```python
ModuleNotFoundError: No module named 'cv2'
```

**해결:**
```bash
pip uninstall opencv-python
pip install opencv-python
```

### 문제: 가상 환경이 활성화되지 않음

**증상:**
- 터미널에 `(venv)`가 표시되지 않음
- 설치한 패키지를 찾을 수 없음

**해결:**

Windows:
```bash
venv\Scripts\activate
```

Mac/Linux:
```bash
source venv/bin/activate
```

---

## 캘리브레이션 문제

### 문제: 화면이 표시되지 않음

**증상:**
- `cv2.imshow()` 후 창이 나타나지 않음

**해결:**
1. `cv2.waitKey(1)` 또는 `cv2.waitKey(0)` 호출 확인
2. 코드 순서 확인:
   ```python
   cv2.namedWindow("이름")
   cv2.imshow("이름", image)
   cv2.waitKey(0)  # 이 줄이 있어야 창이 유지됨
   ```

### 문제: 마우스 드래그가 안됨

**증상:**
- 클릭은 되지만 드래그 중 사각형이 안 보임

**해결:**
- `EVENT_MOUSEMOVE` 이벤트 처리 확인
- `drawing` 플래그 상태 확인
- 원본 이미지 복사 확인:
  ```python
  display = original.copy()  # copy() 필수!
  cv2.rectangle(display, ...)
  ```

### 문제: 저장했는데 파일이 없음

**증상:**
- 's'를 눌렀지만 `roi_config.json`이 생성되지 않음

**해결:**
1. 영역 선택을 먼저 했는지 확인
2. 파일 경로 권한 확인
3. 콘솔 에러 메시지 확인

---

## 게임 자동화 문제

### 문제: "설정 파일을 찾을 수 없습니다"

**증상:**
```
오류: roi_config.json를 찾을 수 없습니다!
```

**해결:**
1. `calibrate.py`를 먼저 실행
2. 영역 선택 후 's' 키로 저장
3. 파일이 같은 폴더에 있는지 확인

### 문제: 점프가 안됨

**증상:**
- 봇이 실행되지만 점프를 하지 않음

**해결:**

1. **ROI 위치 확인**
   - 디버그 이미지 확인 (`debug_captures/` 폴더)
   - ROI가 장애물 출현 영역에 있는지 확인

2. **임계값 조정**
   ```python
   # 감지가 안되면 ratio_threshold를 낮춤
   is_obstacle_detected(gray, ratio_threshold=0.03)
   ```

3. **게임 창 포커스**
   - 게임 창을 클릭해서 활성화
   - 다른 창이 위에 있으면 키 입력이 안 감

### 문제: 너무 자주 점프함 (오탐지)

**증상:**
- 장애물이 없는데도 계속 점프

**해결:**

1. **ROI 위치 확인**
   - ROI가 너무 넓거나 잘못된 위치일 수 있음
   - 점수 표시, 구름 등이 포함되지 않도록

2. **임계값 조정**
   ```python
   # 오탐지가 많으면 ratio_threshold를 높임
   is_obstacle_detected(gray, ratio_threshold=0.10)

   # 또는 brightness_threshold를 낮춤
   is_obstacle_detected(gray, brightness_threshold=100)
   ```

### 문제: 점프 타이밍이 안 맞음

**증상:**
- 너무 일찍 또는 너무 늦게 점프

**해결:**

1. **ROI 위치 조정**
   - 너무 일찍: ROI를 공룡 쪽으로 이동 (x1 감소)
   - 너무 늦음: ROI를 멀리 이동 (x1 증가)

2. **체크 간격 조정**
   ```python
   # 반응이 느리면 간격 줄임
   bot.run(check_interval=0.03)
   ```

### 문제: 점프 후 연속 점프됨

**증상:**
- 한 번 점프해야 하는데 여러 번 점프

**해결:**
- 쿨다운 시간 확인
  ```python
  bot.run(jump_cooldown=0.4)  # 쿨다운 늘림
  ```

---

## 게임 관련 문제

### 문제: 야간 모드에서 감지 실패

**증상:**
- 야간 모드 (검은 배경)로 바뀌면 감지가 안됨

**해결:**
현재 버전은 주간 모드 전용입니다. 야간 모드 지원은 추후 개선이 필요합니다.

임시 해결책:
- 야간 모드 전에 게임 재시작
- 또는 감지 로직을 반대로 수정 (밝은 픽셀 감지)

### 문제: 새(pterodactyl)를 피하지 못함

**증상:**
- 선인장은 피하지만 날아오는 새에 충돌

**해결:**
현재 버전은 점프만 지원합니다. 숙이기(duck) 기능은 추후 추가 필요합니다.

아이디어:
- 높은 위치에 두 번째 ROI 추가
- 새가 감지되면 아래 화살표 입력

---

## 성능 문제

### 문제: 캡처가 느림

**증상:**
- 체크 간격보다 캡처 시간이 더 오래 걸림

**해결:**
1. 다른 프로그램 종료
2. 화면 해상도 낮추기
3. ROI 크기 줄이기

### 문제: CPU 사용량이 높음

**증상:**
- 봇 실행 중 CPU 100% 사용

**해결:**
- 체크 간격 늘리기
  ```python
  bot.run(check_interval=0.1)  # 100ms
  ```

---

## 기타 문제

### 문제: PyAutoGUI 권한 에러 (Mac)

**증상:**
```
pyautogui.FailSafeException 또는 권한 에러
```

**해결:**
- 시스템 환경설정 → 보안 및 개인 정보 → 개인 정보 보호 → 손쉬운 사용
- 터미널 또는 Python 추가

### 문제: 프로그램이 멈추지 않음

**증상:**
- Ctrl+C가 작동하지 않음

**해결:**
- **Fail-Safe 사용**: 마우스를 화면 구석으로 빠르게 이동
- 터미널에서 `Ctrl+C`를 여러 번 누름
- 최후의 수단: 터미널 창 닫기

---

## 도움 요청

위 해결책으로도 문제가 해결되지 않으면:

1. 에러 메시지 전체를 복사
2. 실행 환경 정보 확인:
   ```bash
   python --version
   pip list
   ```
3. 디버그 이미지 (`debug_captures/`) 확인
4. 수업 담당자에게 문의

---

[← 목차로 돌아가기](../README.md)
