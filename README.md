<h1>Análise Exploratória - ANAC</h1>

<p align="justify">O projeto busca analisar dados da ANAC (Agência Nacional de Aviação Civíl) planilhados, e transforma-los em insights úteis para fornecer uma visão estratégica e funcinal sobre a infraestrutura aeroportuária do país. Essa análise tem por finalidade praticar os ensinamentos aprendidos ao decorrer da capacitação em Analytics.</p>

<hr>

<h2>Tecnologias utilizadas</h2>
<ul>
    <li><strong>Python v3.13.3</strong></li>
    <li><strong>SQLite v3.49.1</strong>: Gerencia banco de dados SQLite. Usado para criar uma conexão entre um banco de dados e o projeto, criação de tabelas, inserção e consulta de dados da ANAC.
    <li><strong>Pandas v2.2.3</strong>: Manipula dados em tabelas (DataFrames). Usado para ler arquivos CSV e executar consultas SQL com retorno estruturado.</li>
    <li><strong>Streamlit v1.45.1</strong>: Cria dashboards interativos com interface web. Usado para a análise exploratória e visualição dos dados preliminares.</li>
    <li><strong>Matplotlib v3.10.3</strong>: Usa-se para apresentar dados personalizados. Usado para customizar os dados representados em planilhas</li>
    <li><strong>Seaborn v0.13.2</strong>: Cria gráficos dinâmicos para visualização dos dados. Usado para mostrar os dados explorados em esquemas interativos.</li>
</ul>

<hr>

<h2>Estrutura das pastas</h2>

<pre>
ANAC-EXPLORATORY-ANALYSIS/
├── 📁 csv/                  # Arquivos .csv usados no projeto para população dos Dados
│   ├── resumo_anual_2025.csv
├── 📁 modules/             # Funções reutilizáveis e lógica de negócio
│   ├── data.py
│   └── database.py
├── 📁 pages/               # Páginas do Streamlit
│   ├── cargas.py
│   ├── dashboard.py
│   ├── regioes.py
│   └── rotas.py
├── banco_de_dados.db      # Banco SQLite
└── main.py                # Arquivo principal do Streamlit
</pre>

<p align="justify">Outros arquivos e pastas foram omitidos por não serem essenciais para o entendimento da estrutura do projeto.</p>

<hr>

#FUNCIONALIDADES

<hr>

<h2>Como rodar esse projeto em seu ambiente</h2>

<h3>Pré-requisitos:</h3>
<ul>
  <li>Python v3.13.3 ou superior</li>
  <li>Git instalado</li>
  <li>Navegador moderno (Chrome, Firefox, etc.)</li>
</ul>

<h3>Passo a passo:</h3>
<ol>

  <li>
    <strong>Instale o Git (caso não possuir)</strong><br>
    Acesse: <a href="https://git-scm.com/downloads" target="_blank">git-scm.com/downloads</a><br>
    Baixe e instale conforme seu sistema operacional.<br>
    Verifique a instalação com:
    <pre><code>git --version</code></pre>
  </li>

  <li>
    <strong>Clone o repositório do projeto</strong>
    <pre><code>git clone https://github.com/HeitorDalla/ANAC-exploratory-analysis.git</code></pre>
  </li>

  <li>
    <strong>Instale as dependências do projeto</strong><br>
    <pre><code>pip install streamlit pandas seaborn matplotlib plotly pydeck airportsdata</code></pre>
  </li>

  <li>
    <strong>Execute a aplicação com Streamlit</strong>
    <pre><code>streamlit run main.py</code></pre>
    (Substitua <code>main.py</code> pelo nome do seu arquivo principal se for diferente.)
  </li>

  <li>
    <strong>Acesse no navegador</strong><br>
    Streamlit abrirá automaticamente. Caso contrário, acesse:
    <pre><code>http://localhost:8501</code></pre>
  </li>

</ol>

<hr>

<h2>⚠️ Importante</h2>

<p align="justify">Todos os dados utilizados neste projeto são oficiais e provenientes de fontes públicas do governo federal. Não há nenhum conteúdo restrito ou confidencial, tampouco dados ofensivos que possam ferir a privacidade, integridade ou reputação de indivíduos ou organizações. Dessa forma, assegura-se que tais dados não representem qualquer perigo ou risco, seja à segurança física ou digital de qualquer pessoa.</p>

<hr>

<h2>Contribuições</h2>
<p align="justify">Este projeto está aberto para contribuições via issues. Se você encontrou um bug, deseja sugerir uma melhoria ou tem dúvidas sobre o funcionamento, siga as instruções abaixo:</p>
<ol>
    <li>Verifique se já existe uma issue sobre o assunto. Caso sim, adicione um comentário nela.</li>
    <li>Se não houver, abra uma nova issue com uma descrição clara e objetiva.</li>
</ol>

<hr>

<h2>Licença e Autor</h2>
<p align="justify">Este projeto foi desenvolvido por <a href="https://github.com/HeitorDalla">Heitor Giussani Dalla Villa</a>, <a href="https://github.com/RaulSimioni">RaulSimioni</a>. Veja o <a href="./LICENSE">documento</a> para mais detalhes.</p>
