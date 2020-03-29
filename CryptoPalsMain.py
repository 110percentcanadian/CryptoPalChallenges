
# main program/script for the cyptopals challenges
#might evolve into a few methods and main or something
import codecs


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


if __name__ == '__main__':

    #challenge 1
    hexString = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
    Base64newby = hexString2Base64(wrkStr=hexString)
    print(Base64newby)#the answer to first challenge
    #challenge 2
    firstHex = "1c0111001f010100061a024b53535009181c"
    secHex   = "686974207468652062756c6c277320657965"
    resultHex=XORsomeHEXES(firstHex,secHex)
    print(resultHex)#answer for challenge 2, encoded in hex