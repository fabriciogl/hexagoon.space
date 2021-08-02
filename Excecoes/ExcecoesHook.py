import sys

#TODO fazer com que as exceções passem por aqui e retornem uma messagem de erro
#TODO para o usuario
#TODO outra possibilidade é usar o pacote returns com o decorator @safe
#TODO parecido com o safe do R
def except_hook(excecao, value, traceback):
    return {type(excecao).__name__: value}

sys.excepthook = except_hook