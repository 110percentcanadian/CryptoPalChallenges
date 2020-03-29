
# main program/script for the cyptopals challenges
#might evolve into a few methods and main or something
import codecs


def hexString2Base64(wrkStr):
    hexString = wrkStr
    #now decode is in the codecs module, still built in
    BaseNewStr = codecs.encode(hexString)
    deCodeString = codecs.decode(BaseNewStr,'hex_codec')
    Base64Str = codecs.encode(deCodeString,'base64_codec')
    return Base64Str


if __name__ == '__main__':
    hexString = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
    Base64newby = hexString2Base64(wrkStr=hexString)
    print(Base64newby)