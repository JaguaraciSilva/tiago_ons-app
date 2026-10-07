# ⚡ Assistente Inteligente - Dados Abertos ONS (TIAGO)

Plataforma corporativa de consulta inteligente aos dados abertos do setor elétrico brasileiro (Operador Nacional do Sistema Elétrico - ONS), utilizando **FastAPI**, **LangChain**, um Modelo de Linguagem de Tamanho Reduzido (SLM) rodando via **vLLM**, e interface em **Streamlit**.

---

## 📋 Pré-requisitos de Sistema (Linux Debian)

Certifique-se de que o seu ambiente Debian possui os seguintes componentes instalados:
* **Docker** e **Docker Compose** atualizados.
* **NVIDIA Container Toolkit** configurado (caso vá rodar o SLM localmente utilizando uma placa de vídeo NVIDIA).
* Espaço em disco suficiente na partição configurada para o Docker (recomenda-se apontar o diretório de dados para uma partição com amplo espaço livre, como `/home`).

---

## 🚀 Instruções de Execução

### 1. Clonar ou Baixar o Projeto
Abra o terminal do Debian e navegue até a pasta onde deseja manter a aplicação:
```bash
cd /caminho/para/seu/diretorio
```

### 2. Configurar o Armazenamento do Docker (Opcional, recomendado para economia de espaço)

Caso queira evitar lotar a partição raiz (/) do Debian com os pesos do modelo SLM, certifique-se de que o Docker está configurado para salvar os dados em uma partição com bastante espaço livre (ex: /home/docker-data) alterando o ficheiro /etc/docker/daemon.json:

```bash
{
  "data-root": "/home/docker-data"
}

```

Verifique se o docker está exeutando no diretório alterado:

```bash
sudo docker info | grep "Docker Root Dir"
```

reinicie o serviço:

```bash
sudo systemctl restart docker
```

### 3. Configurar Variáveis de Ambiente

Crie um arquivo .env na raiz do projeto caso utilize modelos que exijam token de acesso (como modelos restritos da Meta, ex: Llama):

HUGGING_FACE_HUB_TOKEN=seu_token_aqui

Para modelos livres como o Qwen 2.5, esta etapa é opcional).


### 4. Executar o Ollama e Baixar o Modelo SLM#

Inicie primeiro apenas o conteiner do Ollama:

```bash
sudo docker compose up -d ollama
```

Baixe o modelo Qwen 2.5 (3B) para dentro do conteiner:

```bash
sudo docker exec -it tiago_ollama ollama run qwen2.5:3b
```

### 5. Executar a Aplicação com Docker Compose

Na raiz do projeto, suba todos os serviços em segundo plano:

```bash
sudo docker compose up --build -d
```

### 6. Observar os logs

```bash
sudo docker compose logs -f backend
```

### 7. Acessar a Interface

Após a inicialização completa dos serviços (o carregamento do modelo SLM na GPU pode levar alguns instantes), abra o navegador e acesse:

    Interface de Chat (Streamlit): http://localhost:8501

    API Backend (FastAPI / Swagger): http://localhost:8001/docs


### 8. Exemplos de consultas ao ONS

*Geração de Energia:

    "Qual foi a geração solar total no Nordeste em 2024?"

    "Mostre a geração por fonte de energia ontem."

    "Qual a participação da energia eólica na matriz do subsistema Sul no último trimestre?"

*Carga de Energia e Subsistemas:

    "Faça uma comparação da carga de energia entre os subsistemas em 2024."

    "Qual foi a carga registada no subsistema Sudeste/Centro-Oeste no mês passado?"

*Intercâmbio de Energia:

    "Qual foi a variação mensal do intercâmbio de energia entre os subsistemas em 2025?"

    "Como se comportou o fluxo de intercâmbio entre as regiões Norte e Nordeste?"

*Nível de Reservatórios e Recursos Hídricos:

    "Qual é o nível atual dos reservatórios do subsistema Norte?"

    "Compare a energia armazenada nos reservatórios da bacia do Rio Paraná em relação ao ano anterior."


* Maiores detalhes para utilizar MCP da ONS -> https://github.com/ONSBR/TIAGO-Dados-Abertos

#### 🧪 Execução de Testes e Qualidade

Para rodar os testes unitários e verificar o quality gate do projeto:

    1. Instale as dependências de teste e qualidade:

        pip install pytest pytest-cov ruff
    

    2. Valide o estilo e as regras estáticas de código:

        ruff check .

    3. Execute os testes unitários:

        pytest
