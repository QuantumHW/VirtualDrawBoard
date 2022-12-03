'''
Description: 
Author: Huang Wen
Date: 2022-12-01 15:13:57
LastEditTime: 2022-12-02 17:42:32
LastEditors: Huang Wen
'''

import cv2
import numpy as np
from hands import Hands
from global_var import globalVar
from util import indexCVKeyPoint
from util import getDistance

class DrawBoard:
    def __init__(self):
        # 存储当前视频帧
        self.img = None
        # 初始化各类检测器
        self.hands = Hands()
        
        # 一堆有用的flag
        self.flag_start = False # 是否开始绘制（直线、圆、矩形）
        self.flag_drawing = False # 是否正在绘制（直线、圆、矩形）
        self.flag_end = True # 是否结束（直线、圆、矩形）
        

        
        # 存放各种轨迹的历史坐标点
        self.free_record = [] # 自由绘制
        self.line_record = [] # 直线
        self.circle_record = [] # 圆
        self.rectangle_record = [] # 矩形
        self.mosaic_record = [] # 马赛克
        
        
        # 一堆临时使用的temp数据
        self.draw_temp = None
        self.line_temp = None

    
    
    def handleImage(self, img):
        self.img = img
        self.hands.handleImage(img)
        if not self.hands.right_landmarks:
            return
        if globalVar.DRAW_EQUIPMENT==0:self.rubber() # 橡皮擦
        elif globalVar.DRAW_EQUIPMENT==1:self.drawFree() # 自由绘制
        elif globalVar.DRAW_EQUIPMENT==2:self.drawLine() # 绘制直线
        elif globalVar.DRAW_EQUIPMENT==3:self.drawCircle() # 绘制圆
        elif globalVar.DRAW_EQUIPMENT==4:self.drawRectangle() # 绘制矩形
        elif globalVar.DRAW_EQUIPMENT==5:self.drawMosaic() # 绘制马赛克
            
        # 绘制历史轨迹
        self.drawHistoy()
        # 显示状态信息
        self.showInfor()

    
    # 0橡皮擦
    def rubber(self):
        topMark1 = indexCVKeyPoint(self.img, 8, self.hands.right_landmarks.landmark)
        topMark2 = indexCVKeyPoint(self.img, 12, self.hands.right_landmarks.landmark)
        dis = getDistance(topMark1, topMark2)
        rubber_size = 8
        if dis<30:
            # 遍历已有的点 达到清除的效果
            for i in self.free_record:
                if getDistance(topMark1, i[0])<rubber_size:
                    self.free_record.remove(i)
            
            for i in self.line_record:
                if getDistance(topMark1, i[0])<rubber_size or getDistance(topMark1, i[1])<rubber_size:
                    self.line_record.remove(i)
                    
            for i in self.circle_record:
                if getDistance(topMark1, i[0])<rubber_size:
                    self.circle_record.remove(i)
                    
            for i in self.rectangle_record:
                if getDistance(topMark1, i[0])<rubber_size or getDistance(topMark1, i[1])<rubber_size:
                    self.rectangle_record.remove(i)
                    
            for i in self.mosaic_record:
                if getDistance(topMark1, i)<rubber_size:
                    self.mosaic_record.remove(i)
        
        
    # 1自由绘制
    def drawFree(self):
        topMark1 = indexCVKeyPoint(self.img, 8, self.hands.right_landmarks.landmark)
        topMark2 = indexCVKeyPoint(self.img, 12, self.hands.right_landmarks.landmark)
        dis = getDistance(topMark1, topMark2)
        # 方法一
        # if dis<30:
        #     list_temp = []
        #     list_temp.append((topMark1[0],topMark1[1])) 
        #     list_temp.append(globalVar.COLOR) # 存放颜色
        #     self.free_record.append(list_temp) # 存入历史轨迹中
        #     cv2.circle(self.img, (topMark1[0],topMark1[1]), 3, color=globalVar.COLOR, thickness=-1)
        #     cv2.circle(self.img, (topMark1[0],topMark1[1]), 4, color=globalVar.COLOR, thickness=2)
        if dis<80:
            if self.line_temp==None:
                self.line_temp=(topMark1[0],topMark1[1])
            else:
                cv2.line(self.img,self.line_temp,(topMark1[0],topMark1[1]), globalVar.COLOR, thickness=6)
                self.line_record.append((self.line_temp,(topMark1[0],topMark1[1]),globalVar.COLOR))
                self.line_temp=None
    
    
    # 2绘制直线
    def drawLine(self):
        topMark1 = indexCVKeyPoint(self.img, 8, self.hands.right_landmarks.landmark)
        topMark2 = indexCVKeyPoint(self.img, 12, self.hands.right_landmarks.landmark)
        dis = getDistance(topMark1, topMark2)
        if dis<30 and self.flag_start==False and self.flag_end: # 下第一笔
            self.flag_end=False
            self.flag_start=True
            self.draw_temp = (topMark1[0],topMark1[1])
       
        elif dis>50 and self.flag_start: # 绘制轨迹
            cv2.line(self.img, self.draw_temp, (topMark1[0],topMark1[1]), globalVar.COLOR, thickness=6)
            self.flag_drawing = True
            
        elif dis<30  and self.flag_start and self.flag_drawing: # 最后一笔
            self.flag_start=False
            self.flag_drawing = False
            list_temp = []
            list_temp.append(self.draw_temp)
            list_temp.append((topMark1[0],topMark1[1]))
            list_temp.append(globalVar.COLOR)
            self.line_record.append(list_temp) # 存入历史轨迹中
            cv2.line(self.img, self.draw_temp, (topMark1[0],topMark1[1]), globalVar.COLOR, thickness=6)
            
        if self.flag_end==False and self.flag_drawing==False and dis>50:
            # 画完最后一笔后，要把手指拿开 才算真正的结束
            self.flag_end=True
    
    
    # 3圆
    def drawCircle(self):
        topMark1 = indexCVKeyPoint(self.img, 8, self.hands.right_landmarks.landmark)
        topMark2 = indexCVKeyPoint(self.img, 12, self.hands.right_landmarks.landmark)
        dis = getDistance(topMark1, topMark2)
        if dis<30 and self.flag_start==False and self.flag_end: # 下第一笔
            self.flag_end=False
            self.flag_start=True
            self.draw_temp = (topMark1[0],topMark1[1])
       
        elif dis>50 and self.flag_start: # 绘制轨迹
            radius = getDistance(self.draw_temp, topMark1)
            cv2.circle(self.img, self.draw_temp, int(radius), globalVar.COLOR, thickness=3)
            self.flag_drawing = True
            
        elif dis<30  and self.flag_start and self.flag_drawing: # 最后一笔
            self.flag_start=False
            self.flag_drawing = False
            list_temp = []
            list_temp.append(self.draw_temp)
            radius = getDistance(self.draw_temp, topMark1)
            list_temp.append(radius)
            list_temp.append(globalVar.COLOR)
            self.circle_record.append(list_temp) # 存入历史轨迹中
            cv2.circle(self.img, self.draw_temp, int(radius), globalVar.COLOR, thickness=3)
            
        if self.flag_end==False and self.flag_drawing==False and dis>50:
            # 画完最后一笔后，要把手指拿开 才算真正的结束
            self.flag_end=True
    
    # 4矩形
    def drawRectangle(self):
        topMark1 = indexCVKeyPoint(self.img, 8, self.hands.right_landmarks.landmark)
        topMark2 = indexCVKeyPoint(self.img, 12, self.hands.right_landmarks.landmark)
        dis = getDistance(topMark1, topMark2)
        if dis<30 and self.flag_start==False and self.flag_end: # 下第一笔
            self.flag_end=False
            self.flag_start=True
            self.draw_temp = (topMark1[0],topMark1[1])
       
        elif dis>50 and self.flag_start: # 绘制轨迹
            cv2.rectangle(self.img, self.draw_temp, (topMark1[0],topMark1[1]), color=globalVar.COLOR, thickness=3)
            self.flag_drawing = True
            
        elif dis<30  and self.flag_start and self.flag_drawing: # 最后一笔
            self.flag_start=False
            self.flag_drawing = False
            list_temp = []
            list_temp.append(self.draw_temp)
            list_temp.append((topMark1[0],topMark1[1]))
            list_temp.append(globalVar.COLOR)
            self.rectangle_record.append(list_temp) # 存入历史轨迹中
            cv2.rectangle(self.img, self.draw_temp, (topMark1[0],topMark1[1]), color=globalVar.COLOR, thickness=3)
            
        if self.flag_end==False and self.flag_drawing==False and dis>50:
            # 画完最后一笔后，要把手指拿开 才算真正的结束
            self.flag_end=True
        
        
        
    # 5绘制马赛克
    def drawMosaic(self):
        topMark1 = indexCVKeyPoint(self.img, 8,self.hands.right_landmarks.landmark)
        topMark2 = indexCVKeyPoint(self.img, 12,self.hands.right_landmarks.landmark)
        distance = getDistance(topMark1, topMark2)
        if distance<30:
            self.mosaic_record.append(topMark1)
            self.mosaic(topMark1[1],topMark1[0],size=10)     
        
    
    # 在指定坐标生成马赛克
    def mosaic(self, x,y,size=10):
        m=int(x/size*size)
        n=int(y/size*size)
        for i in range(size):
            for j in range(size):
                # 防止越界
                if (m+i<self.img.shape[0]) and (n+j<self.img.shape[1]):
                    self.img[m+i][n+j]=self.img[m][n]
    
    
    # 绘制历史轨迹
    def drawHistoy(self):
        # 1自由绘制
        for i in self.free_record:
            # cv2.circle(self.img, i[0], 3, color=i[1], thickness=-1)
            # cv2.circle(self.img, i[0], 4, color=i[1], thickness=2)
            cv2.line(self.img, i[0], i[1], color=i[2], thickness=6)
            
        # 2直线
        for i in self.line_record: 
            cv2.line(self.img, i[0], i[1], color=i[2], thickness=6)
            
        # 3圆
        for i in self.circle_record:
            cv2.circle(self.img, i[0], int(i[1]), color=i[2], thickness=3)
            
        # 4矩形
        for i in self.rectangle_record:
            cv2.rectangle(self.img, i[0], i[1], color=i[2], thickness=3)
            
        # 5马赛克
        for i in self.mosaic_record:
            self.mosaic(i[1],i[0],size=10)
        
    # 展示状态信息
    def showInfor(self):
        pass