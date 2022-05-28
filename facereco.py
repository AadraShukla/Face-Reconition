import face_recognition
import cv2
import pickle
import os
import numpy as np
from deepface import DeepFace
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import glob


class Dlib_Face_Unlock:
	#to check for updates, if update has occured, encoded and saved to the encoded pickle file
	def __init__(self):
		#this is to detect if the directory is found or not
		try:
			#this will open the existing pickle file to load in the encoded faces of the users who has sign up for the service
			with open (r"C:\Users\HP\Desktop\Code-master\Face Recognition\labels.pickle",'rb') as self.f:
				self.og_labels = pickle.load(self.f)
			print(self.og_labels)
		#error checking
		except FileNotFoundError:
			#allowing to known that their was no file found
			print("No label.pickle file detected, will create required pickle files")

		#this will be used to for selecting the photos
		self.current_id = 0
		#creating a blank ids dictionary
		self.labels_ids = {}
		#this is the directory where all the users are stored
		self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
		self.image_dir = os.path.join(self.BASE_DIR, 'images')
		for self.root, self.dirs, self.files in os.walk(self.image_dir):
			#checking each folder in the images directory
			for self.file in self.files:
				#looking for any png or jpg files of the users
				if self.file.endswith('png') or self.file.endswith('jpg'):
					#getting the folder name, as the name of the folder will be the user
					self.path = os.path.join(self.root, self.file)
					self.label = os.path.basename(os.path.dirname(self.path)).replace(' ','-').lower()
					if not self.label in self.labels_ids:
						#adding the user into the labels_id dictionary
						self.labels_ids[self.label] = self.current_id
						self.current_id += 1
						self.id = self.labels_ids[self.label]

		print(self.labels_ids)
		#this is compare the new label ids to the old label ids dictionary seeing if their has been any new users or old users
		#being added to the system, if there is no change then nothing will happen
		self.og_labels=0
		if self.labels_ids != self.og_labels:
			#if the dictionary change then the new dictionary will be dump into the pickle file
			with open('labels.pickle','wb') as self.file:
				pickle.dump(self.labels_ids, self.file)

			self.known_faces = []
			for self.i in self.labels_ids:
				#Get number of images of a person
				noOfImgs = len([filename for filename in os.listdir('images/' + self.i) if os.path.isfile(os.path.join('images/' + self.i, filename))])
				print(noOfImgs)
				for imgNo in range(1,(noOfImgs+1)):
					self.directory = os.path.join(self.image_dir, self.i, str(imgNo)+'.png')
					self.img = face_recognition.load_image_file(self.directory)
					try:
						self.img_encoding = face_recognition.face_encodings(self.img)[0]
					except IndexError as e:
						print("No face detected at the previous registration please delete previous registration and try again")
						exit(1)
					self.known_faces.append([self.i, self.img_encoding])
			print(self.known_faces)
			print("No Of Imgs"+str(len(self.known_faces)))
			with open('KnownFace.pickle','wb') as self.known_faces_file:
				pickle.dump(self.known_faces, self.known_faces_file)
		else:
			with open (r"C:\Users\HP\Desktop\Code-master\Face Recognition\KnownFace.pickle",'rb') as self.faces_file:
				self.known_faces = pickle.load(self.faces_file)
			print(self.known_faces)
	  

	#Method: ID
	#Purpose:This is method will be used to create a live feed .i.e turning on the devices camera
	#then the live feed will be used to get an image of the user and then encode the users face
	#once the users face has been encoded then it will be compared to in the known faces
	#therefore identifying the user
	def ID(self):
		#turning on the camera to get a photo of the user frame by frame
		self.cap = cv2.VideoCapture(0)
		cv2.namedWindow("test")
		#seting the running variable to be true to allow me to known if the face recog is running
		self.running = True
		self.face_names = []
		while self.running == True:
			#taking a photo of the frame from the camera
			while True:
				self.ret, self.frame = self.cap.read()
				cv2.imshow("test", self.frame)
				if not self.ret:
					break
				k = cv2.waitKey(1)
		
				if k % 256 == 27:
					# ESC pressed
					print("Escape hit, closing...")
					self.cap.release()
					cv2.destroyAllWindows()
					break
				elif k % 256 == 32:
					self.cap.release()
					cv2.destroyAllWindows()
					break
			raiseFrame(regFrame)
			#analysing emotions
			face_analysis_2 = DeepFace.analyze(self.frame)
			emotion.set(face_analysis_2["dominant_emotion"])
			#resizing the frame so that the face recog module can read it
			self.small_frame = cv2.resize(self.frame, (0,0), fx = 0.5, fy = 0.5)
			#converting the image into black and white
			self.rgb_small_frame = self.small_frame[:, :, ::-1]
			if self.running:
				#searching the black and white image for a face
				self.face_locations = face_recognition.face_locations(self.frame)

				# if self.face_locations == []:
				#     Dlib_Face_Unlock.ID(self)
				#it will then encode the face into a matrix
				self.face_encodings = face_recognition.face_encodings(self.frame, self.face_locations)
				#creating a names list to append the users identify into
				self.face_names = []
				#looping through the face_encoding that the system made
				for self.face_encoding in self.face_encodings:
					#looping though the known_faces dictionary
					for self.face in self.known_faces:
						#using the compare face method in the face recognition module
						self.matches = face_recognition.compare_faces([self.face[1]], self.face_encoding)
						print(self.matches)
						self.name = 'Unknown'
						#compare the distances of the encoded faces
						self.face_distances = face_recognition.face_distance([self.face[1]], self.face_encoding)
						#uses the numpy module to comare the distance to get the best match
						self.best_match = np.argmin(self.face_distances)
						print(self.best_match)
						print('This is the match in best match',self.matches[self.best_match])
						if self.matches[self.best_match] == True:
							self.running = False
							self.face_names.append(self.face[0])
							break
						next
			print("The best match(es) is"+str(self.face_names))
			self.cap.release()
			cv2.destroyAllWindows()
			break
		return self.face_names

def register():
	#Create images folder
	if not os.path.exists("images"):
		os.makedirs("images")
	#Create folder of person (IF NOT EXISTS) in the images folder
	Path("images/"+name.get()).mkdir(parents=True, exist_ok=True)
	#Obtain the number of photos already in the folder
	numberOfFile = len([filename for filename in os.listdir('images/' + name.get()) if os.path.isfile(os.path.join('images/' + name.get(), filename))])
	#Add 1 because we start at 1
	numberOfFile+=1
	#Take a photo code
	cam = cv2.VideoCapture(0)
	
	cv2.namedWindow("test")
	
	
	while True:
		ret, frame = cam.read()
		cv2.imshow("test", frame)
		if not ret:
			break
		k = cv2.waitKey(1)
		
		if k % 256 == 27:
			# ESC pressed
			print("Escape hit, closing...")
			cam.release()
			cv2.destroyAllWindows()
			break
		elif k % 256 == 32:
			# SPACE pressed
			img_name = str(numberOfFile)+".png"
			cv2.imwrite(img_name, frame)
			print("{} written!".format(img_name))
			os.replace(str(numberOfFile)+".png", "images/"+name.get().lower()+"/"+str(numberOfFile)+".png")
			cam.release()
			cv2.destroyAllWindows()
			break
	raiseFrame(loginFrame)
	
#Passing in the model
def login():
	# After someone has registered, the face scanner needs to load again with the new face
	dfu = Dlib_Face_Unlock()
	#Will return the user's name as a list, will return an empty list if no matches
	user = dfu.ID()
	if user ==[]:
		messagebox.showerror("Alert","Face Not Recognised")
		return
	loggedInUser.set(user[0])
	raiseFrame(userMenuFrame)

#Tkinter
root = tk.Tk()
root.title("Face Login")
#Frames
loginFrame=tk.Frame(root)
regFrame=tk.Frame(root)
userMenuFrame = tk.Frame(root)

#Define Frame List
frameList=[loginFrame,regFrame,userMenuFrame]
#Configure all Frames
for frame in frameList:
	frame.grid(row=0,column=0, sticky='news')
	frame.configure(bg='#86EBC0')
	
def raiseFrame(frame):
	frame.tkraise()

def regFrameRaiseFrame():
	raiseFrame(regFrame)
def logFrameRaiseFrame():
	raiseFrame(loginFrame)
#Tkinter Vars
#Stores user's name when registering
name = tk.StringVar()
#Stores user's name when they have logged in
loggedInUser = tk.StringVar()
emotion = tk.StringVar()


tk.Label(loginFrame,text="FACE RECOGNITION",font=("Bebas Neue", 60),bg="#86EBC0").grid(row=1,column=1,columnspan=5,sticky=tk.E)
loginButton = tk.Button(loginFrame,text="LOGIN",bg="#F79DF3",font=("Amatic SC", 30),command=login)
loginButton.grid(row=4,column=5)
regButton = tk.Button(loginFrame,text="REGISTER",command=regFrameRaiseFrame,bg="#F79DF3",font=("Amatic SC", 30))
regButton.grid(row=4,column=1)

tk.Label(regFrame,text="REGISTER",font=("Bebas Neue",60),bg="#86EBC0").grid(row=1,column=1,columnspan=5,)
tk.Label(regFrame,text="NAME: ",font=("Amatic SC",30),bg="#86EBC0").grid(row=2,column=1)
nameEntry=tk.Entry(regFrame,textvariable=name,font=("Amatic SC",30)).grid(row=2,column=2)

registerButton = tk.Button(regFrame,text="REGISTER",command=register,bg="#F79DF3",font=("Amatic SC", 30))
registerButton.grid(row=3,column=1)
BackButton = tk.Button(regFrame,text="BACK",command=logFrameRaiseFrame,bg="#F79DF3",font=("Amatic SC", 30))
BackButton.grid(row=3,column=3)

tk.Label(userMenuFrame,text="HEY, ",font=("Alata",40),bg="#86EBC0").grid(row=1,column=1)
tk.Label(userMenuFrame,textvariable=loggedInUser,font=("Alata",40),bg="#86EBC0").grid(row=1,column=2)
tk.Label(userMenuFrame,text="YOUR EMOTION :",font=("Alata",40),bg="#86EBC0").grid(row=2,column=1)
tk.Label(userMenuFrame,textvariable=emotion,font=("Alata",40),bg="#86EBC0").grid(row=2,column=5)
tk.Button(userMenuFrame,text="BACK",font=("Amatic SC", 30),bg="#F79DF3",command=logFrameRaiseFrame).grid(row=3,column=9,sticky='ew')


#Load Faces
dfu = Dlib_Face_Unlock()
raiseFrame(loginFrame)
root.mainloop()






