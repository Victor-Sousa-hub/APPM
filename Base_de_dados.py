import sqlite3

# Conectar ao banco
conn = sqlite3.connect('dados_jogos.db')
cursor = conn.cursor()

# Criar tabelas
cursor.execute('''
CREATE TABLE IF NOT EXISTS jogos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS minutos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    jogo_id INTEGER,
    minuto INTEGER,
    FOREIGN KEY (jogo_id) REFERENCES jogos(id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS estatisticas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    minuto_id INTEGER,
    escanteios_time_a TEXT,
    escanteios_time_b TEXT,
    APPM REAL,
    pressao REAL,
    FOREIGN KEY (minuto_id) REFERENCES minutos(id)
)
''')

# Exemplo: Inserir dados de um jogo

def busca_dados_jogo(nome_jogo):
    cursor.execute('''
    SELECT minutos.minuto, estatisticas.escanteios_time_a, estatisticas.escanteios_time_b, estatisticas.APPM, estatisticas.pressao 
    FROM jogos 
    JOIN minutos ON jogos.id = minutos.jogo_id 
    JOIN estatisticas ON minutos.id = estatisticas.minuto_id
    WHERE jogos.nome = ?
    ''', (nome_jogo,))
    
    return cursor.fetchall()


conn.close()