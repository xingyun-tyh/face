import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from face import Ui_MainWindow  # 导入生成的UI类
import cv2 as cv
from datetime import datetime
from PySide6.QtCore import QTimer, QEvent
from PySide6.QtGui import QImage, QPixmap
import os
from PIL import Image
import numpy as np
import sqlite3

# 创建全局变量
app = None
window = None
ui = None
cap = None
attended_ids = set()  # 存储已考勤的人员ID

# 初始化SQLite数据库
def init_database():
    conn = sqlite3.connect('face_attendance.db')
    c = conn.cursor()
    
    # 创建人员信息表
    c.execute('''CREATE TABLE IF NOT EXISTS persons
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  num TEXT UNIQUE NOT NULL,
                  jointime TEXT NOT NULL)''')
    
    conn.commit()
    conn.close()

# 加载人脸检测器
faceCascade = cv.CascadeClassifier("./haarcascade_frontalface_alt2.xml")

def update_current_time():
    """更新当前时间显示"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ui.timeLabel.setText(f"当前时间: {current_time}")

def on_Open_click():
    print("Open按钮被点击了!")
    
    global cap
    if  cap is not None and cap.isOpened():
        # 清空画面
        ui.faceLabel.clear()
        # 关闭摄像头
        cap.release()
        cv.destroyAllWindows()
        ui.openButton.setText("打开摄像头")
    else:
        ui.openButton.setText("关闭摄像头")

        cap = cv.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                return
            
            # 转换为灰度图
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            
            # 检测人脸
            face = faceCascade.detectMultiScale(gray)
            
            if len(face) == 0:
                ui.statusLabel.setText("未检测到人脸")
                return
            
            for x, y, w, h in face:
                cv.rectangle(frame, (x, y), (x + w, y + h), (0, 200, 0), 2)

            cv.waitKey(1) & 0xFF

            # 转换为Qt可显示的格式
            rgb_image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            ui.faceLabel.setPixmap(QPixmap.fromImage(convert_to_Qt_format))
            
            if on_Recog_click or on_Input_click == True:
                break

def on_Save_click():
    print("Save按钮被点击了!")
    
    # 获取当前信息
    num = ui.numLineEdit.text()
    
    if num:
        # 标记该人员已考勤
        attended_ids.add(num)
        ui.statusLabel.setText("考勤状态：已考勤")

def get_images_and_labels(path):
    """获取训练图片和标签"""
    images = []
    ids = []
    
    for filename in os.listdir(path):
        if filename.endswith('.jpg'):
            face_id = int(filename.split('.')[0])
            image_path = os.path.join(path, filename)
            
            # 打开图片并转换为灰度
            PIL_img = Image.open(image_path).convert('L')
            np_img = np.array(PIL_img, dtype='uint8')
            
            # 检测人脸
            faces = faceCascade.detectMultiScale(np_img)
            for (x, y, w, h) in faces:
                images.append(np_img[y:y+h, x:x+w])
                ids.append(face_id)
    
    return images, ids

def train_recognizer():
    """训练人脸识别模型"""
    recognizer = cv.face.LBPHFaceRecognizer.create()
    path = "./data"
    faces, labels = get_images_and_labels(path)
    
    if len(faces) > 0:
        recognizer.train(faces, np.array(labels))
        if not os.path.exists('trains'):
            os.makedirs('trains')
        recognizer.write("trains/trainer.yml")
        print("模型训练完成并保存")

def on_Recog_click():
    print("Recog按钮被点击了!")
    
    # 清空输入框
    ui.nameLineEdit.clear()
    ui.numLineEdit.clear()
    ui.jointimeLineEdit.clear()

    if cap is None or not cap.isOpened():
        ui.statusLabel.setText("请先打开摄像头")
        return
    
    # 初始化人脸识别器
    recognizer = cv.face.LBPHFaceRecognizer.create()
    recognizer.read("trains/trainer.yml")
    while True:
        ret, frame = cap.read()
        if not ret:
            return
        
        # 转换为灰度图
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        
        # 检测人脸
        faces = faceCascade.detectMultiScale(gray)
        
        for (x, y, w, h) in faces:
            # 绘制人脸框
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 200, 0), 2)
            
            # 获取人脸区域
            roi_gray = gray[y:y + h, x:x + w]
            
            # 预测人脸
            id, conf = recognizer.predict(roi_gray)
            
            # 在图像上显示识别结果
            label = f"ID:{id} conf:{conf:.0f}%"
            cv.putText(frame, label, (x, y - 10), 2, 0.9, (0, 200, 0), 1)
            
            if conf < 90:  # 置信度阈值
                # 从数据库查询人员信息
                conn = sqlite3.connect('face_attendance.db')
                c = conn.cursor()
                c.execute("SELECT name, num, jointime FROM persons WHERE id=?", (id,))
                person = c.fetchone()
                conn.close()
                
                if person:
                    name, num, jointime = person
                    ui.nameLineEdit.setText(name)
                    ui.numLineEdit.setText(num)
                    ui.jointimeLineEdit.setText(jointime)
                    
                    # 检查考勤状态
                    if num in attended_ids:
                        ui.statusLabel.setText("考勤状态：已考勤")
                    else:
                        ui.statusLabel.setText("考勤状态：未考勤")
                else:
                    ui.nameLineEdit.setText("未知人员")
                    ui.numLineEdit.setText("")
                    ui.jointimeLineEdit.setText("")
                    ui.statusLabel.setText("")
            else:
                ui.nameLineEdit.setText("未识别到人脸")
                ui.numLineEdit.setText("")
                ui.jointimeLineEdit.setText("")
                ui.statusLabel.setText("考勤状态：未知")

        cv.waitKey(1) & 0xFF
        
        # 显示更新后的图像
        rgb_image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        ui.faceLabel.setPixmap(QPixmap.fromImage(convert_to_Qt_format))

        if on_Open_click == True:
            # 清空画面
            ui.faceLabel.clear()
            break

def on_Input_click():
    print("Input按钮被点击了!")
    
    if cap is None or not cap.isOpened():
        ui.statusLabel.setText("请先打开摄像头")
        return
    
    # 获取人员信息
    name = ui.nameLineEdit.text()
    num = ui.numLineEdit.text()
    jointime = ui.jointimeLineEdit.text()
    
    if not name or not num or not jointime:
        ui.statusLabel.setText("请输入完整的人员信息")
        return
    
    while True:
        ret, frame = cap.read()
        if not ret:
            return
        
        # 转换为灰度图
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        
        # 检测人脸
        face = faceCascade.detectMultiScale(gray)
        
        if len(face) == 0:
            ui.statusLabel.setText("未检测到人脸")
            return
        
        for x, y, w, h in face:
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 200, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]  # 截取部分

        cv.waitKey(1) & 0xFF

        # 转换为Qt可显示的格式
        rgb_image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        ui.faceLabel.setPixmap(QPixmap.fromImage(convert_to_Qt_format))

        if on_Recog_click or on_Open_click == True:
            break
    
    # 将人员信息存入数据库
    conn = sqlite3.connect('face_attendance.db')
    c = conn.cursor()
    
    try:
        # 插入人员信息
        c.execute("INSERT INTO persons (name, num, jointime) VALUES (?, ?, ?)", 
                 (name, num, jointime))
        person_id = c.lastrowid
        
        # 保存人脸图片
        if not os.path.exists('data'):
            os.makedirs('data')
        cv.imwrite(f"./data/{person_id}.jpg", roi_gray)
        
        conn.commit()
        ui.statusLabel.setText(f"人员录入成功！ID: {person_id}")
        
        # 训练模型
        train_recognizer()
    except sqlite3.IntegrityError:
        ui.statusLabel.setText("工号已存在，请勿重复录入")
    finally:
        conn.close()

def handle_close_event(event: QEvent):
    print("关闭键被点击，执行清理操作...")
    # 释放资源
    if cap is not None and cap.isOpened():
        cap.release()
    cv.destroyAllWindows()
    event.accept()

def setup_window():
    global app, window, ui
    
    # 初始化数据库
    init_database()
    
    app = QApplication(sys.argv)
    window = QMainWindow()
    
    # 创建UI对象
    ui = Ui_MainWindow()
    ui.setupUi(window)

    # 设置定时器更新时间
    time_timer = QTimer()
    time_timer.timeout.connect(update_current_time)
    time_timer.start(1000)

    # 连接按钮信号和槽函数
    ui.openButton.clicked.connect(on_Open_click)
    ui.saveButton.clicked.connect(on_Save_click)
    ui.recogButton.clicked.connect(on_Recog_click)
    ui.inputButton.clicked.connect(on_Input_click)

    # 替换窗口的closeEvent方法
    window.closeEvent = handle_close_event
    
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    setup_window()