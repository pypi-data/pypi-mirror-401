import numpy as np

def greeting():
    print('Hi, i grreting from Greetings.greeting() module!.')
    
    
def test():
    print('This is a test of change in hte new version!.')
    
    
def generar_array(numeros):
    return np.arange(numeros)

class Greeting:
    def __init__(self):
        print('Hola, te saludo desde Greeting.__init__')
    

if __name__ == '__main__':
    # greeting()
    print(generar_array(5))