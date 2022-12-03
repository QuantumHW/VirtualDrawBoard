'''
Description: 常用工具
Author: Huang Wen
Date: 2022-12-01 14:51:09
LastEditTime: 2022-12-01 20:18:18
LastEditors: Huang Wen
'''

from win32 import win32gui, win32print
from win32.lib import win32con
from win32.win32api import GetSystemMetrics
import numpy as np
import math

# 计算角度
def getAngle(sta_point, mid_point, end_point):
    ma_x = sta_point[0] - mid_point[0]
    ma_y = sta_point[1] - mid_point[1]
    mb_x = end_point[0] - mid_point[0]
    mb_y = end_point[1] - mid_point[1]
    ab_x = sta_point[0] - end_point[0]
    ab_y = sta_point[1] - end_point[1]
    ab_val2 = ab_x * ab_x + ab_y * ab_y
    ma_val2 = ma_x * ma_x + ma_y * ma_y
    mb_val2 = mb_x * mb_x + mb_y * mb_y
    cos_M = (ma_val2 + mb_val2 - ab_val2) / (2 * np.sqrt(ma_val2) * np.sqrt(mb_val2))
    angleAMB = np.arccos(cos_M) / np.pi * 180
    return angleAMB

# 计算两点间的距离
def getDistance(p1,p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])



# 转换坐标
def indexCVKeyPoint(img, index, landmark):
    mark = landmark[index]
    imgH = img.shape[0]
    imgW = img.shape[1]
    x = int(mark.x * imgW)
    y = int(mark.y * imgH)
    return (x,y)

def get_screen_size():
    """获取缩放后的显示器分辨率"""
    w = GetSystemMetrics (0)
    h = GetSystemMetrics (1)
    return (w, h)

def get_real_resolution():
    """获取真实的分辨率"""
    hDC = win32gui.GetDC(0)
    # 横向分辨率
    w = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
    # 纵向分辨率
    h = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
    return w, h



if __name__=='__main__':
    print(get_screen_size())