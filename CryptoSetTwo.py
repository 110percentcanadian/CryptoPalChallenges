import codecs
import numpy as np
import pandas as pd
import bitstring as bitty

def PKCSnumSevenPAD(PlainText):
    #Pad to even number of blocks
    Blocklength = len(PlainText)
    fillSize = 20-Blocklength%20
    bytechar = [4]*fillSize
    padChar = bytes(bytechar)
    paddedText = PlainText+padChar
    return paddedText

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

if __name__ == '__main__':
    #csvImport some letters
    LetterFreq = pd.read_csv('letterFrequency.csv', names = ["fuckyou","Frequency","empty","letters"], delimiter="," )

    #set 2 challenge 1
    unevenBlock = "YELLOW SUBMARINE"
    unevenBlock = codecs.encode(unevenBlock) #encodes to bytes object
    paddedBlock = PKCSnumSevenPAD(unevenBlock)
    print(paddedBlock)
