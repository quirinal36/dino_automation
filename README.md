# 🦖 Chrome Dino Game Automation

Chrome 브라우저의 공룡 게임(chrome://dino)을 자동으로 플레이하는 파이썬 프로그램입니다.

## 📋 개요

이 프로젝트는 컴퓨터 비전을 활용하여 Chrome의 숨겨진 공룡 게임을 자동으로 플레이합니다. ROI(Region of Interest) 영역을 설정하고, 해당 영역에서 장애물(어두운 색상)을 감지하면 자동으로 점프하여 게임을 진행합니다.

## ✨ 주요 기능

- 🎯 **ROI 캘리브레이션**: 마우스 드래그로 간편하게 게임 영역 설정
- 🤖 **자동 장애물 감지**: 실시간으로 장애물을 감지하여 자동 점프
- 📸 **디버그 모드**: 점프할 때마다 ROI 영역을 이미지로 저장
- ⚡ **빠른 반응 속도**: 50ms 간격으로 화면을 체크하여 빠르게 반응

## 프로젝트 구조

- `calibrate.py`: ROI(Region of Interest) 설정 도구
- `requirements.txt`: 필요한 Python 패키지 목록
- `roi_config.json`: ROI 좌표 설정 파일 (calibrate.py 실행 후 생성됨)

## 설치 방법

1. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

## 사용 방법

### 1. ROI 캘리브레이션

게임 영역을 설정하기 위해 먼저 캘리브레이션을 실행합니다:

```bash
python calibrate.py
```

**단계별 안내:**
1. Chrome 브라우저에서 `chrome://dino` 페이지를 엽니다
2. 게임 화면이 보이도록 준비합니다
3. 프로그램을 실행하고 Enter 키를 누릅니다
4. 화면이 캡처되면 마우스로 드래그하여 게임 영역을 선택합니다
5. `s` 키를 눌러 ROI를 저장합니다
6. `q` 키를 눌러 종료합니다

**키보드 단축키:**
- `s`: 현재 선택한 ROI를 저장
- `r`: 화면을 다시 캡처
- `q`: 프로그램 종료

### 2. 게임 자동화

ROI 설정 후 게임 자동화 프로그램을 실행합니다:

```bash
python main.py
```

**동작 원리:**
1. `roi_config.json` 파일에서 설정된 ROI 영역을 로드합니다
2. 50ms마다 ROI 영역을 캡처하여 분석합니다
3. ROI 영역이 어두운 색상(검정 계열, 장애물)으로 변하면:
   - 스페이스바를 눌러 점프합니다
   - "점프!"를 출력합니다
   - ROI 영역을 이미지로 캡처하여 `debug_captures/` 폴더에 저장합니다
4. Ctrl+C를 눌러 프로그램을 종료할 수 있습니다

**디버그 이미지:**
- 점프할 때마다 ROI 영역이 `debug_captures/jump_XXXX_timestamp.png` 형식으로 저장됩니다
- 이미지를 통해 감지 상태를 확인할 수 있습니다

## 요구사항

- Python 3.7 이상
- Windows OS (현재 버전)
- Chrome 브라우저

## 주의사항

- 게임 화면이 명확하게 보이는 상태에서 ROI를 설정하세요
- ROI는 게임 영역만 포함하도록 정확하게 선택하세요
- 화면 해상도나 브라우저 크기가 변경되면 ROI를 다시 설정해야 합니다

## 🤝 기여

버그 리포트, 기능 제안, Pull Request를 환영합니다!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 라이센스

이 프로젝트는 MIT 라이센스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 👤 작성자

**Albert**

---

⭐ 이 프로젝트가 도움이 되었다면 Star를 눌러주세요!
