# Chrome Dino Game Automation 프로젝트 프롬프트 히스토리

이 문서는 Chrome Dino Game Automation 프로젝트를 개발하는 과정에서 사용된 프롬프트들을 기록합니다.

## 날짜: 2026-01-09

### 1. 초기 프로젝트 요청

```
chrome webbrowser 의 chrome://dino 에서 플레이 할 수 있는 게임을 자동화 할 수 있는 파이썬 프로그램을 작성 하고싶다.
ROI 를 설정하는 프로그램을 먼저 제작하자.
calibrate 하는 파일을 작성하여 마우스로 드래그 한 뒤, 좌표를 입력 할 수 있도록 설정하자.
```

**결과:**
- `calibrate.py`: ROI 캘리브레이션 도구 생성
- `requirements.txt`: 필요한 Python 패키지 목록
- `README.md`: 프로젝트 문서

**사용된 기술:**
- OpenCV (cv2): 화면 캡처 및 이미지 처리
- PyAutoGUI: 화면 캡처
- Pillow (PIL): 이미지 처리
- NumPy: 배열 처리

---

### 2. 게임 자동화 메인 프로그램 요청

```
ROI 영역이 원래 하얀색인데, 첨부한 사진처럼 어두운 색상(검정 계열)이 감지되면 keyboard 의 space 키를 누르며, "점프!" 를 출력하자.
그 때 마다 ROI 영역의 상태를 확인(디버깅)하기 위해 ROI 영역을 이미지로 캡쳐하여 저장하자.
이러한 자동화 프로그램을 main.py 파일로 작성하자.
```

**결과:**
- `main.py`: 게임 자동화 메인 프로그램 생성
- 어두운 색상 감지 알고리즘 구현
- 디버그 이미지 자동 저장 기능 (`debug_captures/` 폴더)

**주요 기능:**
- 50ms 간격으로 ROI 영역 모니터링
- 그레이스케일 변환 후 밝기 분석
- 어두운 픽셀 비율이 10% 이상일 때 장애물로 판단
- 자동 스페이스바 입력
- 타임스탬프가 포함된 디버그 이미지 저장

---

### 3. Git 설정 요청

```
.gitignore 파일을 만들어줘
```

**결과:**
- `.gitignore`: Git 저장소 제외 파일 설정
- Python, 가상환경, IDE, 디버그 이미지, ROI 설정 파일 제외

---

### 4. GitHub Publish 준비 요청

```
github에 publish 하기 위한 절차를 준비해줘
```

**결과:**
- `LICENSE`: MIT 라이센스 파일 추가
- `README.md`: GitHub 표준에 맞게 개선 (이모지, 섹션 추가)
- `PUBLISH_GUIDE.md`: GitHub publish 단계별 가이드

**개선된 README 내용:**
- 프로젝트 개요 및 주요 기능 섹션
- 이모지를 활용한 가독성 향상
- 기여 가이드라인
- 라이센스 정보

---

## 프로젝트 구조

```
hg/
├── .gitignore              # Git 제외 파일 설정
├── LICENSE                 # MIT 라이센스
├── README.md               # 프로젝트 문서
├── PUBLISH_GUIDE.md        # GitHub publish 가이드
├── requirements.txt        # Python 패키지 의존성
├── calibrate.py            # ROI 캘리브레이션 도구
├── main.py                 # 게임 자동화 메인 프로그램
├── roi_config.json         # ROI 설정 파일 (사용자 생성)
└── debug_captures/         # 디버그 이미지 저장 폴더 (자동 생성)
```

---

## 기술 스택

- **언어**: Python 3.7+
- **컴퓨터 비전**: OpenCV (cv2)
- **화면 캡처**: PyAutoGUI, Pillow (PIL)
- **데이터 처리**: NumPy
- **설정 저장**: JSON
- **버전 관리**: Git
- **호스팅**: GitHub

---

## 개발 과정 요약

1. **ROI 캘리브레이션 도구 개발**: 사용자가 마우스로 게임 영역을 선택할 수 있는 도구
2. **자동화 알고리즘 구현**: 컴퓨터 비전을 활용한 장애물 감지 및 자동 점프
3. **디버그 기능 추가**: 점프 시마다 ROI 영역을 이미지로 저장
4. **프로젝트 문서화**: README, 라이센스, publish 가이드 작성
5. **GitHub 배포**: Git 설정 및 원격 저장소에 push

---

## 향후 개선 가능 사항

- 새(bird) 장애물 감지를 위한 높이별 ROI 설정
- 게임 속도 증가에 따른 동적 반응 시간 조정
- 머신러닝을 활용한 장애물 패턴 학습
- 점수 인식 및 기록 기능
- GUI 인터페이스 추가
- 다양한 화면 해상도 자동 대응

---

## 참고 링크

- GitHub 저장소: https://github.com/quirinal36/dino_automation
- Chrome Dino Game: chrome://dino
