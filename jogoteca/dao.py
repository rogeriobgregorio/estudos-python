from models import Jogo, Usuario
import logging

# Configuração de logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# SQL Queries
SQL_DELETA_JOGO = 'DELETE FROM jogo WHERE id = %s'
SQL_JOGO_POR_ID = 'SELECT id, nome, categoria, console FROM jogo WHERE id = %s'
SQL_USUARIO_POR_ID = 'SELECT id, nome, senha FROM usuario WHERE id = %s'
SQL_ATUALIZA_JOGO = 'UPDATE jogo SET nome = %s, categoria = %s, console = %s WHERE id = %s'
SQL_BUSCA_JOGOS = 'SELECT id, nome, categoria, console FROM jogo'
SQL_CRIA_JOGO = 'INSERT INTO jogo (nome, categoria, console) VALUES (%s, %s, %s)'


class JogoDao:
    def __init__(self, db):
        """
        Classe para gerenciar operações no banco de dados relacionadas a jogos.

        Args:
            db: Objeto de conexão ao banco de dados.
        """
        self.__db = db

    def salvar(self, jogo):
        """
        Salva ou atualiza um jogo no banco de dados.

        Args:
            jogo (Jogo): O objeto Jogo a ser salvo.

        Returns:
            Jogo: O objeto Jogo salvo, com o ID atualizado (se aplicável).
        """
        try:
            cursor = self.__db.connection.cursor()
            if jogo.id:
                logger.info("Atualizando jogo com ID: %s", jogo.id)
                cursor.execute(SQL_ATUALIZA_JOGO, (jogo.nome, jogo.categoria, jogo.console, jogo.id))
            else:
                logger.info("Inserindo novo jogo.")
                cursor.execute(SQL_CRIA_JOGO, (jogo.nome, jogo.categoria, jogo.console))
                jogo.id = cursor.lastrowid
            self.__db.connection.commit()
            return jogo
        except Exception as e:
            logger.error("Erro ao salvar jogo: %s", e)
            self.__db.connection.rollback()
            raise

    def listar(self):
        """
        Lista todos os jogos do banco de dados.

        Returns:
            list: Lista de objetos Jogo.
        """
        try:
            cursor = self.__db.connection.cursor()
            cursor.execute(SQL_BUSCA_JOGOS)
            jogos = traduz_jogos(cursor.fetchall())
            return jogos
        except Exception as e:
            logger.error("Erro ao listar jogos: %s", e)
            raise

    def busca_por_id(self, id):
        """
        Busca um jogo pelo ID.

        Args:
            id (int): ID do jogo.

        Returns:
            Jogo: Objeto Jogo correspondente ao ID, ou None se não encontrado.
        """
        try:
            cursor = self.__db.connection.cursor()
            cursor.execute(SQL_JOGO_POR_ID, (id,))
            tupla = cursor.fetchone()
            if tupla:
                return Jogo(tupla[1], tupla[2], tupla[3], id=tupla[0])
            return None
        except Exception as e:
            logger.error("Erro ao buscar jogo por ID: %s", e)
            raise

    def deletar(self, id):
        """
        Deleta um jogo pelo ID.

        Args:
            id (int): ID do jogo a ser deletado.
        """
        try:
            logger.info("Deletando jogo com ID: %s", id)
            self.__db.connection.cursor().execute(SQL_DELETA_JOGO, (id,))
            self.__db.connection.commit()
        except Exception as e:
            logger.error("Erro ao deletar jogo: %s", e)
            self.__db.connection.rollback()
            raise


class UsuarioDao:
    def __init__(self, db):
        """
        Classe para gerenciar operações no banco de dados relacionadas a usuários.

        Args:
            db: Objeto de conexão ao banco de dados.
        """
        self.__db = db

    def buscar_por_id(self, id):
        """
        Busca um usuário pelo ID.

        Args:
            id (str): ID do usuário.

        Returns:
            Usuario: Objeto Usuario correspondente ao ID, ou None se não encontrado.
        """
        try:
            cursor = self.__db.connection.cursor()
            cursor.execute(SQL_USUARIO_POR_ID, (id,))
            dados = cursor.fetchone()
            return traduz_usuario(dados) if dados else None
        except Exception as e:
            logger.error("Erro ao buscar usuário por ID: %s", e)
            raise


def traduz_jogos(jogos):
    """
    Converte uma lista de tuplas do banco de dados em objetos Jogo.

    Args:
        jogos (list): Lista de tuplas retornadas do banco.

    Returns:
        list: Lista de objetos Jogo.
    """
    def cria_jogo_com_tupla(tupla):
        return Jogo(tupla[1], tupla[2], tupla[3], id=tupla[0])

    return list(map(cria_jogo_com_tupla, jogos))


def traduz_usuario(tupla):
    """
    Converte uma tupla do banco de dados em um objeto Usuario.

    Args:
        tupla (tuple): Tupla retornada do banco.

    Returns:
        Usuario: Objeto Usuario.
    """
    return Usuario(tupla[0], tupla[1], tupla[2])
