# Tarefas Aleatórias

Aplicação Flask para gerar tarefas aleatórias para fazer em casa, com base em diferentes categorias e tempo disponível.

## Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes do Python)

## Instalação

1. Clone o repositório:
   ```bash
   git clone <url-do-repositório>
   cd principal-tarefas-aleatorias
   ```

2. Crie um ambiente virtual (recomendado):
   ```bash
   python -m venv venv
   venv\Scripts\activate  # No Windows
   # ou
   source venv/bin/activate  # No Linux/Mac
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Configuração

O aplicativo usa um banco de dados SQLite chamado `listas.db` que deve estar na pasta `app/`. Certifique-se de que o arquivo existe e contém as tabelas necessárias.

## Executando o Aplicativo

1. Inicie o servidor de desenvolvimento:
   ```bash
   python run.py
   ```

2. Acesse o aplicativo no navegador:
   ```
   http://127.0.0.1:5000/
   ```

## Rotas da API

### GET /atividades/casa

Retorna uma atividade aleatória para fazer em casa.

**Parâmetros:**
- `tempo` (opcional, padrão=60): Tempo disponível em minutos
- `reset` (opcional): Se definido como 'true', limpa o histórico de atividades mostradas

**Exemplo de resposta:**
```json
{
  "atividade": "Jogos eletrônicos",
  "detalhes": {
    "jogo": "The Witcher 3"
  },
  "tempo_estimado": 120
}
```

### GET /musica

Retorna uma música aleatória para ouvir.

**Exemplo de resposta:**
```json
{
  "atividade": "Ouvir música",
  "detalhes": {
    "musica": "Álbum: Folklore - Taylor Swift"
  }
}
```

## Testes

Para executar os testes automatizados:

```bash
python -m unittest test_routes.py
```

## Estrutura do Projeto

```
principal-tarefas-aleatorias/
├── app/
│   ├── __init__.py      # Inicialização do aplicativo
│   ├── routes.py        # Rotas da API
│   └── database.py      # Acesso ao banco de dados
├── listas.db           # Banco de dados SQLite
├── run.py              # Ponto de entrada do aplicativo
├── test_routes.py      # Testes automatizados
└── README.md           # Este arquivo
```

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.
