# Casa de Apostas - Desafio Fullstack

Este projeto foi desenvolvido como resolução do desafio de programação para a vaga de Desenvolvedor Fullstack. Trata-se de um sistema web completo para o cadastro de Clientes e gerenciamento de seus respectivos Contatos vinculados, com relatórios em PDF e autenticação segura.

## 🚀 Tecnologias Utilizadas

A stack foi escolhida pensando em simplicidade de execução.

- **Back-end:** Python (Flask)
- **Banco de Dados:** SQLite 
- **Segurança & Auth:** Flask-Login (gerenciamento de sessão) e bcrypt (hash de senhas)
- **Geração de PDF:** ReportLab
- **Front-end / UI:** Vanilla HTML, CSS e Jinja2 (Templates)
---

## 🛠️ Como rodar o projeto localmente

A grande vantagem dessa arquitetura é que o avaliador **não precisa instalar banco de dados** ou configurações complexas. Tudo já está embutido!

### Pré-requisitos
- **Python 3.8+** instalado na máquina.

### Passo 1: Clonar o repositório
```bash
git clone git@github.com:vinicgs/casa-de-apostas.git
cd casa-de-apostas
```

### Passo 2: Criar e ativar o ambiente virtual (Recomendado)
```bash
# No Windows
python -m venv venv
venv\Scripts\activate

# No Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Passo 3: Instalar as dependências
```bash
pip install -r requirements.txt
```

### Passo 4: Rodar a aplicação
O banco de dados (`app.db`) e as tabelas são inicializados automaticamente quando o app roda.
```bash
python app.py
```

**Acesse no navegador:** [http://127.0.0.1:3000](http://127.0.0.1:3000)

## 🔐 Credenciais de Acesso (Login)

- **E-mail:** `admin@casadeapostas.com`
- **Senha:** `admin123`
