<div align="center">
  <h1>🎙️ Plataforma de Processamento de Áudio e Resumos Automáticos</h1>
  <p><i>Uma arquitetura moderna, distribuída e perfeitamente orquestrada para transcrição e resumos inteligentes com IA.</i></p>
  
  <p>
    <img src="https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white" alt="Angular" />
    <img src="https://img.shields.io/badge/Ionic-3880FF?style=for-the-badge&logo=ionic&logoColor=white" alt="Ionic" />
    <img src="https://img.shields.io/badge/Spring_Boot-6DB33F?style=for-the-badge&logo=spring-boot&logoColor=white" alt="Spring Boot" />
    <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
    <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" />
  </p>
</div>

<hr />

<h2>🏗️ Arquitetura do Sistema</h2>
<p>O ecossistema foi projetado seguindo o modelo de <b>Arquitetura em Três Camadas</b>. Essa separação garante o isolamento de escopo, facilita manutenções pontuais e permite a escalabilidade elástica de forma independente.</p>

<table width="100%">
  <tr>
    <td width="33.3%" valign="top" style="border: 1px solid #e1e4e8; border-radius: 6px; padding: 16px; background-color: #f6f8fa;">
      <h3>📱 1. Apresentação (Front-end)</h3>
      <p><b>Tecnologias:</b> Angular & Ionic</p>
      <p>Interface unificada e responsiva adequada tanto para navegadores Web quanto para dispositivos móveis (Mobile).</p>
      <ul>
        <li>Experiência idêntica multi-dispositivo</li>
        <li>Validação robusta de formulários</li>
        <li>Consumo otimizado de APIs REST</li>
        <li>Gestão de estado client-side</li>
      </ul>
    </td>
    <td width="33.3%" valign="top" style="border: 1px solid #e1e4e8; border-radius: 6px; padding: 16px; background-color: #f6f8fa;">
      <h3>⚙️ 2. Negócios (Back-end)</h3>
      <p><b>Tecnologias:</b> Java & Spring Boot</p>
      <p>O núcleo inteligente e orquestrador de microsserviços. Garante a estabilidade e a segurança das operações.</p>
      <ul>
        <li>Tipagem forte e segurança robusta</li>
        <li>Autenticação e autorização via JWT</li>
        <li>Gestão transacional de dados</li>
        <li>Endpoints REST prontos para escala</li>
      </ul>
    </td>
    <td width="33.3%" valign="top" style="border: 1px solid #e1e4e8; border-radius: 6px; padding: 16px; background-color: #f6f8fa;">
      <h3>🤖 3. Processamento (IA)</h3>
      <p><b>Tecnologias:</b> Python & FastAPI</p>
      <p>Microsserviço assíncrono especializado em lidar estritamente com tarefas de alto custo computacional.</p>
      <ul>
        <li>Integração veloz com LLMs</li>
        <li>Transcrição assíncrona de áudios</li>
        <li>Geração automatizada de resumos</li>
        <li>Documentação nativa com Swagger</li>
      </ul>
    </td>
  </tr>
</table>

<br />

<hr />

<h2>📦 Como Executar o Projeto</h2>
<p>O projeto está 100% conteinerizado e automatizado através do <b>Docker Compose</b>, fazendo uso de 3 arquivos <code>Dockerfile</code> distintos.</p>

<h3>📋 Pré-requisitos</h3>
<ul>
  <li>Docker instalado e rodando</li>
  <li>Docker Compose configurado</li>
</ul>

<h3>🚀 Instruções Práticas</h3>

<ol>
  <li>
    <b>Clonar o Repositório:</b>
    <pre><code>git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio</code></pre>
  </li>
  <li>
    <b>Configurar as Variáveis de Ambiente:</b>
    <p>Crie o arquivo de configuração local a partir do modelo disponibilizado:</p>
    <pre><code>cp .env.example .env</code></pre>
    <p><i>Nota: Abra o arquivo <code>.env</code> gerado e preencha as credenciais e chaves necessárias.</i></p>
  </li>
  <li>
    <b>Construir e Inicializar os Containers:</b>
    <p>Suba toda a infraestrutura com um único comando:</p>
    <pre><code>docker compose up --build</code></pre>
  </li>
</ol>

<hr />

<h2>📂 Estrutura Organizacional</h2>
<p>Para o correto funcionamento do ecossistema, certifique-se de que os diretórios seguem o padrão mapeado abaixo:</p>

<pre><code>.
├── backend/            # Código-fonte da API Spring Boot (+ Dockerfile)
├── frontend/           # Aplicação Angular/Ionic (+ Dockerfile)
├── microservice/       # Microsserviço FastAPI (+ Dockerfile)
├── .env.example        # Modelo base de variáveis de ambiente
├── .env                # Variáveis de produção/desenvolvimento (Ignorado no Git)
└── docker-compose.yml  # Manifesto de orquestração do ecossistema Docker
</code></pre>
