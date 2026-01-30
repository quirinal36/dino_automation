# DinoML 프로젝트 분석 리포트

> 작성일: 2026-01-30

---

## 1. 프로젝트 개요

**DinoML**은 Chrome 공룡 게임(chrome://dino)을 머신러닝을 이용해 자동으로 플레이하는 프로젝트입니다. Google의 Teachable Machine을 활용한 이미지 분류와 키보드 자동화를 결합하여 데이터 수집부터 자율 플레이까지 완전한 파이프라인을 구현했습니다.

### 핵심 특징
- 컴퓨터 비전 기반 실시간 게임 상태 인식
- Teachable Machine을 통한 간편한 모델 학습
- 키보드 자동화를 통한 자율 게임 플레이
- GUI 기반 화면 영역 선택

---

## 2. 프로젝트 구조

```
DinoML/
├── auto_play.py          # 자동 플레이 엔진 (350줄)
├── capture_screen.py     # 학습 데이터 수집 도구 (224줄)
├── region_selector.py    # GUI 화면 영역 선택기 (207줄)
├── test_model.py         # 모델 검증 스크립트 (44줄)
├── keras_model.h5        # 학습된 ML 모델 (2.4MB)
├── labels.txt            # 액션 레이블 (4개 클래스)
├── requirements.txt      # Python 의존성
├── PRD.md               # 제품 요구사항 문서
├── README.md            # 프로젝트 문서화
├── .gitignore           # Git 제외 파일
├── dino_game_captures/  # 학습 이미지 저장소 (gitignored)
├── debug_captures/      # 디버그 스크린샷 (gitignored)
└── venv/                # Python 가상환경
```

**총 코드 라인**: 약 825줄 (의존성 제외)

---

## 3. 기술 스택

### 핵심 기술

| 기술 | 버전 | 용도 |
|------|------|------|
| **Python** | 3.8+ | 메인 프로그래밍 언어 |
| **TensorFlow** | ≥2.13.0 | ML 프레임워크 백엔드 |
| **tf-keras** | ≥2.16.0 | 모델 로딩 및 추론 |
| **OpenCV** | ≥4.8.0 | 이미지 전처리 |
| **MSS** | ≥9.0.1 | 고속 화면 캡처 |
| **Pillow** | ≥10.0.0 | 이미지 조작 |
| **keyboard** | ≥0.13.5 | 키보드 입력 자동화 |
| **tkinter** | Built-in | GUI 영역 선택 |
| **h5py** | ≥3.8.0 | HDF5 모델 파일 처리 |
| **numpy** | ≥1.24.0 | 수치 연산 |

### 외부 플랫폼
- **Teachable Machine** (Google): 웹 기반 이미지 분류 모델 학습 플랫폼

---

## 4. 핵심 워크플로우

### 전체 파이프라인

```
┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│   Phase 1: 데이터    │    │   Phase 2: 모델     │    │   Phase 3: 자동     │
│       수집          │ → │       학습          │ → │       플레이        │
│  capture_screen.py  │    │  Teachable Machine  │    │    auto_play.py     │
└─────────────────────┘    └─────────────────────┘    └─────────────────────┘
         │                          │                          │
         ▼                          ▼                          ▼
   게임 화면 캡처              4개 클래스 분류            실시간 예측
   30 FPS 연속 촬영           모델 학습 및 내보내기        10 FPS 추론
   학습 데이터 저장           keras_model.h5 생성         키보드 제어
```

### Phase 1: 데이터 수집 (`capture_screen.py`)
1. Chrome에서 `chrome://dino` 접속
2. GUI 오버레이로 게임 영역 선택
3. 테스트 캡처로 선택 영역 확인
4. 수동 플레이 중 30 FPS로 연속 캡처
5. `dino_game_captures/`에 순차적 파일명으로 저장
6. Ctrl+C로 캡처 종료 및 통계 출력

### Phase 2: 모델 학습 (Teachable Machine)
1. 캡처된 이미지를 teachablemachine.withgoogle.com에 업로드
2. 4개 액션 클래스로 분류:
   - `big_jump`: 높은 장애물 (익룡)
   - `small_jump`: 낮은 장애물 (선인장)
   - `walk`: 안전 구간
   - `down`: 숙이기 필요
3. 이미지 분류 모델 학습
4. Keras 모델로 내보내기 (`keras_model.h5` + `labels.txt`)

### Phase 3: 자율 플레이 (`auto_play.py`)
1. 학습된 Keras 모델 로드 (폴백 메커니즘 포함)
2. GUI로 게임 영역 선택
3. 5초 카운트다운 후 게임 시작
4. 실시간 예측 루프 (기본 10 FPS):
   - 화면 영역 캡처
   - 224×224 픽셀로 리사이즈
   - 픽셀값 정규화 (0-1 범위)
   - 모델 추론 실행
   - 예측 신뢰도 기반 액션 실행
5. 타이밍 제어와 함께 액션 실행
6. 통계 추적 및 쿨다운으로 중복 방지
7. 선택적 디버그 모드로 액션 스크린샷 캡처

---

## 5. 주요 컴포넌트

### 컴포넌트 다이어그램

```
┌─────────────────────┐
│  region_selector.py │
│  (RegionSelector)   │
└──────────┬──────────┘
           │ region dict 제공
           ├──────────────┬─────────────┐
           ▼              ▼             ▼
┌────────────────┐ ┌────────────┐ ┌─────────────┐
│capture_screen  │ │ auto_play  │ │test_model   │
│(ScreenCapture) │ │(DinoAuto   │ │(validation) │
│                │ │  Player)   │ │             │
└────────────────┘ └─────┬──────┘ └──────┬──────┘
         │               │                │
         ▼               ▼                ▼
    ┌────────────────────────────────────────┐
    │        keras_model.h5 + labels.txt     │
    │      (Teachable Machine Model)         │
    └────────────────────────────────────────┘
```

### 클래스 상세

#### `RegionSelector` (region_selector.py)
- **목적**: 화면 영역 선택을 위한 인터랙티브 GUI
- **주요 메서드**:
  - `select_region()`: 메인 진입점, region dict 반환
  - 이벤트 핸들러: `on_mouse_down`, `on_mouse_move`, `on_mouse_up`
- **기능**:
  - 전체화면 투명 오버레이 (30% 알파)
  - 드래그 중 실시간 크기 표시
  - Enter로 확인, ESC로 취소/재시도
  - 최소 10×10 픽셀 검증

#### `ScreenCapture` (capture_screen.py)
- **목적**: 학습 데이터 수집 엔진
- **주요 메서드**:
  - `capture_once(region, filename)`: 단일 스크린샷
  - `capture_continuous(region, duration, fps)`: 스트리밍 캡처
  - `set_custom_region(left, top, width, height)`: 수동 영역 설정
- **기능**:
  - 설정 가능한 FPS (기본 30)
  - 실시간 진행 표시
  - 자동 디렉토리 생성
  - 타임스탬프 기반 파일명
  - 성능 메트릭 (실제 FPS, 평균 캡처 시간)

#### `DinoAutoPlayer` (auto_play.py)
- **목적**: 자율 게임 제어 및 예측
- **주요 메서드**:
  - `__init__()`: 폴백 메커니즘이 있는 모델 로딩
  - `preprocess_image(image)`: 이미지 정규화 파이프라인
  - `predict_action(region)`: 추론 실행
  - `execute_action(action, confidence)`: 키보드 자동화
  - `play(region, fps)`: 메인 게임 루프
  - `_capture_debug_frame(action)`: 디버그 스크린샷 캡처
- **기능**:
  - 설정 가능한 점프 지속시간 (big vs small)
  - 신뢰도 임계값 필터링 (기본 0.6)
  - 액션 쿨다운 (100ms) 스팸 방지
  - 모든 예측에 대한 통계 추적
  - 액션 트리거 캡처가 있는 디버그 모드
  - TensorFlow 호환성을 위한 폴백 모델 로딩

### 액션 분류 체계

| 액션 | 대상 | 키 입력 | 지속시간 |
|------|------|---------|----------|
| `big_jump` | 높은 장애물 (익룡) | Spacebar | 150ms |
| `small_jump` | 낮은 장애물 (선인장) | Spacebar | 50ms |
| `walk` | 안전 구간 | 없음 | - |
| `down` | 숙이기 필요 | Down Arrow | 300ms |

---

## 6. 특수 기능

### 디버그 모드
- `DinoAutoPlayer`에서 `debug_mode=True`로 활성화
- 액션 실행 시 자동 스크린샷 캡처
- 파일명에 액션 타입과 마이크로초 타임스탬프 포함
- `debug_captures/` 디렉토리에 저장
- 실패한 게임플레이의 사후 분석에 유용

### 듀얼 점프 시스템
- **Big jump** (150ms): 높이 나는 익룡용
- **Small jump** (50ms): 낮은 선인장/장애물용
- 생성자에서 지속시간 설정 가능
- 세밀한 장애물 회피 가능

### 모델 로딩 복원력
- 기본 방법: 표준 `keras.models.load_model()`
- 폴백 방법: TF 2.16+ 호환성을 위한 `safe_mode=False`
- 레거시 Teachable Machine 모델 형식 처리
- 정보성 메시지가 있는 우아한 에러 처리

### 액션 쿨다운 시스템
- 동일 액션 간 최소 100ms 간격
- 게임 물리에 영향을 줄 수 있는 입력 스팸 방지
- `last_action`과 `last_action_time` 추적
- 신뢰도 임계값 (0.6)으로 추가 필터링

### 실시간 성능 모니터링
- 캡처 중 FPS 추적
- 실제 vs 목표 FPS 보고
- 프레임당 평균 캡처 시간
- Ctrl+C 종료 시 통계 대시보드

---

## 7. 설정 및 의존성

### requirements.txt 분석
모든 의존성은 `>=` 제약조건으로 최소 버전 지정:
- **화면 캡처**: `mss` (빠름, 크로스 플랫폼)
- **이미지 처리**: `Pillow`, `opencv-python`, `numpy`
- **ML 프레임워크**: `tensorflow`, `tf-keras`, `h5py`
- **자동화**: `keyboard` (Windows에서 관리자 권한 필요)

### labels.txt 구조
```
0 big_jump
1 small_jump
2 walk
3 down
```
형식: `{index} {action_name}` (Teachable Machine 표준)

### .gitignore 설정
제외 항목:
- 가상환경 (`venv/`, `env/`)
- ML 모델 (`*.h5`, `*.pkl`, `*.pth`)
- 학습 데이터 (`dino_game_captures/`, `debug_captures/`)
- IDE 파일 (`.vscode/`, `.idea/`)
- Python 아티팩트 (`__pycache__/`, `*.pyc`)

---

## 8. 코드 품질 평가

### 강점

| 항목 | 설명 |
|------|------|
| **모듈화 설계** | 캡처/학습/플레이 단계의 명확한 분리 |
| **사용자 친화적** | GUI 영역 선택, 카운트다운, 진행 표시 |
| **설정 가능** | FPS, 점프 지속시간, 신뢰도 임계값 파라미터화 |
| **에러 처리** | 폴백 메커니즘이 있는 try-except 블록 |
| **문서화** | 스크린샷이 포함된 포괄적인 한국어 README |

### 개선 여지

| 항목 | 현재 상태 | 권장 사항 |
|------|----------|----------|
| **테스트** | 유닛 테스트 없음 | pytest 기반 테스트 추가 |
| **설정** | 하드코딩된 값 | config.yaml 도입 |
| **모델 관리** | 버전 관리 없음 | MLflow 등 도입 |
| **타입 힌트** | 미사용 | type hints 추가 |
| **로깅** | print문 사용 | logging 모듈 적용 |

### 코드 품질 관찰

| 항목 | 평가 |
|------|------|
| 타입 힌트 | 최소 (docstring으로 문서화) |
| 주석 | 대부분 한국어, 일부 영어 |
| 네이밍 | 명확하고 서술적 (영어 변수명) |
| 에러 메시지 | 이모지가 포함된 이중 언어 출력 |
| PEP 8 준수 | 일반적으로 Python 스타일 규칙 따름 |

---

## 9. Git 히스토리

```
10e0f69 - readme update (최신)
48b057e - 화면 캡쳐
6d02245 - Add debug screen capture feature for game events
ff6c961 - init (초기 커밋)
```

### 개발 타임라인
1. 초기 프로젝트 스캐폴딩
2. 디버그 캡처 기능 구현
3. 화면 캡처 기능
4. 문서 업데이트

**개발 단계**: 최근 문서 개선이 있는 기능적 프로토타입

---

## 10. 시스템 요구사항

| 항목 | 요구사항 |
|------|----------|
| **OS** | Windows (기본), macOS/Linux (가능) |
| **Python** | 3.8 이상 |
| **RAM** | ~2GB (TensorFlow용) |
| **디스크** | ~500MB (TensorFlow + 의존성) |
| **권한** | 관리자 권한 (Windows 키보드 제어) |
| **브라우저** | Google Chrome (chrome://dino) |
| **디스플레이** | 최소 800×600 해상도 |

---

## 11. 설치 및 실행

```bash
# 1. 저장소 클론
git clone <repository-url>
cd DinoML

# 2. 가상환경 생성
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# 3. 의존성 설치
pip install -r requirements.txt

# 4. 학습 데이터 수집
python capture_screen.py

# 5. Teachable Machine에서 모델 학습
# (수동 웹 기반 단계)

# 6. 자동화 실행
python auto_play.py
```

---

## 12. 향후 개선 제안

### 단기 개선사항
- [ ] argparse/click으로 CLI 인자 파싱 추가
- [ ] config.yaml 설정 파일 생성
- [ ] logging 프레임워크 구현
- [ ] 모델 성능 메트릭 대시보드 추가
- [ ] 크로스 플랫폼 키보드 추상화

### 중기 개선사항
- [ ] 강화학습 (DQN/PPO) 구현
- [ ] 데이터 증강 파이프라인 추가
- [ ] 자동화된 모델 재학습 워크플로우 생성
- [ ] 모니터링용 웹 인터페이스 구축
- [ ] 멀티 게임 지원 추가

### 장기 개선사항
- [ ] 컨테이너화된 서비스로 배포 (Docker)
- [ ] 클라우드 기반 모델 학습 통합
- [ ] 실수에서 배우는 실시간 학습
- [ ] 멀티플레이어 점수 경쟁 플랫폼
- [ ] 모바일/태블릿 버전

---

## 13. 사용 사례 및 대상 사용자

### 주요 사용 사례
1. **교육용**: ML 기반 게임 자동화 시연
2. **실험용**: 컴퓨터 비전 + 게임 자동화 개념 테스트
3. **포트폴리오**: Python, ML, CV 기술 쇼케이스
4. **연구용**: 강화학습 대안 탐색

### 대상 사용자
- ML 통합을 배우는 Python 개발자
- 컴퓨터 비전 학생
- 게임 자동화 애호가
- 브라우저 자동화에 관심 있는 메이커
- 한국어 사용 개발자 (주요 문서 언어)

---

## 14. 결론

### 프로젝트 평가 요약

| 항목 | 평가 |
|------|------|
| **프로젝트 상태** | 교육/실험용으로 사용 가능 |
| **코드 성숙도** | Beta (테스트/최적화 여지 있음) |
| **문서화 품질** | 우수 (포괄적인 한국어 README) |
| **아키텍처** | 깔끔한 모듈화 설계 |
| **확장성** | 중간 (리팩토링으로 개선 가능) |

### 핵심 가치

**DinoML**은 컴퓨터 비전, 자동화, 게임 AI의 실용적 통합을 보여주는 교육적이고 잘 구조화된 ML 프로젝트입니다. 전이 학습과 키보드 자동화를 통해 자율적인 Chrome Dino 게임플레이라는 목표를 성공적으로 달성합니다.

다음 분야의 우수한 참조 구현체로 활용 가능:
- Teachable Machine 통합
- 화면 캡처 및 자동화
- 실시간 ML 추론
- Python 게임 자동화
- End-to-end ML 파이프라인 설계

---

*이 리포트는 DinoML 프로젝트의 종합적인 분석을 제공합니다.*
