import string


def add(x,y):
  return x+y

def subtract(x,y):
  return x-y

def convertWord(word):
  letter_mapping = {}
  letters = list(string.ascii_lowercase)
  for letter in word:
    if letter not in letter_mapping:                
      letter_mapping[letter] = letters[0]
      letters = letters[1:]
  new_word = "".join([letter_mapping[letter] for letter in word])
  return new_word

# takes a list of strings
def checkCode(code):
  newCode = []
  for s in code:
    if "=" in s:
      s = s.split(" ")[0]
      s_declare = "global " + s.strip()
      newCode.append(s_declare + "\n")
  code = "".join(newCode + code)
  return code
      