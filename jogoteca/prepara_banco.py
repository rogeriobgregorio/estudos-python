import MySQLdb

print('Conectando...')
conn = MySQLdb.connect(user='root', passwd='admin', host='127.0.0.1', port=3306)
cursor = conn.cursor()

# Verifica e exclui o banco se existir
cursor.execute("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'jogoteca'")
if cursor.fetchone():
    cursor.execute("DROP DATABASE jogoteca;")
    print("Banco de dados 'jogoteca' removido.")

# Criação do banco e tabelas
cursor.execute("CREATE DATABASE jogoteca /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_bin */;")
cursor.execute("USE jogoteca;")
cursor.execute("""
    CREATE TABLE jogo (
        id INT(11) NOT NULL AUTO_INCREMENT,
        nome VARCHAR(50) COLLATE utf8_bin NOT NULL,
        categoria VARCHAR(40) COLLATE utf8_bin NOT NULL,
        console VARCHAR(20) NOT NULL,
        PRIMARY KEY (id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
""")
cursor.execute("""
    CREATE TABLE usuario (
        id VARCHAR(8) COLLATE utf8_bin NOT NULL,
        nome VARCHAR(20) COLLATE utf8_bin NOT NULL,
        senha VARCHAR(8) COLLATE utf8_bin NOT NULL,
        PRIMARY KEY (id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
""")

# Inserção de usuários
usuarios = [
    ('rogerio', 'Rogério Gregório', '1234'),
    ('luan', 'Luan Marques', 'flask'),
    ('nico', 'Nico', '7a1'),
    ('danilo', 'Danilo', 'vegas')
]
cursor.executemany("INSERT INTO usuario (id, nome, senha) VALUES (%s, %s, %s)", usuarios)

# Inserção de jogos
jogos = [
    ('God of War 4', 'Ação', 'PS4'),
    ('NBA 2k18', 'Esporte', 'Xbox One'),
    ('Rayman Legends', 'Indie', 'PS4'),
    ('Super Mario RPG', 'RPG', 'SNES'),
    ('Super Mario Kart', 'Corrida', 'SNES'),
    ('Fire Emblem Echoes', 'Estratégia', '3DS')
]
cursor.executemany("INSERT INTO jogo (nome, categoria, console) VALUES (%s, %s, %s)", jogos)

# Exibição dos dados
cursor.execute("SELECT * FROM usuario")
print(" -------------  Usuários:  -------------")
for user in cursor.fetchall():
    print(user[1])

cursor.execute("SELECT * FROM jogo")
print(" -------------  Jogos:  -------------")
for jogo in cursor.fetchall():
    print(jogo[1])

# Commit e fechamento
conn.commit()
cursor.close()
conn.close()
