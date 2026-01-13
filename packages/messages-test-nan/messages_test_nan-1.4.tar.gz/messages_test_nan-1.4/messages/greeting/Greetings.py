import numpy as np

def greeting():
    print('Hi, i greeting from Greetings.greeting() module!.')
    
    
def test():
    print('This is a new test of change in the new version 1.4!.')
    
    
def generar_array(numeros):
    return np.arange(numeros)

class Greeting:
    def __init__(self):
        print('Hola, te saludo desde Greeting.__init__')
    

if __name__ == '__main__':
    # greeting()
    print(generar_array(5))