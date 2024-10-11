# Projeto de Monitoramento de APPM e Escanteios

Este projeto utiliza Flask para criar um dashboard interativo que exibe o APPM e escanteios de diferentes jogos. Os dados são atualizados automaticamente a cada minuto com base em um banco de dados SQLite.

## Funcionalidades

- Gráfico dinâmico com valores de APPM atualizados a cada minuto.
- Exibição de escanteios como pontos destacados no gráfico.
- Exibição de pressão em porcentagem em um card estilizado abaixo do gráfico.
- Interface de seleção para escolher o jogo desejado.

## Estruturação do projeto
```
meu_projeto/
│
├── app.py                     # O código principal Flask
├── recupera_dados.py           # Script de scraping para recuperar dados
├── dados_jogos.db              # Base de dados SQLite
├── Base_de_dados.py            # Script que cria a base de dados
├── Deleta_jogos.py             # Script que limpa toda a base de dados
├── templates/                  # Templates HTML
│   ├── index.html              # Template principal
├── README.md                   # Instruções de uso e documentação
├── requirements.txt            # Dependências do projeto
```


## Instalação

### Pré-requisitos

- Python 3.x
- Pip (gerenciador de pacotes Python)

### Passo a passo

1. Clone o repositório:

   ```bash
   git clone https://github.com/victor-sousa-hub/Dashboard-escanteios
   cd seu-repositorio
   pip install -r requirements.txt
2. Rodando o programa:
    1. Na primeira vez rode o comando: python3 Base_de_dados.py para criar o banco de dados
    2. Logo em seguida começe a recuperar os dados dos jogos ao vivo com o comando: python3 recupera_dados.py
    3. Por fim rode o comando: python3 app.py para inciar a instancia do grafico.
    4. No seu navegador va em https://localhost:5000

