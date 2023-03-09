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

def isQuestion(s):
  s = s.lower()
  conditions = ("what", "how", "where", "when", "why", "who", "?")
  for cond in conditions:
    if cond in s:
      return True
  return False

def parseResponse(response):
  if len(response) < 2000:
    return response, ""
  for i in range(len(response)-1,-1,-1):
    if response[i] == " ":
      a,b = response[:i], response[i:]
      if len(b > 0):
        return a,b[1:]
      return a,b
  return response[:2000], response[2000:]