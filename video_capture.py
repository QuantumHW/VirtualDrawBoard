'''
Description: 
Author: Huang Wen
Date: 2022-12-01 14:49:56
LastEditTime: 2022-12-02 12:27:59
LastEditors: Huang Wen
'''

import cv2
from pose import Pose
from global_var import globalVar
from draw_board import DrawBoard
from util import get_screen_size

class VideoCapture:
    def __init__(self):
        # # 初始化姿态检测类
        # self.pose = Pose()
        self.draw_board = DrawBoard()
        self.screen_size = get_screen_size()
        # 创建图像的检测对象
        self.handVideoCapture()
       
    
    
    def handVideoCapture(self):
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            retval, image = cap.read()
            if not retval:
                print("can't read image")
            image = cv2.flip(image, 1) # 水平翻转图像
            # self.pose.handleImage(image) # 处理图像_姿态
            self.draw_board.handleImage(image) # 处理图像_画板
            
            # cv2.namedWindow("img", 0)
            # cv2.resizeWindow("img", self.screen_size[0], self.screen_size[1])
            cv2.imshow("img",image)
            
            key = cv2.waitKey(1)
            if key == ord("a"):globalVar.DRAW_EQUIPMENT = 0
            elif key == ord("s"):globalVar.DRAW_EQUIPMENT = 1
            elif key == ord("d"):globalVar.DRAW_EQUIPMENT = 2
            elif key == ord("f"):globalVar.DRAW_EQUIPMENT = 3
            elif key == ord("g"):globalVar.DRAW_EQUIPMENT = 4
            elif key == ord("h"):globalVar.DRAW_EQUIPMENT = 5
            
            elif key == ord("z"):globalVar.COLOR = (0,0,255)
            elif key == ord("x"):globalVar.COLOR = (0,255,0)
            elif key == ord("c"):globalVar.COLOR = (255,0,0)
            elif key == ord("q"):
                break
        # 释放资源
        cap.release()
        cv2.destroyAllWindows()
        

if __name__ =='__main__':
    VideoCapture()