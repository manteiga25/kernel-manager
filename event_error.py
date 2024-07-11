import os

class io_error:

    def __init__(self) -> None:
        try:
            self.error_write = open("register.txt", "w")
        except:
            return 1
    
    def fechar(self):
        self.error_write.close()

    # parametro mensagem contem a mensagem de erro e a excesao o motivo que desencadeou o erro
    def escreve_erro(self, mensagem, excesao):
        print(mensagem + ": " + excesao)
        try:
            self.error_write.write(mensagem + ": " + excesao)
            self.error_write.flush()
        except:
            print("?")

    def le_registro(self):
        conteudo = ""
        error_read = open("register.txt", "r")
        for s in error_read:
            conteudo += s
        return conteudo