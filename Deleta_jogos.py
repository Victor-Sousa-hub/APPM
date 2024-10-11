import sqlite3

# Conectar ao banco
conn = sqlite3.connect('dados_jogos.db')
cursor = conn.cursor()

# Função para deletar jogos
def deletar_jogo(nome_jogo=None):
    if nome_jogo:
        # Deletar um jogo específico
        cursor.execute('SELECT id FROM jogos WHERE nome = ?', (nome_jogo,))
        jogo = cursor.fetchone()
        
        if jogo:
            jogo_id = jogo[0]
            # Deletar as estatísticas e minutos associados ao jogo
            cursor.execute('DELETE FROM estatisticas WHERE minuto_id IN (SELECT id FROM minutos WHERE jogo_id = ?)', (jogo_id,))
            cursor.execute('DELETE FROM minutos WHERE jogo_id = ?', (jogo_id,))
            cursor.execute('DELETE FROM jogos WHERE id = ?', (jogo_id,))
            print(f"Jogo '{nome_jogo}' e seus dados foram deletados.")
        else:
            print(f"Jogo '{nome_jogo}' não encontrado.")
    
    else:
        # Deletar todos os jogos e informações
        cursor.execute('DELETE FROM estatisticas')
        cursor.execute('DELETE FROM minutos')
        cursor.execute('DELETE FROM jogos')
        print("Todos os jogos e dados foram deletados.")

    conn.commit()

if __name__ == '__main__':
    deletar_jogo()
