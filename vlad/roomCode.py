from random import randint

def codeGen():
    code = ""
    for i in range(4):
        code += chr(randint(97, 122))
        code += chr(randint(49, 57))
        code += chr(randint(65, 90))
    
    return code

