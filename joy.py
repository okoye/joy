'''
My Zoe time-capsule.

@description:   Allows you to get/send messages from/to the future today.
                To successfully unscramble messages. You will need to deduce the passphrase.
                Herein lies the challenge.

@author:        Chuka
'''
import math
from base64 import b64encode, b64decode
from os import environ
from Crypto.Cipher import DES


def scramble(message, passphrase):
  '''
  apply DES
  '''
  remainder = int((math.ceil(len(message)/8.0) * 8) - len(message))
  for i in xrange(remainder):
    message += 'X' #pesky padding requirement
  des = DES.new(passphrase, DES.MODE_ECB)
  cipher = des.encrypt(message)
  return b64encode(cipher)


def unscramble(cipher, passphrase):
  '''
  decode DES
  '''
  cipher = b64decode(cipher)
  des = DES.new(passphrase, DES.MODE_ECB)
  message = des.decrypt(cipher)
  message = message.strip('X')#remove pesky padding also
  return message

def test_passphrase(passphrase):
  '''
  a quick test to see if passphrase is correct
  '''
  if len(passphrase) == 8: #CLUE: got to be 8 characters in length!
    return True
  else:
    return False

def start():
  while True:
    passphrase = environ.get('ZOE_PASSPHRASE', None)
    if not passphrase:
      passphrase = raw_input('type passphrase and press enter: ')
      passphrase = passphrase.strip()
      if not test_passphrase(passphrase):
        print 'incorrect passphrase.'
        continue

    purpose = raw_input('enter 1 to scramble message or 0 to unscramble messages: ')
    purpose = purpose.strip()
    try:
      assert purpose == '1' or purpose == '0'
    except AssertionError:
      purpose = 0 #assume you are going to unscramble messages by default

    if purpose == '1':
      message = raw_input('type your message and press enter: ')
      cipher = scramble(message, passphrase)
      print "here is your scrambled message: ", cipher
    else:
      cipher = raw_input('type the scrambled text from the future: ')
      message = unscramble(cipher, passphrase)
      print "here is your unscrambled message: ", message

    action = raw_input("type anything to exit otherwise press enter to continue: ")
    if action:
      break


if __name__ == '__main__':
  start() #whoopee, powering up time-machine!
  print "roses are red, violets are blue, these ciphers will never be rued"
