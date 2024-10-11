from flask import Flask, render_template, jsonify, request
import plotly.graph_objs as go
import sqlite3

app = Flask(__name__)

# Função que busca os dados da base de dados para o jogo selecionado
def generate_data(jogo_selecionado):
    conn = sqlite3.connect('dados_jogos.db')
    cursor = conn.cursor()

    # Buscar os minutos, APPM e escanteios do jogo selecionado
    cursor.execute('''
        SELECT minutos.minuto, estatisticas.APPM, estatisticas.escanteios_time_a, estatisticas.escanteios_time_b,estatisticas.pressao
        FROM estatisticas 
        JOIN minutos ON estatisticas.minuto_id = minutos.id
        JOIN jogos ON minutos.jogo_id = jogos.id
        WHERE jogos.nome = ?
        ORDER BY minutos.minuto
    ''', (jogo_selecionado,))
    
    dados = cursor.fetchall()
    conn.close()

    if dados:
        minutos, appm, escanteios_a_str, escanteios_b_str,pressao = zip(*dados)

        # Tratamento para converter escanteios de string para lista
        escanteios_a = []
        for escanteios in escanteios_a_str:
            if escanteios:  # Verifica se a string não está vazia
                try:
                    escanteios_a.append(list(map(int, escanteios.strip('[]').split(','))))
                except ValueError:
                    escanteios_a.append([])  # Adiciona uma lista vazia em caso de erro
            else:
                escanteios_a.append([])  # Adiciona uma lista vazia se não houver escanteios

        escanteios_b = []
        for escanteios in escanteios_b_str:
            if escanteios:  # Verifica se a string não está vazia
                try:
                    escanteios_b.append(list(map(int, escanteios.strip('[]').split(','))))
                except ValueError:
                    escanteios_b.append([])  # Adiciona uma lista vazia em caso de erro
            else:
                escanteios_b.append([])  # Adiciona uma lista vazia se não houver escanteios
        
        return list(minutos), list(appm), escanteios_a, escanteios_b,pressao
    else:
        return [], [], [], [],[]

# Página principal que carrega o gráfico e widget
@app.route('/')
def index():
    # Buscar apenas os nomes dos jogos
    conn = sqlite3.connect('dados_jogos.db')
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT nome FROM jogos')
    jogos = [jogo[0] for jogo in cursor.fetchall()]
    conn.close()

    return render_template('index.html', jogos=jogos)

# Rota que retorna os dados atualizados do gráfico
@app.route('/update_data', methods=['GET'])
def update_data():
    # Recupera o jogo selecionado na requisição
    jogo_selecionado = request.args.get('jogo')
    print(jogo_selecionado)
    time_a = jogo_selecionado.split('x')[0]
    time_b = jogo_selecionado.split('x')[1]
    # Gera os dados a partir da base de dados
    minutos, data, escanteios_a, escanteios_b, pressao = generate_data(jogo_selecionado)

    # Cria o gráfico usando Plotly
    fig = go.Figure()

    # Plotando a linha do APPM
    fig.add_trace(go.Scatter(
        x=minutos,
        y=data,
        fill='tozeroy',
        fillcolor='rgba(0, 255, 0, 0.2)',
        line=dict(color='green'),
        mode='lines',
        name='APPM'
    ))

     # Adicionando escanteios do Time A como pontos azuis
    pontos_escanteios_a = []
    for escanteio_time_a in escanteios_a:
        pontos_escanteios_a.extend(escanteio_time_a)  # Adiciona todos os escanteios à lista

    # Adicionando os pontos de escanteio do Time A ao gráfico
    if pontos_escanteios_a:  # Verifica se há escanteios
        fig.add_trace(go.Scatter(
            x=pontos_escanteios_a,
            y=[data[minutos.index(minuto)] if minuto in minutos else 70 for minuto in pontos_escanteios_a],
            mode='markers',
            marker=dict(color='blue', size=10),
            name=f'Escanteios {time_a}',  # Nome definido aqui para aparecer apenas uma vez
            showlegend=True
        ))

    # Adicionando escanteios do Time B como pontos vermelhos
    pontos_escanteios_b = []
    for escanteio_time_b in escanteios_b:
        pontos_escanteios_b.extend(escanteio_time_b)  # Adiciona todos os escanteios à lista

    # Adicionando os pontos de escanteio do Time B ao gráfico
    if pontos_escanteios_b:  # Verifica se há escanteios
        fig.add_trace(go.Scatter(
            x=pontos_escanteios_b,
            y=[data[minutos.index(minuto)] if minuto in minutos else 70 for minuto in pontos_escanteios_b],
            mode='markers',
            marker=dict(color='red', size=10),
            name=f'Escanteios {time_b}',  # Nome definido aqui para aparecer apenas uma vez
            showlegend=True
        ))

    # Adicionando o card da pressão abaixo da linha do gráfico
    if pressao:
        pressao_value = pressao[-1]  # Último valor
    else:
        pressao_value = 0
    media_pressao = sum(data) / len(data)
    fig.add_annotation(
        text=f'Pressão: {pressao_value*100:.2f}%',
        xref='paper', yref='y',
        x=0.5, y= 50,  # Ajuste a posição para ficar abaixo da linha
        showarrow=False,
        font=dict(size=32, color='yellow', family='Mini'),  # Fonte alterada para 'Mini' e texto em amarelo
        bgcolor='rgba(255, 255, 255, 0)',  # Fundo transparente
        bordercolor='yellow',
        borderwidth=4,
        borderpad=15,
        align='center'
    )


    # Estilizando o gráfico
    fig.update_layout(
        plot_bgcolor='#303030',
        paper_bgcolor='#303030',
        font_color='#FFFFFF',
        title=f'APPM Atualizado - {jogo_selecionado}',
        xaxis=dict(range=[0, 90], dtick=5, showgrid=False, title='Minuto'),
        yaxis=dict(range=[0, max(data) + 10], dtick=10, showgrid=False, title='APPM / Pressão (%)'),
        height=600,
        legend=dict(title="Legenda")
    )

    # Retorna os dados do gráfico como JSON
    graph_json = fig.to_json()
    return jsonify(graph_json)

if __name__ == '__main__':
    app.run(debug=True)
