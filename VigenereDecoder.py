import tkinter
from tkinter import *
tk = tkinter.Tk()

cipherBox = None
plainBox = None
keyBox = None
	
def decrypt():
	
	#get entered text, cut off last character(new line)
	cipherText = cipherBox.get('1.0', END)
	cipherText = cipherText[0:len(cipherText)-1]
	
	#get key
	keyText = keyBox.get('1.0', END)
	keyText = keyText[0:len(keyText)-1]
	
	#if empty stop
	if cipherText == '' or keyText == '':
		return
	
	#for forming the plaintext
	plainText = ''
	
	#for keeping track of location within key
	keyCount = 0

	#loop through each letter in the cipher text
	for letter in cipherText:
	
		#convert current cipher letter, and key letter to numbers
		ciphNum = ord(letter)
		keyNum = ord(keyText[keyCount % len(keyText)])
				
		#if not a letter just add it on
		if (ciphNum < 97 or ciphNum > 122) and (ciphNum < 65 or ciphNum > 90):
				plainText += chr(ciphNum)
		else:
			#check what we should adjust them by, uppercase 64, lower 96
			ciphAdj = getAdjust(ciphNum)
			keyAdj = getAdjust(keyNum)
			
			#adjust values
			keyNum -= keyAdj
			ciphNum -= ciphAdj
			
			#convert and keep in mod 26
			ciphNum = (ciphNum - keyNum) % 26
			
			#convert back to ascii
			plainText += chr(ciphNum + ciphAdj + 1)
			keyCount += 1
					
	updateDisplay(plainText)	

#for finding what adjust to be used to bring number between 1 and 26
def getAdjust(num):
	if num >= 65 and num <= 90:
		return 64
	elif num >= 97 and num <= 122:
		return 96
		
#used to update display
def updateDisplay(plainText):
	plainBox.config(state = 'normal')
	plainBox.delete('1.0', END)
	plainBox.insert(INSERT, plainText)
	plainBox.config(state = 'disabled')
	
#setting up display
def displaySetup():
	global cipherBox, plainBox, keyBox, keyBoxMod
	
	tk.title("Vigenere Cipher")
	tk.resizable(0,0)
	
	keyTitle = Text(tk, height=1, width=4)
	keyTitle.insert(INSERT, "Key:")
	keyTitle.config(state = "disabled")
	keyTitle.grid(row=0, column=0)
	
	keyBox = Text(tk, height=1, width=15)
	keyBox.grid(row=0, column=1)
	
	cipherTitle = Text(tk, height=1, width=12)
	cipherTitle.insert(INSERT, "Cipher Text:")
	cipherTitle.config(state = "disabled")
	cipherTitle.grid(row=0, column=2)
	cipherBox = Text(tk, height=15, width=40)
	cipherBox.grid(row=1, column=0, columnspan=3)
	
	plainTitle = Text(tk, height=1, width=12)
	plainTitle.insert(INSERT, "Plain Text:")
	plainTitle.config(state = "disabled")
	plainTitle.grid(row=2, column=1)
	plainBox = Text(tk, height=15, width=40, state = 'disabled')
	plainBox.grid(row=3, column=0, columnspan=3)
	
	Button(tk, text = "Decrypt", command=decrypt, height=1, width=7).grid(row=4, column=1)
	
displaySetup()
tk.mainloop()


