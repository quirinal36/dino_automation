"""
Chrome Dino Game ROI Calibration Tool
마우스 드래그로 게임 화면의 ROI(Region of Interest)를 설정하는 프로그램
"""

import cv2
import numpy as np
import pyautogui
from PIL import ImageGrab
import json
import os

class ROICalibrator:
    def __init__(self):
        self.roi_coords = None
        self.start_point = None
        self.end_point = None
        self.drawing = False
        self.screenshot = None
        self.display_img = None
        
    def mouse_callback(self, event, x, y, flags, param):
        """마우스 이벤트 콜백 함수"""
        if event == cv2.EVENT_LBUTTONDOWN:
            # 마우스 왼쪽 버튼을 누르면 시작점 설정
            self.drawing = True
            self.start_point = (x, y)
            self.end_point = (x, y)
            
        elif event == cv2.EVENT_MOUSEMOVE:
            # 마우스를 움직이면 끝점 업데이트
            if self.drawing:
                self.end_point = (x, y)
                
        elif event == cv2.EVENT_LBUTTONUP:
            # 마우스 왼쪽 버튼을 떼면 그리기 종료
            self.drawing = False
            self.end_point = (x, y)
            
            # 좌표 정규화 (왼쪽 위, 오른쪽 아래 순서로)
            x1 = min(self.start_point[0], self.end_point[0])
            y1 = min(self.start_point[1], self.end_point[1])
            x2 = max(self.start_point[0], self.end_point[0])
            y2 = max(self.start_point[1], self.end_point[1])
            
            self.roi_coords = (x1, y1, x2, y2)
            print(f"\n선택된 ROI 좌표: ({x1}, {y1}, {x2}, {y2})")
            print(f"ROI 크기: {x2-x1} x {y2-y1}")
    
    def capture_screen(self):
        """현재 화면을 캡처"""
        print("화면을 캡처하는 중...")
        screenshot = ImageGrab.grab()
        self.screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        self.display_img = self.screenshot.copy()
        print(f"화면 캡처 완료: {self.screenshot.shape[1]} x {self.screenshot.shape[0]}")
        
    def draw_rectangle(self):
        """현재 선택 영역을 화면에 표시"""
        if self.start_point and self.end_point:
            self.display_img = self.screenshot.copy()
            cv2.rectangle(
                self.display_img,
                self.start_point,
                self.end_point,
                (0, 255, 0),  # 녹색
                2
            )
            
            # 좌표 텍스트 표시
            if self.roi_coords:
                x1, y1, x2, y2 = self.roi_coords
                text = f"ROI: ({x1},{y1}) to ({x2},{y2})"
                cv2.putText(
                    self.display_img,
                    text,
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2
                )
    
    def save_roi(self, filename='roi_config.json'):
        """ROI 좌표를 JSON 파일로 저장"""
        if self.roi_coords:
            config = {
                'roi': {
                    'x1': self.roi_coords[0],
                    'y1': self.roi_coords[1],
                    'x2': self.roi_coords[2],
                    'y2': self.roi_coords[3]
                },
                'width': self.roi_coords[2] - self.roi_coords[0],
                'height': self.roi_coords[3] - self.roi_coords[1]
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            
            print(f"\nROI 설정이 '{filename}' 파일에 저장되었습니다.")
            return True
        else:
            print("\n저장할 ROI가 선택되지 않았습니다.")
            return False
    
    def run(self):
        """캘리브레이션 프로그램 실행"""
        print("=" * 60)
        print("Chrome Dino Game ROI Calibration Tool")
        print("=" * 60)
        print("\n사용 방법:")
        print("1. Chrome 브라우저에서 chrome://dino 페이지를 열어주세요")
        print("2. 게임 화면이 보이도록 준비해주세요")
        print("3. 아무 키나 눌러 화면을 캡처합니다")
        print("4. 마우스로 드래그하여 게임 영역을 선택하세요")
        print("5. 's' 키를 눌러 ROI를 저장합니다")
        print("6. 'q' 키를 눌러 종료합니다")
        print("7. 'r' 키를 눌러 다시 캡처합니다")
        print("=" * 60)
        
        input("\n준비가 되면 Enter 키를 눌러주세요...")
        
        # 화면 캡처
        self.capture_screen()
        
        # OpenCV 윈도우 생성
        window_name = 'ROI Calibration - 드래그로 영역 선택'
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.setMouseCallback(window_name, self.mouse_callback)
        
        print("\n마우스로 드래그하여 ROI 영역을 선택하세요...")
        print("- 's' 키: ROI 저장")
        print("- 'r' 키: 화면 다시 캡처")
        print("- 'q' 키: 종료")
        
        while True:
            # 사각형 그리기
            if self.drawing or self.roi_coords:
                self.draw_rectangle()
            
            # 화면 표시
            cv2.imshow(window_name, self.display_img)
            
            # 키 입력 대기
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                # 종료
                print("\n프로그램을 종료합니다.")
                break
                
            elif key == ord('s'):
                # ROI 저장
                if self.save_roi():
                    print("저장 완료! 계속 조정하거나 'q'를 눌러 종료하세요.")
                    
            elif key == ord('r'):
                # 화면 다시 캡처
                self.capture_screen()
                self.roi_coords = None
                self.start_point = None
                self.end_point = None
                print("\n화면을 다시 캡처했습니다. ROI를 다시 선택하세요.")
        
        cv2.destroyAllWindows()
        print("\n캘리브레이션이 완료되었습니다!")


if __name__ == "__main__":
    try:
        calibrator = ROICalibrator()
        calibrator.run()
    except KeyboardInterrupt:
        print("\n\n사용자에 의해 중단되었습니다.")
    except Exception as e:
        print(f"\n오류 발생: {e}")
        import traceback
        traceback.print_exc()
