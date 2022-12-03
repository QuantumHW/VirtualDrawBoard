'''
Description: 检测全身姿态
Author: Huang Wen
Date: 2022-12-01 14:53:07
LastEditTime: 2022-12-02 14:43:51
LastEditors: Huang Wen
'''

import mediapipe as mp
import cv2

class Pose:
    def __init__(self):
        self.mpPose = mp.solutions.pose
        # 创建pose用于识别肢体的关键点
        self.pose = self.mpPose.Pose()
        self.pointStyle = mp.solutions.drawing_styles.DrawingSpec(color=(0,0,255),thickness=2)
        self.lineStyle = mp.solutions.drawing_styles.DrawingSpec(color=(0,0,255),thickness=2)
        # 关键点的坐标
        self.landmark = None
        self.img = None

    
            
    def handleImage(self, img):
        self.img = img
        self.drawPoint()
 
    
    
    
    
    # 绘制关键点
    def drawPoint(self):
        img = self.img
        pose = self.pose
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = pose.process(img_rgb)
        pose_landmarks = result.pose_landmarks
        if not pose_landmarks: # 如果没值直接停止执行
            return
        self.landmark = pose_landmarks.landmark # 保存坐标点
        # 绘制关键点的连线
        mp.solutions.drawing_utils.draw_landmarks(img,
                                                  pose_landmarks,
                                                  self.mpPose.POSE_CONNECTIONS,
                                                  self.pointStyle,
                                                  self.lineStyle
                                                )
        
        for index, mark in enumerate(pose_landmarks.landmark):
            x,y = self.indexCvPoint(index)
            cv2.putText(img, str(index), (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color=(0,255,0), thickness=1)
        
        
    def indexCvPoint(self, index):
        imgH, imgW = self.img.shape[0:2]
        mark = self.landmark[index]
        x = int(mark.x*imgW)
        y = int(mark.y*imgH)
        return x,y