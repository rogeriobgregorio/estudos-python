class Jogo:
    def __init__(self, nome, categoria, console, id=None):
        self.id = id
        self.nome = nome
        self.categoria = categoria
        self.console = console
    
    # Métodos get e set
    def get_nome(self):
        return self.nome
    
    def set_nome(self, nome):
        self.nome = nome
    
    def get_categoria(self):
        return self.categoria
    
    def set_categoria(self, categoria):
        self.categoria = categoria
    
    def get_console(self):
        return self.console
    
    def set_console(self, console):
        self.console = console
    
    def __str__(self):
        return f"Jogo(nome={self.nome}, categoria={self.categoria}, console={self.console})"


class Usuario:
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha
    
    # Métodos get e set
    def get_id(self):
        return self.id
    
    def set_id(self, id):
        self.id = id
    
    def get_nome(self):
        return self.nome
    
    def set_nome(self, nome):
        self.nome = nome
    
    def get_senha(self):
        return self.senha
    
    def set_senha(self, senha):
        self.senha = senha

    def __str__(self):
        return f"Usuario(id={self.id}, nome={self.nome}, senha={self.senha})"