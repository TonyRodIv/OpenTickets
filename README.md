# OpenTickets 🎟️
![Capa do Open Tickets](https://github.com/TonyRodIv/OpenTickets/blob/main/static/assets/OpenTickets-cover.png?raw=true)

OpenTickets é um sistema de gerenciamento de bilheteria de cinema, de código aberto, construído para ser prático e intuitivo. Ele oferece um painel administrativo completo e uma interface de vendas (totem) para facilitar a gestão do seu cinema.

O projeto é desenvolvido em Python, utilizando o micro-framework Flask para o backend, e HTML, CSS e JavaScript para o frontend. Os dados são armazenados de forma simples e direta em arquivos JSON.

## ✨ Funcionalidades

O sistema é dividido em duas grandes áreas: o Totem de Venda e o Dashboard Administrativo.

### Totem de Venda (Interface do Cliente)

Uma interface de vendas fluida e direta, projetada para totens de autoatendimento ou para o uso por funcionários no caixa.

  * **Página Inicial**: Uma tela de boas-vindas que direciona o cliente para o fluxo de compra.
  * **Seleção de Filme**: O cliente pode visualizar todos os filmes em cartaz e escolher o que deseja assistir.
  * **Escolha de Sala e Horário**: Para o filme selecionado, o sistema exibe as salas e os horários disponíveis.
  ![Tela de escolha de sessão](https://github.com/TonyRodIv/OpenTickets/blob/main/static/assets/OpenTickets-totem-movie.png?raw=true)
  * **Mapa Interativo de Assentos**: Um mapa visual da sala é apresentado, permitindo que o cliente escolha seus lugares. Assentos já ocupados são mostrados como indisponíveis.
  ![Tela de escolha de assento](https://github.com/TonyRodIv/OpenTickets/blob/main/static/assets/OpenTickets-movie-seats.png?raw=true)
  * **Confirmação de Venda**: Ao final, um resumo do pedido é exibido com os detalhes do filme, sala, assentos e o valor total, gerando um "ingresso" virtual.

### Dashboard Administrativo 🧑‍💻

A área de gerenciamento do sistema, acessada por meio de um login seguro, onde os administradores têm controle total sobre as operações.

![Dashboard do adm](https://github.com/TonyRodIv/OpenTickets/blob/main/static/assets/OpenTickets-adm.png?raw=true)

  * **Login**: Acesso à área administrativa com nome de usuário e senha. _(não finalizado)_
  * **Gerenciamento de Filmes**:
      * **Adicionar**: Cadastre novos filmes com título, duração, classificação indicativa, gênero e URL do pôster.
      * **Listar e Editar**: Visualize todos os filmes cadastrados e edite suas informações a qualquer momento.
  * **Gerenciamento de Salas**:
      * **Adicionar**: Crie novas salas, definindo a quantidade de fileiras (linhas) e poltronas (colunas).
      * **Listar e Editar**: Visualize os detalhes das salas, incluindo os filmes em exibição, e edite suas dimensões.
  * **Relatórios**:
      * Acesse relatórios de vendas diárias para acompanhar o faturamento e o número de ingressos vendidos.
      * Veja um ranking de filmes mais populares com base no número de vendas.

## 🚀 Como Executar o Projeto

### Pré-requisitos

  * Python 3.x
  * Flask

### Instalação

1.  Clone este repositório para a sua máquina local.
2.  Instale a única dependência (Flask) via pip:
    ```bash
    pip install Flask
    ```
3.  Navegue até o diretório raiz do projeto.
4.  Execute o arquivo principal:
    ```bash
    python main.py
    ```

### Acesso

  * **Página Inicial do Totem**: Abra seu navegador e acesse `http://127.0.0.1:5000/`.
  * **Login do Administrador**: Para acessar o painel administrativo, acesse `http://127.0.0.1:5000/adm/`.
      * **Usuário**: adm
      * **Senha**: adm

## 📂 Estrutura de Arquivos

```
/
|-- main.py                # Ponto de entrada da aplicação Flask
|-- data/
|   |-- gerenciar_assentos.py # Lógica para gerenciar assentos
|   |-- gerenciar_filmes.py  # Lógica para gerenciar filmes
|   |-- gerenciar_sala.py    # Lógica para gerenciar salas
|   |-- gerenciar_vendas.py  # Lógica para registrar e calcular vendas
|   |-- temp/                # Diretório que atua como "banco de dados"
|       |-- assentos.json
|       |-- filmes.json
|       |-- salas.json
|       |-- vendas.json
|-- routes/
|   |-- adm.py               # Rotas do painel administrativo
|   |-- login.py             # Rota da página inicial/login
|   |-- vend.py              # Rotas do totem de vendas
|-- static/
|   |-- css/                 # Arquivos de estilo (CSS)
|   |-- img/                 # Imagens
|   |-- js/                  # Arquivos de script (JavaScript)
|-- templates/
|   |-- adm/                 # Templates HTML para a área do ADM
|   |-- vend/                # Templates HTML para o totem de vendas
|   |-- index.html           # Template da página inicial
`-- README.md                # Este arquivo :)
```

## 🛠️ Tecnologias Utilizadas

  * **Backend**: Python, Flask
  * **Frontend**: HTML, CSS, JavaScript
  * **Banco de Dados**: Arquivos JSON para persistência de dados.

  ![Capa do Open Tickets](https://github.com/TonyRodIv/OpenTickets/blob/main/static/assets/OpenTickets-cover-alt.png?raw=true)
