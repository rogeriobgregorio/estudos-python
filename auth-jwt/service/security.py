from werkzeug.security import generate_password_hash, check_password_hash

# Função para gerar o hash da senha
def hash_password(password: str) -> str:
    """
    Recebe uma senha e retorna o seu hash.
    """
    return generate_password_hash(password)

# Função para verificar se a senha fornecida corresponde ao hash armazenado
def check_password(stored_password: str, provided_password: str) -> bool:
    """
    Compara a senha fornecida com a senha armazenada.
    Retorna True se as senhas corresponderem, caso contrário, False.
    """
    return check_password_hash(stored_password, provided_password)
