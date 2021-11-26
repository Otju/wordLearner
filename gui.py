from tkinter import *
from tkinter import ttk
import wordPicker
import json

root = Tk()
root.title("Руски")
rightWords = None
try:
  rightWordsFile = open("rightWords.json", encoding="utf-8")
  rightWords = json.load(rightWordsFile)
  rightWordsFile.close()
except:
  newFile = open("rightWords.json", "w", encoding="utf-8")
  newFile.write("[]")
  newFile.close()
  rightWordsFile = open("rightWords.json", encoding="utf-8")
  rightWords = json.load(rightWordsFile)
  rightWordsFile.close()
word = ""
translation= ""
translitteration = ""
totalRightCount = StringVar()

class Checkbar(Frame):
   def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
      Frame.__init__(self, parent)
      self.vars = []
      self.chks = []
      for pick in picks:
         var = IntVar()
         chk = Checkbutton(self, text=pick, variable=var)
         chk.pack(side=side, anchor=anchor, expand=YES)
         self.vars.append(var)
         self.chks.append(chk)
   def state(self):
      return map((lambda var: var.get()), self.vars)
   def checkAll(self):
     for chk in self.chks:
       chk.select()
dictionaryFile = open("dictionary.json", encoding="utf-8")
dictionary = json.load(dictionaryFile)
allWordPacketNames = list(dictionary.keys())
currentWordNumber = 0
def getNew():
  global currentWordNumber
  wordPacketNames = getSelectedWordPacketNames()
  [newWord, newTranslation, newTranslitteration, dictListLength, fullDictListLength] = wordPicker.getWord(wordPacketNames, getDisableMultiWord(), getDisableOver10Letters(), rightWords, currentWordNumber, dictionary)
  if(currentWordNumber==dictListLength):
      currentWordNumber = 0
  global word
  global translation
  global translitteration
  word = newWord
  translation = newTranslation
  translitteration = newTranslitteration
  totalRightCount.set(f"Oikein {len(rightWords)}/{fullDictListLength}")
  if(getHasText()):
    currentWord.set(newWord)
  else:
    currentWord.set("")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)


topRow = 0
wordDisableRow = topRow + 1
wordChooseRow = wordDisableRow + 1
readHearRow = wordChooseRow + 1
inputRow = readHearRow + 1
wordRow = inputRow + 1
translitteraitionRow = wordRow + 1
translationRow = translitteraitionRow + 1
showWordRow = translationRow + 1
buttonRow = showWordRow + 3

currentWord = StringVar()
ttk.Label(mainframe, textvariable=currentWord).grid(column=2, row=wordRow, sticky=(W, E))
ttk.Label(mainframe, textvariable=totalRightCount).grid(column=3, row=wordRow, sticky=(W, E))

userTranslitteration = StringVar()
userTranslitterationEntry = ttk.Entry(mainframe, width=7, textvariable=userTranslitteration)
userTranslitterationEntry.grid(column=2, row=translitteraitionRow, sticky=(W, E))

userTranslation = StringVar()
userTranslationEntry = ttk.Entry(mainframe, width=7, textvariable=userTranslation)
userTranslationEntry.grid(column=2, row=translationRow, sticky=(W, E))

shownWord = StringVar()
ttk.Label(mainframe, textvariable=shownWord).grid(column=2, row=showWordRow, sticky=(W, E))


shownTranslitteration = StringVar()
transLitterationLabel = ttk.Label(mainframe, textvariable=shownTranslitteration)
transLitterationLabel.grid(column=2, row=showWordRow + 1, sticky=(W, E))

shownTranslation = StringVar()
translationLabel = ttk.Label(mainframe, textvariable=shownTranslation)
translationLabel.grid(column=2, row=showWordRow + 2, sticky=(W, E))

difficulty = Checkbar(mainframe, ['Ei monisanaisia', "Ei yli 10 kirjaimen pituisia"])
difficulty.grid(row=wordDisableRow, sticky=W, column=2)
ttk.Label(mainframe, text="Sanat").grid(column=1, row=wordDisableRow, sticky=W)


wordPackets = Checkbar(mainframe, allWordPacketNames)
wordPackets.checkAll()
wordPackets.grid(row=wordChooseRow, sticky=W, column=2)
ttk.Label(mainframe, text="Sanastot").grid(column=1, row=wordChooseRow, sticky=W)

settings = Checkbar(mainframe, ['Ääni', "Teksti"])
settings.checkAll()
settings.grid(row=readHearRow, sticky=W, column=2)
ttk.Label(mainframe, text="Esitystavat").grid(column=1, row=readHearRow, sticky=W)

inputs = Checkbar(mainframe, ['Translitterointi', "Käännös"])
inputs.checkAll()
inputs.grid(row=inputRow, sticky=W, column=2)
ttk.Label(mainframe, text="Tarkistettavat kentät").grid(column=1, row=inputRow, sticky=W)

def getDisableMultiWord():
  return list(difficulty.state())[0] == 1

def getDisableOver10Letters():
  return list(difficulty.state())[1] == 1

def getHasSound():
  return list(settings.state())[0] == 1

def getHasText():
  return list(settings.state())[1] == 1

def getNeedsTranslitteration():
  return list(inputs.state())[0] == 1

def getNeedsTranslation():
  return list(inputs.state())[1] == 1

def getSelectedWordPacketNames():
  selectedWordPackets = []
  states = list(wordPackets.state())
  i = 0
  for state in states:
    if(state == 1):
      selectedWordPackets.append(allWordPacketNames[i])
    i += 1
  return selectedWordPackets
  
def setWordAsRight():
    rightWords.append(word)
    with open('rightWords.json', 'w', encoding='utf-8') as file:
      json.dump(rightWords, file, ensure_ascii=False)


def check():
  global isRightOverride
  translitterationRight = userTranslitteration.get() == translitteration or not getNeedsTranslitteration()
  translationRight = userTranslation.get() == translation or not getNeedsTranslation()
  if(translitterationRight): transLitterationLabel.config(foreground="green")
  else: transLitterationLabel.config(foreground="red")
  if(translationRight): translationLabel.config(foreground="green")
  else: translationLabel.config(foreground="red")
  if(translationRight and translitterationRight):
    setWordAsRight()
  shownWord.set("Sana: " + word)
  shownTranslitteration.set("Translitterointi: " + translitteration)
  shownTranslation.set("Käännös: " + translation)

firstTime = True
nextButtonText = StringVar()
nextButtonText.set("Tarkista")
def next():
  global firstTime
  if(firstTime):
    check()
    firstTime = False
    nextButtonText.set("Seuraava")
  else:
    firstTime = True
    nextButtonText.set("Tarkista")
    getNew()
    shownWord.set("")
    shownTranslation.set("")
    shownTranslitteration.set("")
    userTranslitteration.set("")
    userTranslation.set("")
    root.after(1000, speak)
  

def speak():
  if(getHasSound()):
    wordPicker.speak(word)
  
def handleRightOverride():
  setWordAsRight()
  next()

def resetRightWords():
   rightWordsFile = open("rightWords.json", "w", encoding="utf-8")
   rightWordsFile.truncate(0)
   rightWordsFile.write("[]")
   rightWordsFile.close()
   rightWords.clear()

def updateReadSpeed(_):
  newValue = slider.get()
  wordPicker.setReadSpeed(newValue)

nextButton = ttk.Button(mainframe, textvariable=nextButtonText, command=next).grid(column=3, row=buttonRow, sticky=W)
ttk.Button(mainframe, text="Toista sana", command=speak).grid(column=1, row=buttonRow, sticky=W)
ttk.Button(mainframe, text="Olin oikeassa", command=handleRightOverride).grid(column=2, row=buttonRow, sticky=W)
ttk.Button(mainframe, text="Aloita alusta", command=resetRightWords).grid(column=2, row=topRow, sticky=W)
slider = ttk.Scale(mainframe, from_=50, to=250, value=150)
slider.grid(column=3, row=topRow, sticky=E)
slider.bind("<ButtonRelease-1>", updateReadSpeed)
ttk.Label(mainframe, text="Lukunopeus").grid(column=2, row=topRow, sticky=E)




ttk.Label(mainframe, text="Translitterointi").grid(column=1, row=translitteraitionRow, sticky=W)
ttk.Label(mainframe, text="Käännös").grid(column=1, row=translationRow, sticky=W)

for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

userTranslitterationEntry.focus()
root.bind("<Return>", check)
getNew()
root.after(1000, speak)
root.mainloop()