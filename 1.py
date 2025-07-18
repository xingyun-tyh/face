import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QTableWidget
from face import Ui_MainWindow  # 导入生成的UI类
import cv2 as cv
from datetime import datetime
from PySide6.QtCore import QTimer, Qt
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
timer = None
attended_ids = set()  # 存储已考勤的人员ID
current_mode = "idle"  # 当前模式: idle, preview, recognition, input
recognizer = None  # 人脸识别器
current_capture_info = None  # 存储当前正在录入的人员信息

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
    
    # 创建考勤记录表
    c.execute('''CREATE TABLE IF NOT EXISTS attendance
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  person_id INTEGER NOT NULL,
                  attendance_time TEXT NOT NULL,
                  FOREIGN KEY(person_id) REFERENCES persons(id))''')
    
    conn.commit()
    conn.close()

# 加载人脸检测器
faceCascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
if faceCascade.empty():
    # 如果默认路径找不到，尝试当前目录
    faceCascade = cv.CascadeClassifier("./haarcascade_frontalface_alt2.xml")
    if faceCascade.empty():
        print("人脸检测器加载失败")

def update_current_time():
    """更新当前时间显示"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ui.timeLabel.setText(f"当前时间: {current_time}")

def on_Open_click():
    global cap, timer, current_mode
    
    print("Open按钮被点击了!")
    
    if cap is not None and cap.isOpened():
        # 关闭摄像头
        if timer and timer.isActive():
            timer.stop()
        cap.release()
        cap = None
        ui.faceLabel.clear()
        ui.openGroupBox.setTitle("打开")
        current_mode = "idle"
        ui.statusLabel.setText("摄像头已关闭")
    else:
        ui.openGroupBox.setTitle("关闭")
        ui.statusLabel.setText("正在打开摄像头...")
        
        # 初始化摄像头
        cap = cv.VideoCapture(0)
        if not cap.isOpened():
            ui.statusLabel.setText("摄像头打开失败")
            return
        
        # 初始化定时器
        timer = QTimer()
        timer.timeout.connect(update_frame)
        timer.start(30)  # 每30ms更新一次，约33帧/秒
        current_mode = "preview"

def update_frame():
    global cap, current_mode, recognizer
    
    if cap is None or not cap.isOpened():
        return
    
    ret, frame = cap.read()
    if not ret:
        ui.statusLabel.setText("读取帧失败")
        return
    
    # 转换为灰度图
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    
    # 检测人脸
    faces = []
    if faceCascade is not None:
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    # 根据当前模式处理
    if current_mode == "preview":
        # 预览模式
        if len(faces) > 0:
            ui.statusLabel.setText(f"检测到 {len(faces)} 张人脸")
        else:
            ui.statusLabel.setText("未检测到人脸")
        
        # 绘制人脸矩形框
        for (x, y, w, h) in faces:
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 200, 0), 2)
    
    elif current_mode == "recognition":
        # 识别模式
        if recognizer is None:
            # 初始化人脸识别器
            recognizer = cv.face.LBPHFaceRecognizer.create()
            if os.path.exists("trains/trainer.yml"):
                recognizer.read("trains/trainer.yml")
            else:
                ui.statusLabel.setText("未找到训练模型")
                return
        
        if len(faces) > 0:
            ui.statusLabel.setText(f"检测到 {len(faces)} 张人脸")
        else:
            ui.statusLabel.setText("未检测到人脸")
        
        # 处理每个人脸
        for (x, y, w, h) in faces:
            # 绘制人脸框
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 200, 0), 2)
            
            # 获取人脸区域
            roi_gray = gray[y:y + h, x:x + w]
            
            try:
                # 尝试预测人脸
                id, conf = recognizer.predict(roi_gray)
                
                # 在图像上显示识别结果
                label = f"ID:{id} conf:{conf:.0f}%"
                cv.putText(frame, label, (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 200, 0), 2)
                
                if conf < 60:  # 置信度阈值
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
                    ui.nameLineEdit.setText("未识别")
                    ui.numLineEdit.setText("")
                    ui.jointimeLineEdit.setText("")
                    ui.statusLabel.setText("考勤状态：未知")
            except Exception as e:
                print(f"人脸预测出错: {e}")
                ui.statusLabel.setText(f"人脸识别出错: {e}")
    
    elif current_mode == "input":
        # 录入模式
        if len(faces) == 1:
            ui.statusLabel.setText(f"检测到 1 张人脸-准备录入")
        elif len(faces) > 1:
            ui.statusLabel.setText(f"检测到{len(faces)}张人脸-请确保只有一张人脸在画面中")
        else:
            ui.statusLabel.setText("未检测到人脸-请确保人脸在画面中")
        
        # 绘制人脸矩形框
        for (x, y, w, h) in faces:
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 200, 0), 2)
    
    # 转换为Qt可显示的格式
    rgb_image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    h, w, ch = rgb_image.shape
    bytes_per_line = ch * w
    convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
    ui.faceLabel.setPixmap(QPixmap.fromImage(convert_to_Qt_format))

def on_Save_click():
    print("Save按钮被点击了!")
    
    # 获取当前信息
    num = ui.numLineEdit.text()
    
    if num:
        # 标记该人员已考勤
        attended_ids.add(num)
        
        # 记录考勤时间
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 保存到数据库
        conn = sqlite3.connect('face_attendance.db')
        c = conn.cursor()
        
        try:
            # 获取人员ID
            c.execute("SELECT id FROM persons WHERE num=?", (num,))
            person_id = c.fetchone()
            
            if person_id:
                # 插入考勤记录
                c.execute("INSERT INTO attendance (person_id, attendance_time) VALUES (?, ?)", 
                         (person_id[0], current_time))
                conn.commit()
                ui.statusLabel.setText(f"考勤成功！时间: {current_time}")
            else:
                ui.statusLabel.setText("未找到该人员信息")
        except Exception as e:
            ui.statusLabel.setText(f"考勤保存失败: {e}")
        finally:
            conn.close()

def get_images_and_labels(path):
    """获取训练图片和标签"""
    images = []
    ids = []
    
    for filename in os.listdir(path):
        if filename.endswith('.jpg'):
            face_id = int(filename.split('.')[0])
            image_path = os.path.join(path, filename)
            
            try:
                # 打开图片并转换为灰度
                PIL_img = Image.open(image_path).convert('L')
                np_img = np.array(PIL_img, dtype='uint8')
                
                # 检测人脸
                faces = faceCascade.detectMultiScale(np_img)
                for (x, y, w, h) in faces:
                    images.append(np_img[y:y+h, x:x+w])
                    ids.append(face_id)
            except Exception as e:
                print(f"处理图片 {image_path} 出错: {e}")
    
    return images, ids

def train_recognizer():
    """训练人脸识别模型"""
    recognizer = cv.face.LBPHFaceRecognizer.create()
    path = "./data"
    
    if not os.path.exists(path):
        os.makedirs(path)
        ui.statusLabel.setText("没有训练数据")
        return
    
    faces, labels = get_images_and_labels(path)
    
    if len(faces) == 0:
        ui.statusLabel.setText("没有可训练的人脸数据")
        return
    
    try:
        recognizer.train(faces, np.array(labels))
        
        if not os.path.exists('trains'):
            os.makedirs('trains')
        
        recognizer.write("trains/trainer.yml")
        ui.statusLabel.setText("模型训练完成并保存")
        print("模型训练完成并保存")
    except Exception as e:
        ui.statusLabel.setText(f"模型训练失败: {e}")
        print(f"模型训练出错: {e}")

def on_Recog_click():
    global current_mode
    
    print("Recog按钮被点击了!")
    
    # 清空输入框
    ui.nameLineEdit.clear()
    ui.numLineEdit.clear()
    ui.jointimeLineEdit.clear()

    if cap is None or not cap.isOpened():
        ui.statusLabel.setText("请先打开摄像头")
        return
    
    # 切换到识别模式
    current_mode = "recognition"
    ui.statusLabel.setText("识别模式：正在识别人脸...")

def capture_and_save_face():
    """捕获并保存人脸图片"""
    global current_mode, current_capture_info
    
    if cap is None or not cap.isOpened():
        ui.statusLabel.setText("摄像头未打开")
        return False
    
    # 读取当前帧
    ret, frame = cap.read()
    if not ret:
        ui.statusLabel.setText("读取帧失败")
        return False
    
    # 转换为灰度图
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    
    # 检测人脸
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    if len(faces) == 1:
        (x, y, w, h) = faces[0]
        roi_gray = gray[y:y + h, x:x + w]
        
        # 将人员信息存入数据库
        conn = sqlite3.connect('face_attendance.db')
        c = conn.cursor()
        
        if current_capture_info:
            name, num, jointime = current_capture_info
            
            try:
                # 插入人员信息
                c.execute("INSERT INTO persons (name, num, jointime) VALUES (?, ?, ?)", 
                         (name, num, jointime))
                person_id = c.lastrowid
                
                # 保存人脸图片
                data_dir = './data'
                if not os.path.exists(data_dir):
                    os.makedirs(data_dir)
                
                # 保存灰度人脸图片
                cv.imwrite(f"./data/{person_id}.jpg", roi_gray)
                
                # 同时保存彩色截图供参考
                color_dir = './color_data'
                if not os.path.exists(color_dir):
                    os.makedirs(color_dir)
                cv.imwrite(f"./color_data/{person_id}_color.jpg", frame)
                
                conn.commit()
                ui.statusLabel.setText(f"人员录入成功！ID: {person_id}")
                
                # 训练模型
                train_recognizer()
                
                # 重置捕获状态
                current_capture_info = None
                
                # 切换回预览模式
                current_mode = "preview"
                return True
            except sqlite3.IntegrityError:
                ui.statusLabel.setText("工号已存在，请勿重复录入")
            except Exception as e:
                ui.statusLabel.setText(f"录入失败: {e}")
            finally:
                conn.close()
        else:
            ui.statusLabel.setText("未设置人员信息")
    elif len(faces) > 1:
        ui.statusLabel.setText("检测到多张人脸，请确保只有一张人脸在画面中")
    else:
        ui.statusLabel.setText("未检测到人脸，请确保人脸在画面中")
    
    return False

def on_Input_click():
    global current_mode, current_capture_info
    
    print("Input按钮被点击了!")
    
    # 获取人员信息
    name = ui.nameLineEdit.text()
    num = ui.numLineEdit.text()
    jointime = ui.jointimeLineEdit.text()
    
    if not name or not num or not jointime:
        ui.statusLabel.setText("请输入完整的人员信息")
        return
    
    # 存储当前要录入的信息
    current_capture_info = (name, num, jointime)
    
    # 切换到录入模式
    current_mode = "input"
    ui.statusLabel.setText("录入模式：正在检测人脸...")
    
    # 立即尝试捕获并保存人脸
    success = capture_and_save_face()
    
    if not success:
        # 如果捕获失败，保持在录入模式以便用户调整
        ui.statusLabel.setText("录入失败，请调整姿势后重试")

def init_query_table():
    """初始化查询表格"""
    # 设置表格列数和标题（与图片布局匹配）
    headers = ["序号", "姓名", "工号", "加入时间", "考勤时间"]
    ui.queryTableWidget.setColumnCount(len(headers))
    ui.queryTableWidget.setHorizontalHeaderLabels(headers)
    
    # 设置列宽
    ui.queryTableWidget.setColumnWidth(0, 60)    # 序号
    ui.queryTableWidget.setColumnWidth(1, 100)   # 姓名
    ui.queryTableWidget.setColumnWidth(2, 80)    # 工号
    ui.queryTableWidget.setColumnWidth(3, 150)   # 加入时间
    ui.queryTableWidget.setColumnWidth(4, 300)    # 考勤时间
    
    # 设置表格属性
    ui.queryTableWidget.horizontalHeader().setStretchLastSection(True)  # 最后一列扩展
    ui.queryTableWidget.setSelectionBehavior(QTableWidget.SelectRows)
    ui.queryTableWidget.setEditTriggers(QTableWidget.NoEditTriggers)


def on_Query_click():
    print("Query按钮被点击了!")
    
    # 清空表格
    ui.queryTableWidget.setRowCount(0)
    init_query_table()
    
    # 连接数据库
    conn = sqlite3.connect('face_attendance.db')
    c = conn.cursor()
    
    try:
        # 查询所有考勤记录
        query = """
        SELECT 
            persons.name,
            persons.num,
            persons.jointime,
            attendance.attendance_time
        FROM attendance
        INNER JOIN persons ON attendance.person_id = persons.id
        ORDER BY attendance.attendance_time DESC
        """
        
        c.execute(query)
        records = c.fetchall()
        
        if not records:
            ui.statusLabel.setText("没有找到考勤记录")
            return
        
        # 设置表格行数
        ui.queryTableWidget.setRowCount(len(records))
        
        # 确保表格有正确的列数
        if ui.queryTableWidget.columnCount() != 5:
            ui.queryTableWidget.setColumnCount(5)
            ui.queryTableWidget.setHorizontalHeaderLabels(["序号", "姓名", "工号", "加入时间", "考勤时间"])
        
        # 填充表格
        for row_idx, record in enumerate(records):
            # 序号列
            item_id = QTableWidgetItem(str(row_idx + 1))
            item_id.setTextAlignment(Qt.AlignCenter)
            ui.queryTableWidget.setItem(row_idx, 0, item_id)
            
            # 姓名列
            item_name = QTableWidgetItem(record[0])
            item_name.setTextAlignment(Qt.AlignCenter)
            ui.queryTableWidget.setItem(row_idx, 1, item_name)
            
            # 工号列
            item_num = QTableWidgetItem(record[1])
            item_num.setTextAlignment(Qt.AlignCenter)
            ui.queryTableWidget.setItem(row_idx, 2, item_num)
            
            # 加入时间列
            item_jointime = QTableWidgetItem(record[2])
            item_jointime.setTextAlignment(Qt.AlignCenter)
            ui.queryTableWidget.setItem(row_idx, 3, item_jointime)
            
            # 考勤时间列
            item_attendance = QTableWidgetItem(record[3])
            item_attendance.setTextAlignment(Qt.AlignCenter)
            ui.queryTableWidget.setItem(row_idx, 4, item_attendance)
        
        ui.statusLabel.setText(f"查询到 {len(records)} 条考勤记录")
        
        # 刷新表格视图
        ui.queryTableWidget.viewport().update()
        
    except Exception as e:
        ui.statusLabel.setText(f"查询失败: {e}")
        print(f"查询错误: {e}")
    finally:
        conn.close()

def handle_close_event(event):
    print("关闭键被点击，执行清理操作...")
    # 释放资源
    if cap is not None and cap.isOpened():
        cap.release()
    if timer and timer.isActive():
        timer.stop()
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

    init_query_table()

    # 设置定时器更新时间
    time_timer = QTimer()
    time_timer.timeout.connect(update_current_time)
    time_timer.start(1000)
    update_current_time()  # 立即更新一次

    # 连接按钮信号和槽函数
    ui.openButton.clicked.connect(on_Open_click)
    ui.saveButton.clicked.connect(on_Save_click)
    ui.recogButton.clicked.connect(on_Recog_click)
    ui.inputButton.clicked.connect(on_Input_click)
    ui.queryButton.clicked.connect(on_Query_click)

    # 替换窗口的closeEvent方法
    window.closeEvent = handle_close_event
    
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    setup_window()