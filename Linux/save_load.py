from pickle import dump, load
import pickle
import sys, pathlib
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

def save(items, filename):
	#open file
	file_to_save = open(filename, "wb")
	dump(items, file_to_save)
	file_to_save.close()
	





def load(filename) :
	print("filename : " + str(filename))
	#open file
	file_to_open = open(filename,"rb")
	
	#get items from the file
	items=pickle.load(file_to_open)
	file_to_open.close()

	return items


