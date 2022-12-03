'''
Description: 
Author: Huang Wen
Date: 2022-12-01 15:22:49
LastEditTime: 2022-12-01 20:18:38
LastEditors: Huang Wen
'''

import cv2
import numpy as np
import mediapipe as mp
from hands_type import *
class Hands:
    def __init__(self):
        mpHands = mp.solutions.hands
        self.hands = mpHands.Hands()
        self.cnt_left = 0 # 屏幕上所有手指（左手）
        self.cnt_right = 0 # 屏幕上所有手指（右手）
        self.mul_hands = [] # 存储屏幕上的手掌数据 
        self.pointStyle = mp.solutions.drawing_styles.DrawingSpec(color=(0,0,255), thickness=2)
        self.left_lineStyle = mp.solutions.drawing_styles.DrawingSpec(color=(255,0,0), thickness=2)
        self.right_lineStyle = mp.solutions.drawing_styles.DrawingSpec(color=(0,255,0), thickness=2)
        # 为了方便后续使用关键点，保存为成员变量
        self.left_landmarks = None
        self.right_landmarks = None
        # 为了方便使用图像img，保存为成员变量
        self.img = None
        # 每根手指顶端的坐标
        self.figureTopNum = [4,8,12,16,20]
        
  
        
        
        
    def handleImage(self, img):
        self.img = img
        # 手部关键点识别
        self.handsDetect()
        # 绘制关键点
        self.drawHands()
        
        # 有点才绘制
        if (LEFT_HAND_TYPE in self.mul_hands) and self.left_landmarks:
            # # 绘制关键点的序号
            # self.drawKeyPointNum(self.left_landmarks.landmark)
            pass
           
       
        if (RIGHT_HAND_TYPE in self.mul_hands) and self.right_landmarks:
            # self.drawKeyPointNum(self.right_landmarks.landmark)
            pass
   


    # 识别手部关键点
    def handsDetect(self):
        hands = self.hands
        # 识别图像中的手部关键点
        img_rgb = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        result = hands.process(img_rgb)
        if not result:
            return
        if not result.multi_hand_landmarks:
            return
        
        
        for i in result.multi_handedness:
            label = str(i.classification).split('\n')[2].split('"')[1]
            if len(result.multi_handedness)==2:
                self.mul_hands.clear()
                self.mul_hands = [LEFT_HAND_TYPE,RIGHT_HAND_TYPE]
                if label==LEFT_HAND_TYPE:
                    self.left_landmarks = result.multi_hand_landmarks[0]
                elif label==RIGHT_HAND_TYPE:
                    self.right_landmarks = result.multi_hand_landmarks[1]
            elif len(result.multi_handedness)==1:
                if label==LEFT_HAND_TYPE:
                    self.mul_hands.clear()
                    self.mul_hands = [LEFT_HAND_TYPE]
                    self.left_landmarks = result.multi_hand_landmarks[0]
                    self.cnt_right = 0 # 将另一只手的数据清零
                elif label==RIGHT_HAND_TYPE:
                    self.mul_hands.clear()
                    self.mul_hands = [RIGHT_HAND_TYPE]
                    self.right_landmarks = result.multi_hand_landmarks[0]
                    self.cnt_left = 0 # 将另一只手的数据清零

    # 绘制手部关键点
    def drawHands(self):
        conn = mp.solutions.hands_connections
        # 绘制关键点的连线
            # 参数1：将关键点绘制在图像上img
            # 参数2：需要绘制 识别出来的所有关键点
            # 参数3：绘制哪些关键点
            # 参数4：关键点的样式
            # 参数5：连线的样式
        if LEFT_HAND_TYPE in self.mul_hands:
            mp.solutions.drawing_utils.draw_landmarks(self.img, 
                                                    self.left_landmarks, 
                                                    conn.HAND_CONNECTIONS, 
                                                    self.pointStyle, 
                                                    self.left_lineStyle
                                                    )
        if RIGHT_HAND_TYPE in self.mul_hands:
            mp.solutions.drawing_utils.draw_landmarks(self.img, 
                                                    self.right_landmarks, 
                                                    conn.HAND_CONNECTIONS, 
                                                    self.pointStyle, 
                                                    self.right_lineStyle
                                                    )