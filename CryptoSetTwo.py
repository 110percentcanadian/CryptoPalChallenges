import codecs
import numpy as np
import pandas as pd
import bitstring as bitty
import base64
from Crypto.Cipher import AES
import io
import random


def PKCSnumSevenPAD(PlainText):
    #Pad to even number of blocks
    Blocklength = len(PlainText)
    fillSize = 20-Blocklength%20
    bytechar = [4]*fillSize
    padChar = bytes(bytechar)
    paddedText = PlainText+padChar
    return paddedText

def XORsomeHEXES(hexOne,hexTwo):

    decodHexOne = hexOne
    decodHexTwo = hexTwo
    # print(decodHexOne)
    # print(decodHexTwo)
    result=b''
    for by1, by2 in zip(decodHexOne,decodHexTwo):
        result+=(bytes([by1^by2]))

    #result = decodHexOne^decodHexTwo
    # print(result)
    resultsHex = codecs.encode(result,'hex_codec')
    return result

def CBCdecrypt(key,text, IV):
    # break into chunks and send to the XOR func
    # first XOR key and IV
    ciphKey = AES.new(key, AES.MODE_ECB)
    lastChunk = IV
    output = b''
    chunk=b''

    blockLength =16
    blockSize = 0
    for byte in text:
        if blockSize<blockLength:
            # fuk need the array, the worst
            chunk+=bytes([byte])
            blockSize +=1
        if blockSize==blockLength:
            # first use AES key and chunk?? or xor key and ciphertext, CT becomes IV for next block
            intResult=ciphKey.decrypt(chunk)
            # then IV or last chunk by results
            output +=XORsomeHEXES(intResult, lastChunk)
            lastChunk = chunk
            chunk = b''
            blockSize=0

    return output

def CBCencrypt(key,plaintext, IV):
    # break into chunks and send to the XOR func
    # first XOR key and IV
    # TODO: change this to encrypt
    ciphKey = AES.new(key, AES.MODE_ECB)
    lastChunk = IV
    output = b''
    chunk=b''

    blockLength =16
    blockSize = 0
    for byte in plaintext:
        if blockSize<blockLength:
            # fuk need the array, the worst
            chunk+=bytes([byte])
            blockSize +=1
        if blockSize==blockLength:
            # first use AES key and chunk?? or xor key and ciphertext, CT becomes IV for next block
            intResult= XORsomeHEXES(chunk, lastChunk)
            lastChunk = ciphKey.encrypt(intResult)
            output +=lastChunk
            # then IV or last chunk by results
            chunk = b''
            blockSize=0

    return output

def ECBdecrypt(key,text):
    # takes two bytes objects, one key and one cipherText
    NewCypher = AES.new(key, AES.MODE_ECB)
    return NewCypher.decrypt(text)

def ECBencrypt(key,plaintext):
    # takes two bytes objects, one key and one cipherText
    #if needed, pad to even multiple of 16b
    paddedText = plaintext
    Blocklength = len(plaintext)
    if (16 - Blocklength % 16>0):
        fillSize = 16 - Blocklength % 16
        bytechar = [4] * fillSize
        padChar = bytes(bytechar)
        paddedText = plaintext + padChar
    NewCypher = AES.new(key, AES.MODE_ECB)
    return NewCypher.encrypt(paddedText)

def randomPad(plainText):
    preBytes = 5+round(random.uniform(0,5))
    postBytes = 5+round(random.uniform(0,5))
    prePad=b''
    postPad=b''
    for i in range(preBytes):
        prePad += bytes([round(random.uniform(0,63))])
    for i in range(postBytes):
        postPad += bytes([round(random.uniform(0,63))])
    paddedPlainText = prePad+plainText+postPad
    return paddedPlainText

def randomBytes(keyLength):
    newKey=b''
    for i in range(keyLength):
        newKey+= bytes([round(random.uniform(0, 63))])
    return newKey

def encryptionModeOracle(cypherText):
    #how to detect encryption Mode?
    repeatcounter = 0
    blockLength = 3

    for i in range(len(cypherText)):
        chunk = cypherText[i:i+blockLength]
        for k in range(len(cypherText)):
            if k !=i:
                subBytes = cypherText[k:k+blockLength]
                if chunk ==subBytes:
                    repeatcounter+=1
        if repeatcounter>5:
            break
    CypherCode = 0
    mode = ' CBC'
    # noise seems to be ~2 repeats, 5 to be safe, not full count to save time
    if repeatcounter >5:
        CypherCode =1
        mode = 'ECB'
    return 'Oracle Says Encryption Mode is: '+ mode, repeatcounter, CypherCode

def bufferEncryptECB(buff, plaintext, ):
    # takes buff, joins with plainText, encrypts under ECB
    # assume all bytes objects
    paddedText = plaintext
    Blocklength = len(plaintext)
    if (16 - Blocklength % 16>0):
        fillSize = 16 - Blocklength % 16
        bytechar = [4] * fillSize
        padChar = bytes(bytechar)
        paddedText = plaintext + padChar
    NewCypher = AES.new(key, AES.MODE_ECB)

    return NewCypher

if __name__ == '__main__':
    #csvImport some letters
    #LetterFreq = pd.read_csv('letterFrequency.csv', names = ["fuckyou","Frequency","empty","letters"], delimiter="," )

    #set 2 challenge 1
    unevenBlock = "YELLOW SUBMARINE"
    unevenBlock = codecs.encode(unevenBlock) #encodes to bytes object
    paddedBlock = PKCSnumSevenPAD(unevenBlock)
    print(paddedBlock)

    # backtrack, set 1 challenge 7, AES in ECB mode
    glkey = b'YELLOW SUBMARINE'
    # cipher = io.open('Set1Ch7.txt','rb').read()
    # cipherText = base64.b64decode(cipher)

    # previous solution below - turns out I wasnt being a dummy, have to do this with pycryptoDome??
    # NewCypher = AES.new(key, AES.MODE_ECB)
    # PlainText = NewCypher.decrypt(cipherText)

    # Set 2 Challenge 2 - CBC Mode
    cipher = io.open('set2challenge2.txt', 'rb').read()
    cipherText = base64.b64decode(cipher)
    IVgl = b'\x00'*16
    keyFile =io.open('secretRandomKey.txt','wb')
    keyFile.write(randomBytes(16))
    keyFile.close()

    # plainText = CBCdecrypt(key, cipherText, IV)

    # Set 2 Challenge 11 - ECB/CBC detection oracle
    # first testing that encrypt and decrypt are working properly for both modes...
    # plainSecret = io.open('plaintext-Sample.txt','rb').read()
    # cypherText = ECBencrypt(glkey,plainSecret)
    # plainText = ECBdecrypt(glkey,cypherText)

    # cypherCBC =CBCencrypt(glkey,plainSecret,IVgl)
    # plainCBC = CBCdecrypt(glkey,cypherCBC,IVgl)

    # 10 samples for the oracle to try
    # for i in range(10):
    #     modeSelect = random.randint(0,1)
    #     # now randomly pad with 5-10 bytes
    #     randomPaddedSecret = randomPad(plainSecret)
    #     # create random key
    #     randomKey = randomBytes(16)
    #     randomIV = randomBytes(16)
    #     mysteryCypher =b''
    #     if modeSelect ==0:
    #         # do CBC Mode
    #         mysteryCypher = CBCencrypt(randomKey,randomPaddedSecret,randomIV)
    #         print('cypher is in CBC Mode')
    #     if modeSelect ==1:
    #         # do ECB mode
    #         mysteryCypher = ECBencrypt(randomKey,randomPaddedSecret)
    #         print('cypher is in ECB Mode')
    #     text, results, unitCode = encryptionModeOracle(mysteryCypher)
    #     print(text+' with '+str(results)+' repetitions')
    #     if unitCode == modeSelect:
    #         print('Oracle Correct!!')

    # Set 2 Challenge 12
    unknownKey = io.open('secretRandomKey.txt','rb').read()



    debug = 5
    # test output
    keyFile =io.open('plaintext.txt','wb')
    # keyFile.write(plainCBC)
    keyFile.close()
    debug = 6