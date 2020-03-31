
# main program/script for the cyptopals challenges
#might evolve into a few methods and main or something
import codecs
import numpy as np
import pandas as pd

def hexString2Base64(wrkStr):
    hexString = wrkStr
    #now decode is in the codecs module, still built in
    BaseNewStr = codecs.encode(hexString)
    deCodeString = codecs.decode(BaseNewStr,'hex_codec')
    Base64Str = codecs.encode(deCodeString,'base64_codec')
    print(deCodeString)
    return Base64Str

def XORsomeHEXES(hexOne,hexTwo):
    decodHexOne = codecs.decode(codecs.encode(hexOne),'hex_codec')
    decodHexTwo = codecs.decode(codecs.encode(hexTwo),'hex_codec')
    codecs.encode(hexTwo)
    print(decodHexOne)
    print(decodHexTwo)
    result=b''
    for by1, by2 in zip(decodHexOne,decodHexTwo):
        result+=(bytes([by1^by2]))

    #result = decodHexOne^decodHexTwo
    print(result)
    result = codecs.encode(result,'hex_codec')
    return result

def singXorCypher(hexStr,singStr):
    charKey=singStr
    p=int(len(hexStr)/2)
    charKey=''
    for i in range(p):
        charKey += singStr
    #can just use singStr*p for the above code, python str be like that
    # print(charKey)
    cipherText=codecs.decode(codecs.encode(hexStr),'hex_codec')
    charKeyString=codecs.encode(codecs.encode(charKey),'hex_codec')
    resultingStr=b''
    # print(cipherText)
    for byt,charKeyF in zip(cipherText,charKeyString):
        resultingStr+=bytes([(byt)^charKeyF])
    # print(resultingStr)
    english =codecs.encode(resultingStr, 'hex_codec')


    return resultingStr


def EnglishDetector(yourEnglish, LetterFreq):
    yourEngFreq = np.zeros(26,dtype=int)
    yourEnglish = str(yourEnglish)
    StrLength = len(yourEnglish)
    for i in range(StrLength): #goes through numbers for length of string
        for j in range(25): #goes through each letter of alphabet
            k=LetterFreq.loc[j,'letters']
            if k == str(yourEnglish[i]): #compare each letter
                yourEngFreq[j] +=1
    print(yourEnglish)
    print(yourEngFreq)
    fullSum=yourEngFreq.sum()-yourEngFreq[23]
    return(fullSum)




def SolveChallenge3Pls(HexCode,LetterFreq):
    bigSum = 0;
    for hexNum in range(0xFF):
        print(chr(hexNum))
        #charKey = b''+str(hex(hexNum))
        newEnglish=singXorCypher(HexCode,chr(hexNum))
        newSum = EnglishDetector(newEnglish,LetterFreq)
        if newSum>bigSum:
            bigSum=newSum
            bigStr=newEnglish

    return(bigStr)

if __name__ == '__main__':

    #challenge 1
    hexString = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
    Base64newby = hexString2Base64(wrkStr=hexString)
    print(Base64newby)#the answer to first challenge
    #challenge 2
    firstHex = "1c0111001f010100061a024b53535009181c"
    secHex   = "686974207468652062756c6c277320657965"
    resultHex=XORsomeHEXES(firstHex,secHex)
    print(resultHex) #answer for challenge 2, encoded in hex

    #Challenge 3 - Single byte XOR ciper
    LetterFreq = pd.read_csv('letterFrequency.csv', names = ["fuckyou","Frequency","empty","letters"], delimiter="," )

    print((LetterFreq.loc[0,'letters']))

    #pls remember 0 indexed arrays like the rest of the owrld
    encodedHex = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
    decodedMessage=SolveChallenge3Pls(encodedHex,LetterFreq)
    singleString=str(LetterFreq.loc[0,'letters'])
    singlenoquoteString=str(LetterFreq.loc[0,'fuckyou'])
    # print((LetterFreq.loc[0,'letters']))
    # stringer=str('a')
    # if LetterFreq.loc[0,'letters'] == stringer:
    #     print('itworks!')
    print('\n')
    print(decodedMessage)
