"""
Chrome Dino Game Automation - Main Program
ROI 영역에서 어두운 색상(장애물)을 감지하면 스페이스바를 눌러 점프
"""

import cv2
import numpy as np
import pyautogui
from PIL import ImageGrab
import json
import os
import time
import shutil
from datetime import datetime
import math


class SpeedController:
    """게임 속도에 따른 동적 파라미터 관리"""

    def __init__(self):
        self.start_time = None
        self.MAX_SPEED_FACTOR = 2.17
        self.TIME_TO_MAX = 180.0  # 3분

        # 기본 파라미터
        self.BASE_CHECK_INTERVAL = 0.05
        self.BASE_JUMP_COOLDOWN = 0.30
        self.BASE_DARK_RATIO = 0.05
        self.MIN_DARK_RATIO = 0.03

    def start(self):
        """게임 시작 시 호출"""
        self.start_time = time.time()

    def get_speed_factor(self):
        """현재 속도 배율 계산 (1.0 ~ 2.17)"""
        if self.start_time is None:
            return 1.0
        elapsed = time.time() - self.start_time
        if elapsed >= self.TIME_TO_MAX:
            return self.MAX_SPEED_FACTOR
        progress = elapsed / self.TIME_TO_MAX
        return 1.0 + (self.MAX_SPEED_FACTOR - 1.0) * (math.log(1 + 2 * progress) / math.log(3))

    def get_check_interval(self):
        """동적 체크 간격 반환"""
        return self.BASE_CHECK_INTERVAL / self.get_speed_factor()

    def get_jump_cooldown(self):
        """동적 점프 쿨다운 반환"""
        return self.BASE_JUMP_COOLDOWN / self.get_speed_factor()

    def get_dark_ratio_threshold(self):
        """동적 어두운 픽셀 비율 임계값 반환"""
        factor = self.get_speed_factor()
        return self.BASE_DARK_RATIO - (self.BASE_DARK_RATIO - self.MIN_DARK_RATIO) * (factor - 1.0) / (self.MAX_SPEED_FACTOR - 1.0)


class DinoGameBot:
    def __init__(self, config_file='roi_config.json'):
        """초기화"""
        self.config_file = config_file
        self.roi = None
        self.running = False
        self.jump_count = 0
        self.debug_folder = 'debug_captures'
        self.speed_controller = SpeedController()
        self.dark_mode = False  # 다크 모드 여부
        self.play_start_time = None  # 플레이 시작 시간
        self.report_file = 'report.json'

        # 기존 디버그 폴더가 있으면 타임스탬프로 이동
        if os.path.exists(self.debug_folder):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_folder_name = f"{self.debug_folder}_{timestamp}"
            shutil.move(self.debug_folder, new_folder_name)
            print(f"기존 디버그 폴더 이동: {self.debug_folder} → {new_folder_name}")

        # 새 디버그 폴더 생성
        os.makedirs(self.debug_folder)
        print(f"디버그 폴더 생성: {self.debug_folder}")

        # ROI 설정 로드
        self.load_roi_config()
        
    def load_roi_config(self):
        """ROI 설정 파일 로드"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            self.roi = config['roi']
            print(f"ROI 설정 로드 완료:")
            print(f"  좌표: ({self.roi['x1']}, {self.roi['y1']}) ~ ({self.roi['x2']}, {self.roi['y2']})")
            print(f"  크기: {config['width']} x {config['height']}")
            return True
            
        except FileNotFoundError:
            print(f"오류: '{self.config_file}' 파일을 찾을 수 없습니다.")
            print("먼저 calibrate.py를 실행하여 ROI를 설정해주세요.")
            return False
        except Exception as e:
            print(f"ROI 설정 로드 중 오류 발생: {e}")
            return False
    
    def capture_roi(self):
        """ROI 영역만 캡처"""
        # 전체 화면 캡처
        screenshot = ImageGrab.grab()
        screenshot_np = np.array(screenshot)
        
        # ROI 영역 추출
        roi_img = screenshot_np[
            self.roi['y1']:self.roi['y2'],
            self.roi['x1']:self.roi['x2']
        ]
        
        return roi_img
    
    def check_dark_mode(self, dark_ratio):
        """
        다크 모드 전환 감지
        어두운 픽셀 비율이 95% 이상이면 다크 모드로 전환
        밝은 픽셀 비율이 95% 이상이면 라이트 모드로 전환
        """
        if not self.dark_mode and dark_ratio >= 0.95:
            self.dark_mode = True
            print("\n[모드 전환] 다크 모드 감지 → 밝은 픽셀 감지로 전환\n")
        elif self.dark_mode and dark_ratio <= 0.05:
            self.dark_mode = False
            print("\n[모드 전환] 라이트 모드 감지 → 어두운 픽셀 감지로 전환\n")

    def is_obstacle_detected(self, roi_img, threshold=128, ratio_threshold=0.05):
        """
        ROI 영역에서 장애물 감지 (라이트/다크 모드 자동 대응)

        Args:
            roi_img: ROI 영역 이미지 (RGB)
            threshold: 밝기 임계값 (0-255)
            ratio_threshold: 픽셀 비율 임계값 (동적 조정 가능)

        Returns:
            tuple: (장애물 감지 여부, 평균 밝기, 감지 비율)
        """
        # RGB를 그레이스케일로 변환
        gray = cv2.cvtColor(roi_img, cv2.COLOR_RGB2GRAY)

        # 평균 밝기 계산
        avg_brightness = np.mean(gray)

        # 어두운 픽셀 비율 계산
        dark_pixels = np.sum(gray < threshold)
        total_pixels = gray.size
        dark_ratio = dark_pixels / total_pixels

        # 다크 모드 전환 체크
        self.check_dark_mode(dark_ratio)

        if self.dark_mode:
            # 다크 모드: 밝은 픽셀(장애물)을 감지
            light_ratio = 1.0 - dark_ratio
            is_obstacle = light_ratio > ratio_threshold
            return is_obstacle, avg_brightness, light_ratio
        else:
            # 라이트 모드: 어두운 픽셀(장애물)을 감지
            is_obstacle = dark_ratio > ratio_threshold
            return is_obstacle, avg_brightness, dark_ratio
    
    def save_debug_image(self, roi_img, jump_count):
        """디버그용 ROI 이미지 저장"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
        filename = f"{self.debug_folder}/jump_{jump_count:04d}_{timestamp}.png"
        
        # RGB를 BGR로 변환 (OpenCV 저장용)
        roi_bgr = cv2.cvtColor(roi_img, cv2.COLOR_RGB2BGR)
        cv2.imwrite(filename, roi_bgr)
        
        return filename
    
    def jump(self):
        """스페이스바를 눌러 점프"""
        pyautogui.press('space')
        self.jump_count += 1
        print(f"점프! (총 {self.jump_count}번)")

    def save_report(self, elapsed_time):
        """플레이 결과를 report.json에 저장"""
        # 디버그 이미지 갯수 계산
        debug_image_count = len([f for f in os.listdir(self.debug_folder) if f.endswith('.png')])

        # 플레이 결과 데이터
        play_result = {
            "play_start_time": self.play_start_time.strftime("%Y-%m-%d %H:%M:%S") if self.play_start_time else None,
            "total_play_time_seconds": round(elapsed_time, 1),
            "jump_count": self.jump_count,
            "debug_image_count": debug_image_count,
            "roi": self.roi
        }

        # 기존 report.json 로드 또는 새로 생성
        if os.path.exists(self.report_file):
            with open(self.report_file, 'r', encoding='utf-8') as f:
                report_data = json.load(f)
        else:
            report_data = {"play_history": []}

        # 플레이 결과 추가
        report_data["play_history"].append(play_result)

        # report.json 저장
        with open(self.report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)

        print(f"플레이 결과 저장: {self.report_file}")
    
    def run(self):
        """
        게임 자동화 실행 (동적 속도 조정 적용)
        """
        if self.roi is None:
            print("ROI 설정이 로드되지 않았습니다.")
            return

        print("\n" + "=" * 60)
        print("Chrome Dino Game Automation 시작")
        print("=" * 60)
        print(f"동적 속도 조정: 활성화")
        print(f"  - 초기 체크 간격: {self.speed_controller.BASE_CHECK_INTERVAL*1000:.0f}ms")
        print(f"  - 초기 쿨다운: {self.speed_controller.BASE_JUMP_COOLDOWN*1000:.0f}ms")
        print(f"  - 최대 속도 배율: {self.speed_controller.MAX_SPEED_FACTOR:.2f}x (약 {self.speed_controller.TIME_TO_MAX:.0f}초 후)")
        print(f"디버그 이미지 저장 위치: {self.debug_folder}/")
        print("\n게임을 시작하세요!")
        print("종료하려면 Ctrl+C를 누르세요.")
        print("=" * 60 + "\n")

        self.running = True
        self.play_start_time = datetime.now()
        self.speed_controller.start()
        last_status_time = time.time()

        try:
            while self.running:
                # 동적 파라미터 가져오기
                check_interval = self.speed_controller.get_check_interval()
                ratio_threshold = self.speed_controller.get_dark_ratio_threshold()
                jump_cooldown = self.speed_controller.get_jump_cooldown()

                # 10초마다 속도 상태 출력
                if time.time() - last_status_time >= 10:
                    factor = self.speed_controller.get_speed_factor()
                    elapsed = time.time() - self.speed_controller.start_time
                    mode_str = "다크" if self.dark_mode else "라이트"
                    print(f"[속도] {elapsed:.0f}초 | {factor:.2f}x | 모드: {mode_str} | 체크: {check_interval*1000:.0f}ms | 쿨다운: {jump_cooldown*1000:.0f}ms | 임계값: {ratio_threshold*100:.1f}%")
                    last_status_time = time.time()

                # ROI 영역 캡처
                roi_img = self.capture_roi()

                # 장애물 감지 (라이트/다크 모드 자동 대응)
                is_obstacle, avg_brightness, detect_ratio = self.is_obstacle_detected(
                    roi_img, ratio_threshold=ratio_threshold
                )

                if is_obstacle:
                    # 점프 실행
                    self.jump()

                    # 디버그 이미지 저장
                    saved_file = self.save_debug_image(roi_img, self.jump_count)
                    mode_str = "밝은" if self.dark_mode else "어두운"
                    print(f"  - 평균 밝기: {avg_brightness:.1f}, {mode_str} 픽셀 비율: {detect_ratio*100:.1f}%")
                    print(f"  - 디버그 이미지 저장: {saved_file}")

                    # 동적 쿨다운 적용
                    time.sleep(jump_cooldown)

                # 동적 체크 간격 적용
                time.sleep(check_interval)

        except KeyboardInterrupt:
            elapsed = time.time() - self.speed_controller.start_time if self.speed_controller.start_time else 0
            print("\n\n사용자에 의해 중단되었습니다.")
            print(f"총 플레이 시간: {elapsed:.1f}초")
            print(f"총 점프 횟수: {self.jump_count}번")
            print(f"디버그 이미지: {self.jump_count}개 저장됨")

            # 플레이 결과 저장
            self.save_report(elapsed)

        self.running = False


def main():
    """메인 함수"""
    print("Chrome Dino Game Bot을 시작합니다...\n")
    
    # 봇 인스턴스 생성
    bot = DinoGameBot()
    
    # ROI 설정 확인
    if bot.roi is None:
        print("\n프로그램을 종료합니다.")
        return
    
    print("\n준비 사항:")
    print("1. Chrome 브라우저에서 chrome://dino 페이지를 열어주세요")
    print("2. 게임 화면을 calibrate.py에서 설정한 위치에 배치해주세요")
    print("3. 게임을 시작할 준비를 해주세요 (스페이스바를 눌러 시작)")
    
    input("\n준비가 되면 Enter 키를 눌러주세요...")
    
    # 카운트다운
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    print("시작!\n")
    
    # 봇 실행 (동적 속도 조정 자동 적용)
    bot.run()
    
    print("\n프로그램이 종료되었습니다.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n오류 발생: {e}")
        import traceback
        traceback.print_exc()
