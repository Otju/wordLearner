from re import S
import pyttsx3
import json
from random import randrange
import re 

def has_cyrillic(text):
    return bool(re.search('[ЁёА-я]', text))
    
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

tranlitterationDictionary = {"а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "jo", "ж": "zh", "з": "z", "и": "i", "й": "j", "к": "k", "л": "l", "м": "m", "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u", "ф": "f", "х": "h", "ц": "ts", "ч": "tsh","ш": "sh", "щ": "shtsh", "ъ": "", "ы": "y", "ь": "", "э": "e", "ю": "ju", "я": "ja"}

def translitterate(text):
    translitteratedText = ""
    for i in range(0, len(text)):
        character = text[i]
        isUpper = character.isupper()
        character = character.lower()
        newCharacter = ""
        if(i == 0 and character == "е"):
            newCharacter = "je"
        elif(has_cyrillic(character)):
            newCharacter =  tranlitterationDictionary[character]
        else:
            newCharacter = character
        translitteratedText += newCharacter.upper() if isUpper else newCharacter
    return translitteratedText

engine = pyttsx3.init()
voices = engine.getProperty('voices')
hasRUS = False
for voice in voices:
    if(voice.name.find("Russia") != -1):
        engine.setProperty('voice', voice.id)
        hasRUS = True
        break
dictionaryFile = open("dictionary.json", encoding="utf-8")
dictionary = json.load(dictionaryFile)
if(not hasRUS):
    print("No Russian TTS found")

def speak(word):
    engine.say(word)
    engine.runAndWait()

def setReadSpeed(speed):
    engine.setProperty('rate', speed) 

goneTroughWords = []
def getWord(wordPacketNames, disableMultiWord, disableOver10Letters, rightWords, currentWordNumber):
    rawDictList = []
    for name in wordPacketNames:
        rawDictList.extend(list(dictionary[name].items()))
    dictList = []
    for value in rawDictList:
        word = value[1]
        allow = True
        if(disableOver10Letters and len(word) > 10):
            allow = False
        if(disableMultiWord and " " in word):
            allow = False
        if(allow):
            dictList.append(value)
    countOfRightWordsInDictList = 0
    def isNotInList(var, list):
        if(var[1] not in list):
            return True
        return False
    def isNotInRightWords(var):
        return isNotInList(var, rightWords)
    def isNotInGoneTroughWords(var):
        return isNotInList(var, goneTroughWords)
    for var in dictList:
        if(not isNotInRightWords(var)):
            countOfRightWordsInDictList += 1
    currentMaxIndex = countOfRightWordsInDictList + 15
    fullDictListLength = len(dictList)
    dictList = dictList[0:currentMaxIndex]
    dictList = list(filter(isNotInRightWords, dictList))
    dictListLength = len(dictList)
    if(currentWordNumber>=dictListLength):
        goneTroughWords.clear()
    filteredDictList = list(filter(isNotInGoneTroughWords, dictList))
    if(len(filteredDictList) == 0):
        goneTroughWords.clear()
    else:
        dictList = filteredDictList
    randomWordIndex = randrange(len(dictList))
    randomWordAndTranslation = dictList[randomWordIndex]
    word  = randomWordAndTranslation[1]
    goneTroughWords.append(word)
    translation = randomWordAndTranslation[0]
    translitteration = translitterate(word)
    return [word, translation, translitteration, dictListLength, fullDictListLength]
