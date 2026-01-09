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
from datetime import datetime

class DinoGameBot:
    def __init__(self, config_file='roi_config.json'):
        """초기화"""
        self.config_file = config_file
        self.roi = None
        self.running = False
        self.jump_count = 0
        self.debug_folder = 'debug_captures'
        
        # 디버그 폴더 생성
        if not os.path.exists(self.debug_folder):
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
    
    def is_dark_detected(self, roi_img, threshold=128):
        """
        ROI 영역에서 어두운 색상(검정 계열) 감지
        
        Args:
            roi_img: ROI 영역 이미지 (RGB)
            threshold: 밝기 임계값 (0-255, 이 값보다 낮으면 어두운 것으로 판단)
        
        Returns:
            bool: 어두운 색상이 감지되면 True
        """
        # RGB를 그레이스케일로 변환
        gray = cv2.cvtColor(roi_img, cv2.COLOR_RGB2GRAY)
        
        # 평균 밝기 계산
        avg_brightness = np.mean(gray)
        
        # 어두운 픽셀 비율 계산
        dark_pixels = np.sum(gray < threshold)
        total_pixels = gray.size
        dark_ratio = dark_pixels / total_pixels
        
        # 어두운 픽셀이 일정 비율 이상이면 장애물로 판단
        # (전체 픽셀의 5% 이상이 어두우면 장애물로 간주)
        is_dark = dark_ratio > 0.05
        
        return is_dark, avg_brightness, dark_ratio
    
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
    
    def run(self, check_interval=0.05):
        """
        게임 자동화 실행
        
        Args:
            check_interval: ROI 체크 간격 (초)
        """
        if self.roi is None:
            print("ROI 설정이 로드되지 않았습니다.")
            return
        
        print("\n" + "=" * 60)
        print("Chrome Dino Game Automation 시작")
        print("=" * 60)
        print(f"ROI 체크 간격: {check_interval}초")
        print(f"디버그 이미지 저장 위치: {self.debug_folder}/")
        print("\n게임을 시작하세요!")
        print("종료하려면 Ctrl+C를 누르세요.")
        print("=" * 60 + "\n")
        
        self.running = True
        
        try:
            while self.running:
                # ROI 영역 캡처
                roi_img = self.capture_roi()
                
                # 어두운 색상 감지
                is_dark, avg_brightness, dark_ratio = self.is_dark_detected(roi_img)
                
                if is_dark:
                    # 점프 실행
                    self.jump()
                    
                    # 디버그 이미지 저장
                    saved_file = self.save_debug_image(roi_img, self.jump_count)
                    print(f"  - 평균 밝기: {avg_brightness:.1f}, 어두운 픽셀 비율: {dark_ratio*100:.1f}%")
                    print(f"  - 디버그 이미지 저장: {saved_file}")
                    
                    # 점프 후 잠시 대기 (연속 점프 방지)
                    time.sleep(0.3)
                
                # 다음 체크까지 대기
                time.sleep(check_interval)
                
        except KeyboardInterrupt:
            print("\n\n사용자에 의해 중단되었습니다.")
            print(f"총 점프 횟수: {self.jump_count}번")
            print(f"디버그 이미지: {self.jump_count}개 저장됨")
        
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
    
    # 봇 실행
    bot.run(check_interval=0.05)  # 50ms마다 체크
    
    print("\n프로그램이 종료되었습니다.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n오류 발생: {e}")
        import traceback
        traceback.print_exc()
