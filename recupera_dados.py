
def estrutura_dados(eventos,time_a,time_b,APPM,tempo):
    import re

    lance = []
    for evento in eventos:
        lance.append(evento.split('\n'))
    lance_filtrada = [sublista for sublista in lance if len(sublista) > 1]
    # Inicializa o dicionário para armazenar os dados de ambos os times
    jogo = {}
    jogo[tempo] =  dados_da_partida = {
        f"escanteios_{time_a}": [],
        f"escanteios_{time_b}": [],
        'pressão' : (APPM/tempo) * 100,
        'APPM' : APPM * 100
    }
    # Processar os pares
    for primeiro, segundo in lance_filtrada:
        # Identificar se é um escanteio ou um lance irrelevante
        is_primeiro_escanteio = "Corner" in primeiro
        is_segundo_escanteio = "Corner" in segundo

        # Se o primeiro é um escanteio e o segundo é um tempo, pertence ao Time A
        if is_primeiro_escanteio and re.search(r"\d+'", segundo):
            minuto = int(re.findall(r"\d+", segundo)[0])  # Captura o minuto
            dados_da_partida[f"escanteios_{time_a}"].append(minuto)

        # Se o primeiro é um tempo e o segundo é um escanteio, pertence ao Time B
        elif re.search(r"\d+'", primeiro) and is_segundo_escanteio:
            minuto = int(re.findall(r"\d+", primeiro)[0])  # Captura o minuto
            dados_da_partida[f"escanteios_{time_b}"].append(minuto)

    # Resultado final
    return jogo



def recupera_dados():
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    import time
    import re
    from bs4 import BeautifulSoup

    # Configurando opções para o Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ativar modo headless
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")  # Para evitar problemas de memória

    # Inicializa o driver
    driver = webdriver.Chrome(options=chrome_options)
    #driver = webdriver.Chrome()


    driver.get('https://sokkerpro.com')


    #Seleciona a aba de jogos ao vivo
    try:
        elemento = driver.find_element(By.CLASS_NAME, "totalmenuLine")
        filhos = elemento.find_elements(By.XPATH, "./*")
        filhos[1].click()
    except():
        recupera_dados()

    #Seleiona os jogos ao vivo
    games_lists = driver.find_elements(By.CLASS_NAME,'match')

    for game in games_lists:
        #driver.execute_script("arguments[0].setAttribute('target', '_self');", game)
        game.click()
    all_windows = driver.window_handles[1:]

    dados = {}
    for window in all_windows:
        #Recupera os escanteios
        driver.switch_to.window(window)
        elementos = driver.find_elements(By.CLASS_NAME,'event')[:-1]
        times = driver.find_elements(By.CLASS_NAME,'team')
        times_a_b = []

        for Time in times:
            times_a_b.append(Time.text)

        try:
          time_a = times_a_b[0].split('\n')[1]
          time_b = times_a_b[1].split('\n')[1]
        except:
            pass

        eventos = []
        for elemento in elementos:
            eventos.append(elemento.text)

        #Recuper APPM
        try:
            driver.execute_script("var elementos = document.getElementsByClassName('clever-core-ads'); while (elementos.length > 0) { elementos[0].parentNode.removeChild(elementos[0]); }")
            statistc = driver.find_element(By.XPATH,"//*[contains(@class, 'menuitem') and contains(text(), 'STATISTICS')]")
            statistc.click()
        except:
            recupera_dados()
        try:
            div_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'top')]//span[text()='Dangerous attacks per minute']"))
            )
            div_pai = div_element.find_element(By.XPATH, "..")
            dadosAPPM = div_pai.text.split('\n')
            APPM_sum = float(dadosAPPM[0]) + float(dadosAPPM[2])
        except:
            APPM_sum = 0

        try:
            tempo = int(driver.find_element(By.CLASS_NAME,"status").text[:2])
            dados[f'{time_a} x {time_b}'] = (estrutura_dados(eventos,time_b,time_a,APPM_sum,tempo))
        except:
            pass


    return dados



def atualizar_dados_jogos(dados_novos):
    import sqlite3
    conn = sqlite3.connect('dados_jogos.db')
    cursor = conn.cursor()
    def insere_jogo(nome):
        cursor.execute('INSERT INTO jogos (nome) VALUES (?)', (nome,))
        return cursor.lastrowid  # Retorna o ID do jogo inserido

    def insere_minuto(jogo_id, minuto):
        cursor.execute('INSERT INTO minutos (jogo_id, minuto) VALUES (?, ?)', (jogo_id, minuto))
        return cursor.lastrowid  # Retorna o ID do minuto inserido

    def insere_estatisticas(minuto_id, escanteios_time_a, escanteios_time_b, APPM, pressao):
        cursor.execute('''
        INSERT INTO estatisticas (minuto_id, escanteios_time_a, escanteios_time_b, APPM, pressao) 
        VALUES (?, ?, ?, ?, ?)
        ''', (minuto_id, str(escanteios_time_a), str(escanteios_time_b), APPM, pressao))
        conn.commit()  # Salvar as alterações
    # Inserir os dados no banco de dados
    for jogo, minutos in dados_novos.items():
        jogo_id = insere_jogo(jogo)  # Inserir jogo
        time_a = jogo.split('x')[0][:-1]
        time_b = jogo.split('x')[1][1:]
        for minuto, stats in minutos.items():
            minuto_id = insere_minuto(jogo_id, minuto)  # Inserir minuto
            # Inserir estatísticas
            print(stats[f'escanteios_{time_a}'])
            print(stats[f'escanteios_{time_b}'])
            insere_estatisticas(minuto_id, 
                                stats.get(f'escanteios_{time_a}', []), 
                                stats.get(f'escanteios_{time_b}', []), 
                                stats['APPM'], 
                                stats['pressão'])
        print(f'Dados do minuto: {minuto} do jogo: {jogo} Salvos com sucesso')
    print('--------------------------------------------------------------')

    


if __name__ == '__main__':
    print('Iniciando Scraping')
    while True:
        atualizar_dados_jogos(recupera_dados())