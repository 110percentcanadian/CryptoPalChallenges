
# main program/script for the cyptopals challenges
#might evolve into a few methods and main or something
import codecs
import numpy as np
import pandas as pd
import bitstring as bitty

def hexString2Base64(wrkStr):
    hexString = wrkStr
    #now decode is in the codecs module, still built in
    BaseNewStr = codecs.encode(hexString)
    print(BaseNewStr)
    deCodeString = codecs.decode(BaseNewStr,'hex_codec')
    Base64Str = codecs.encode(deCodeString,'base64_codec')
    print(deCodeString)
    return Base64Str

def XORsomeHEXES(hexOne,hexTwo):
    decodHexOne = codecs.decode(codecs.encode(hexOne),'hex_codec')
    decodHexTwo = codecs.decode(codecs.encode(hexTwo),'hex_codec')

    print(decodHexOne)
    print(decodHexTwo)
    result=b''
    for by1, by2 in zip(decodHexOne,decodHexTwo):
        result+=(bytes([by1^by2]))

    #result = decodHexOne^decodHexTwo
    print(result)
    result = codecs.encode(result,'hex_codec')
    return result

def SolveChallenge3Pls(HexCode,LetterFreq):
    bigSum = 1000;

    for hexNum in range(0x7F):
        newEnglish=singXorCypher(HexCode,chr(hexNum))
        newSum = EnglishDetector(newEnglish,LetterFreq)
        if newSum<bigSum:
            bigSum=newSum
            bigStr=newEnglish
            theKey=(hexNum)

    return(bigStr,theKey)

def singXorCypher(hexStr,singStr):
    charKey=singStr*(int(len(hexStr)/2))
    cipherText=codecs.decode(codecs.encode(hexStr),'hex_codec')
    charKeyString = codecs.encode(charKey)
    resultingStr=b''
    for cypherByte,keyByte in zip(cipherText,charKeyString):
        resultingStr+=bytes([cypherByte^keyByte])

    return resultingStr



def EnglishDetector(yourEnglish, LetterFreq):
    yourEngFreq = np.zeros(26,dtype=int)
    yourEnglish = str(yourEnglish)
    StrLength = len(yourEnglish)
    for i in range(StrLength): #goes through numbers for length of string
        for j in range(25): #goes through each letter of alphabet
            if LetterFreq.loc[j,'letters'] == str(yourEnglish[i]): #compare each letter
                yourEngFreq[j] +=1
    relFrequency = yourEngFreq/26
    engScore =0
    for i in range(26):
        engScore += abs(relFrequency[i]-LetterFreq.loc[i,'Frequency'])
    if yourEngFreq[23]>2:
        engScore += 500
    return(engScore)

def SolveChallenge4Pls(HexCode,LetterFreq):
    bigSum = 1000;
    bigStr=''
    theKey=0x00
    for hexNum in range(0x7F):
        newEnglish=singXor4Cypher(HexCode,chr(hexNum))
        if len(newEnglish)>20:
            newSum = EnglishDetector4(newEnglish,LetterFreq)
            if newSum<bigSum:
                bigSum=newSum
                bigStr=newEnglish
                theKey=(hexNum)
    return(bigStr,theKey)

def singXor4Cypher(hexStr,singStr):
    charKey=singStr*int(len(hexStr)/2)
    cipherText=codecs.decode(codecs.encode(hexStr),'hex_codec')
    charKeyString = codecs.encode(charKey)
    resultingStr=b''
    for cypherByte,keyByte in zip(cipherText,charKeyString):
        j=int.from_bytes(bytes([cypherByte ^ keyByte]),"big")
        if (j<0x7f) or j==0x20 or j==0x27:
            resultingStr+=bytes([cypherByte^keyByte])
        else:
            return 'nothing here sucka'

    return resultingStr

def EnglishDetector4(yourEnglish, LetterFreq):
    yourEngFreq = np.zeros(26,dtype=int)
    yourEnglish = str(yourEnglish)
    StrLength = len(yourEnglish)
    for i in range(StrLength): #goes through numbers for length of string
        for j in range(25): #goes through each letter of alphabet
            if LetterFreq.loc[j,'letters'] == str(yourEnglish[i]): #compare each letter
                yourEngFreq[j] +=1
    relFrequency = yourEngFreq/26
    engScore =0
    for i in range(26):
        engScore += abs(relFrequency[i]-LetterFreq.loc[i,'Frequency'])
    if yourEngFreq[23]>2:
        engScore += 500
    return(engScore)

def repeatingXORencryption(KEY, text):
    crypt = KEY*int(len(text)/len(KEY))
    for i in range(len(text)-len(crypt)):
        crypt+=KEY[i]
    crypt = codecs.encode(crypt)    #encodes into bytes
    CypherText = codecs.encode(text) #encodes text into bytes
    encodedText=b'' #initialize output bytes
    for CryByt, CipByt in zip(crypt,CypherText): #byte wise compare
        encodedText+= bytes([CryByt^CipByt])
    encodedText=codecs.encode(encodedText,'hex_codec')  #encodes into hex for displaying later
    return encodedText

def repeatingXORDecryption(KEY,text):
    CypherText = codecs.decode(text, 'hex_codec') #passed text is hex encoded from prev, converts out of hex
    crypt = KEY*(int(len(text)/len(KEY)))  #generate crypt string
    for i in range(len(text)-len(crypt)):
        crypt+=KEY[i] #filling out odd numbered key
    crypt = codecs.encode(crypt) #encode keystring to bytes
    encodedText = b''  #initialize result
    for CryByt, CipByt in zip(crypt,CypherText):  #byte wise XOR
        encodedText+= bytes([CryByt^CipByt])
    encodedText=codecs.decode(encodedText)   #decodes into string
    return encodedText

def SolveChallenge6Pls(text):
    CypherText=codecs.decode(codecs.encode(text),'base64_codec')#text hase been "base64's" according to cryptopal loc[0,'cyphers']
    ScoreToBeat = 1000
    KeySize=[0,0,0]
    for i in range(2,40):
        firstKeyString =CypherText[:i]
        secondKeyString =CypherText[i:i*2]
        hammerTime=HammingDistance(firstKeyString,secondKeyString)/i
        if hammerTime<ScoreToBeat:
            ScoreToBeat=hammerTime
            KeySize[2]=KeySize[1]
            KeySize[1]=KeySize[0]
            KeySize[0]=i
    return KeySize

def HammingDistance(StringOne,StringTwo):
    #encode both strings
    if type(StringOne) == str:
        ByteStringOne = codecs.encode(StringOne)
        ByteStringTwo = codecs.encode(StringTwo)
    else:
        ByteStringOne = StringOne
        ByteStringTwo = StringTwo

    bytesTheSame=b''
    for b1,b2 in zip(ByteStringOne,ByteStringTwo):
        bytesTheSame+=bytes([b1^b2])
    #need to count the bits of the result....
    bitDiff = bitty.BitArray(bytesTheSame)
    bitDiff = bitDiff.count(1)
    return bitDiff


if __name__ == '__main__':

    #challenge 1
    # hexString = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
    # Base64newby = hexString2Base64(wrkStr=hexString)
    # print(Base64newby)#the answer to first challenge
    #challenge 2
    # firstHex = "1c0111001f010100061a024b53535009181c"
    # secHex   = "686974207468652062756c6c277320657965"
    # resultHex=XORsomeHEXES(firstHex,secHex)
    # print(resultHex) #answer for challenge 2, encoded in hex

    #Challenge 3 - Single byte XOR ciper
    LetterFreq = pd.read_csv('letterFrequency.csv', names = ["fuckyou","Frequency","empty","letters"], delimiter="," )
    #pls remember 0 indexed arrays like the rest of the owrld
    # encodedHex = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
    # print(codecs.decode(encodedHex,'hex_codec'))
    # decodedMessage,theKey=SolveChallenge3Pls(encodedHex,LetterFreq)
    # print(decodedMessage)
    # print(theKey)

    #challenge 4 - single byte XOR in big ole file
    # cypherFile=pd.read_csv('mysteryText.txt',names=["cyphers"], delimiter=",")
    # singleSolve=np.zeros(326,dtype=bytearray)
    # theKey = np.zeros(326,dtype=str)
    # for i in range(326):
    #     singleSolve[i],theKey[i] =SolveChallenge4Pls(cypherFile.loc[i,'cyphers'],LetterFreq)
    #     print(i)
    # resultFinder = 1000;
    #
    # for i in range(326):
    #     if singleSolve[i]!='':
    #         bigSum = EnglishDetector4(singleSolve[i],LetterFreq)
    #         if resultFinder>bigSum:
    #             resultFinder=bigSum
    #             cipherSolution = singleSolve[i]
    #
    # print(cipherSolution)
    # testing = codecs.decode(codecs.encode(decodedMessage,'hex_codec'))
    # testFrom3 = codecs.encode(decodedMessage,'hex_codec')
    # print(testing)

    #Challenge 5 Repeating XOR implementation leeetsss goooo
    # KEY = 'ICE'
    # cypherText = 'Burning \'em, if you ain\'t quick and nimble\nI go crazy when I hear a cymbal'
    # encryptedPoem = repeatingXORencryption(KEY,cypherText)
    # print(encryptedPoem)
    # workOfArt = repeatingXORDecryption(KEY,encryptedPoem)
    # print(workOfArt)

    #challenge 6, tha big kahuna -differing bits is a XOR
    testStrOne ="this is a test"
    wakaWaka = "wokka wokka!!!"
    HamHam = HammingDistance(testStrOne,wakaWaka)
    #print(HamHam)
    #cypherFile = pd.read_csv('repeatXORCrack.txt', names=["cyphers"], delimiter=",")
    cypherFile = open('repeatXORCrack.txt')
    theMessage=SolveChallenge6Pls(cypherFile.read())
    print(theMessage)