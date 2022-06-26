#2022.6.20 15:03
#基于face_recognition库的简单人脸识别系统

from tkinter import *
import tkinter.messagebox
import face_recognition
import dlib
import time
import cv2
import os

def get_face():#获得人脸图像
	cap=cv2.VideoCapture(0)
	detector=dlib.get_frontal_face_detector()#调用dlib自带的人脸检测器
	second=0
	flag=0
	while(1):
		ret,frame=cap.read()#ret代表是否读取到图像，frame代表读取到的一帧图像
		second+=1
		print(second)
		frame=cv2.flip(frame, 1)
		gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		faces=detector(gray)
		i = 0
		for face in faces:
			x,y=face.left(),face.top()
			x1,y1=face.right(),face.bottom()
			cv2.rectangle(frame,(x, y),(x1, y1),(0, 255, 0), 2)#绘制人脸边框
			i=i+1
		if i==1 and not os.access('data/face_image/user.jpg',os.X_OK):
			cv2.imwrite("data/face_image/user.jpg",frame)
			flag=1
			'''
			cv2.putText(frame,'face num'+str(i),(x-10, y-10),     
					cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)#显示人脸坐标
			print(face, i)
			'''
		
		cv2.imshow('frame', frame)
		print(second,flag)
		if (cv2.waitKey(1)) & (flag==1) & (second>=50):#50帧图像后关闭摄像头
			break
		'''
		cv2.imshow("capture",frame)
		if cv2.waitKey(1) & 0xFF==ord('q'):
			cv2.imwrite("data/face_image/user.jpg",frame)
			break
		'''
	cap.release()
	cv2.destroyAllWindows()

def judge_face():#判断人脸
	flag=0
	
	second=0
	load_image=cv2.imread('data/face_image/user.jpg')
	'''
	cv2.imshow('55',load_image)
	cv2.waitKey(0)
	'''
	image_face_encoding=face_recognition.face_encodings(load_image)#读取用户图像数据
	#print(image_face_encoding)
	known_encodings=[]
	known_encodings.append(image_face_encoding[0])
	#print(known_encodings,len(known_encodings))
	cap=cv2.VideoCapture(0)
	#detector = dlib.get_frontal_face_detector()#调用dlib自带的人脸检测器
	process_this_frame = True #开始识别
	
	while(cap.isOpened()):
		ret, frame = cap.read()
		#frame=cv2.flip(frame, 1)
		if not ret:
			break
		second+=1
		#small_frame=cv2.resize(frame,(0,0),fx=0.33,fy=0.33)
		#rgb_frame=small_frame[:,:,::-1]
		rgb_frame=frame[:,:,::-1]
		
		#rgb_frame=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		'''
		gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		faces=detector(gray)
		i=0
		for face in faces:
			x, y = face.left(), face.top()
			x1, y1 = face.right(), face.bottom()
			cv2.rectangle(frame, (x, y), (x1, y1), (0, 255, 0), 2)
			
			i = i+1
			cv2.putText(frame, 'face num'+str(i), (x-10, y-10),
				cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
		cv2.imshow('frame', frame)
		'''
		if process_this_frame:
			face_locations=face_recognition.face_locations(rgb_frame)  # 获得所有人脸位置
			face_encodings=face_recognition.face_encodings(rgb_frame,face_locations)  # 获得人脸特征值
			face_names=[]  # 存储出现在画面中人脸的名字
			
			for face_encoding in face_encodings:  # 和数据库人脸进行对比
				# 如果当前人脸和数据库的人脸的相似度超过0.5，则认为人脸匹配
				matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.5)
				
				if True in matches:
					first_match_index=matches.index(True)
					# 返回相似度最高的作为当前人脸的名称
					name="user"
				else:
					name="unknown"
				face_names.append(name)
		if "user" in face_names:
			flag=1
		#print(face_names)
		process_this_frame = not process_this_frame
		# 将捕捉到的人脸显示出来
		for (top, right, bottom, left), name in zip(face_locations, face_names):
			cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)  # 画人脸矩形框
			# 加上人名标签
			cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
			font=cv2.FONT_HERSHEY_DUPLEX
			cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
		
		cv2.imshow('frame', frame)
		if ((cv2.waitKey(1)) & (second>=25) & ("user" not in face_names)) | ((cv2.waitKey(1)) & (second>=10) & ("user" in face_names)):
			break
	cap.release()
	cv2.destroyAllWindows()
	
	if flag==1:
		print("yes")
	else:
		print("no")

def show():#展示界面
	pass

def main():#主函数
	'''
	win=tkinter.Tk()
	win.title('face')
	win.geometry('400x300+400+200')
	win.config(background = "SkyBlue")
	'''
	if not os.access('data/face_image/user.jpg',os.X_OK):
		choice=tkinter.messagebox.askyesno(title='message', message="添加人脸数据?")
		if choice==True:
			get_face()
		else:
			pass
			#win.destroy()
	else:
		judge_face()
	
	#win.mainloop()
#main()
