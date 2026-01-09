# GitHub Publish 가이드

이 문서는 프로젝트를 GitHub에 publish하는 방법을 안내합니다.

## 1단계: Git 커밋 준비

현재 변경사항을 확인하고 커밋합니다:

```bash
# 현재 상태 확인
git status

# 모든 파일 추가 (이미 실행했다면 생략)
git add .

# 커밋 생성
git commit -m "Initial commit: Chrome Dino Game Automation"
```

## 2단계: GitHub 저장소 생성

1. GitHub 웹사이트(https://github.com)에 로그인합니다
2. 우측 상단의 `+` 버튼을 클릭하고 `New repository`를 선택합니다
3. 저장소 정보를 입력합니다:
   - **Repository name**: `chrome-dino-automation` (또는 원하는 이름)
   - **Description**: `Chrome Dino Game Automation using Python and Computer Vision`
   - **Public/Private**: 원하는 공개 설정 선택
   - ⚠️ **중요**: `Initialize this repository with a README` 체크 해제 (이미 로컬에 파일이 있으므로)
4. `Create repository` 버튼을 클릭합니다

## 3단계: 로컬 저장소와 GitHub 연결

GitHub에서 생성한 저장소의 URL을 복사한 후, 다음 명령을 실행합니다:

```bash
# GitHub 저장소를 원격 저장소로 추가
git remote add origin https://github.com/YOUR_USERNAME/chrome-dino-automation.git

# 기본 브랜치 이름을 main으로 설정
git branch -M main

# GitHub에 푸시
git push -u origin main
```

> **참고**: `YOUR_USERNAME`을 실제 GitHub 사용자명으로 변경하세요.

## 4단계: SSH를 사용하는 경우 (선택사항)

HTTPS 대신 SSH를 사용하려면:

```bash
# SSH URL로 원격 저장소 추가
git remote add origin git@github.com:YOUR_USERNAME/chrome-dino-automation.git

# 푸시
git push -u origin main
```

## 5단계: 확인

1. GitHub 저장소 페이지를 새로고침합니다
2. 모든 파일이 정상적으로 업로드되었는지 확인합니다
3. README.md가 저장소 메인 페이지에 표시되는지 확인합니다

## 추가 작업 (선택사항)

### Topics 추가
GitHub 저장소 페이지에서 `About` 섹션의 톱니바퀴 아이콘을 클릭하고 다음 topics를 추가하세요:
- `python`
- `automation`
- `computer-vision`
- `opencv`
- `chrome-dino`
- `game-bot`

### 스크린샷 추가
게임 실행 화면이나 ROI 설정 화면의 스크린샷을 찍어서 README에 추가하면 더 좋습니다:

1. 스크린샷을 `screenshots/` 폴더에 저장
2. README.md에 이미지 추가:
   ```markdown
   ![ROI Calibration](screenshots/calibration.png)
   ![Game Running](screenshots/game_running.png)
   ```
3. Git에 추가하고 푸시:
   ```bash
   git add screenshots/
   git commit -m "Add screenshots"
   git push
   ```

## 문제 해결

### "remote origin already exists" 오류
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/chrome-dino-automation.git
```

### 푸시 권한 오류
- GitHub 로그인 정보를 확인하세요
- Personal Access Token을 사용하는 경우, 올바른 권한이 설정되어 있는지 확인하세요

## 완료!

축하합니다! 프로젝트가 GitHub에 성공적으로 publish되었습니다. 🎉
