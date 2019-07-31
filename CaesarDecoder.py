import enchant
import tkinter
from tkinter import *
tk = tkinter.Tk()

cipherBox = None
plainBox = None
keyBox = None
keyBoxMod = None
shifted = None
cur = 0
	
def decrypt():
	global shifted
	
	#get entered text, cut off last character(new line)
	cipherText = cipherBox.get('1.0', END)
	cipherText = cipherText[0:len(cipherText)-1]
	
	#if empty stop
	if cipherText == '':
		return
	
	#prep lists
	versions = ['']*26
	amountEng = [0]*26
	
	#loop through all possible shifts
	for shift in range(0,26):
		plainText = ''	
		
		#loop through each char in the text
		for letter in cipherText:
			#get ascii val
			num = ord(letter)

			#if not a letter just add it on
			if (num < 97 or num > 122) and (num < 65 or num > 90):
				plainText += chr(num)
			else:
				#if uppercase set the adjust value to 65
				if num >= 65 and num <= 90:
					adj = 65
				#if lowercase set adjust value to 97
				elif num >= 97 and num <= 122:
					adj = 97
					
				#adjust the number in to range and add the shift
				num = num - adj + shift
				
				#convert back to mod 26 and adjust back to ascii val
				convLetter = chr(((num % 26) + adj))
				
				#add to the plain text
				plainText += convLetter
		
		#place in the list of all plaintexts
		versions[shift] = plainText
		
		#split on spaces
		words = plainText.split(' ')
		
		#getting a US english dictionary for checking words
		dict = enchant.Dict("en_US")
		
		#loop through the words and keep track of how many words match per plain text
		for word in words:
			if dict.check(word) is True:
				amountEng[shift] += 1
			
	#zip up the lists containing the plaintexts, amount of enlgish words and the shifts
	shifted = list(zip(versions, amountEng, list(range(0,26))))
	
	#sort it based on amount of english words
	shifted.sort(key = lambda elem : elem[1], reverse=True)
		
	#assume correct plaintext is the one with most english words present
	plainText = shifted[0][0]
	key = (shifted[0][2]*-1)
	#update display accordingly
	updateDisplay(plainText, key)
	
#for iterating over the plaintexts in case the first one isn't correct
def change(next):
	global cur
	cur+=next
	cur = cur % 26
	
	plainText = shifted[cur][0]
	key = shifted[cur][2]*-1
	updateDisplay(plainText, key)
	
#used to update display
def updateDisplay(plainText, key):
	plainBox.delete('1.0', END)
	plainBox.insert(INSERT, plainText)
	
	keyBox.delete('1.0', END)
	keyBox.insert(INSERT, key)
	
	keyBoxMod.delete('1.0', END)
	keyBoxMod.insert(INSERT, str(key % 26) + " mod 26")
	
#setting up display
def displaySetup():
	global cipherBox, plainBox, keyBox, keyBoxMod
	
	tk.title("Caeser Cipher English Brute Force")
	tk.resizable(0,0)
	
	cipherTitle = Text(tk, height=1, width=12)
	cipherTitle.insert(INSERT, "Cipher Text:")
	cipherTitle.config(state = "disabled")
	cipherTitle.grid(row=0, column=1)
	cipherBox = Text(tk, height=15, width=40)
	cipherBox.grid(row=1, column=0, columnspan=3)
	
	plainTitle = Text(tk, height=1, width=12)
	plainTitle.insert(INSERT, "Plain Text:")
	plainTitle.config(state = "disabled")
	plainTitle.grid(row=2, column=1)
	plainBox = Text(tk, height=15, width=40)
	plainBox.grid(row=3, column=0, columnspan=3)
	
	keyBox = Text(tk, height=1, width=3)
	keyBox.grid(row=4, column=1)
	
	keyBoxMod = Text(tk, height=1, width=9)
	keyBoxMod.grid(row=5, column=1)
	
	Button(tk, text = "Decrypt", command=decrypt, height=1, width=7).grid(row=4, column=0)
	Button(tk, text = "Next Key", command=lambda next=1: change(next) , height=1, width=8).grid(row=4, column=2)
	Button(tk, text = "Prev Key", command=lambda next=-1: change(next)  , height=1, width=8).grid(row=5, column=2)
	
displaySetup()
tk.mainloop()


