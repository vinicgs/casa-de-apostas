# Casa de Apostas - Desafio Fullstack

Este projeto foi desenvolvido como resolução do desafio de programação para a vaga de Desenvolvedor Fullstack. Trata-se de um sistema web completo para o cadastro de Clientes e gerenciamento de seus respectivos Contatos vinculados, com relatórios em PDF e autenticação segura.

## 🚀 Tecnologias Utilizadas

A stack foi escolhida pensando em simplicidade de execução, robustez e agilidade de avaliação, demonstrando proficiência no Back-end, Banco de Dados, Front-end e UI/UX:

- **Back-end:** Python (Flask)
- **Banco de Dados:** SQLite (nativo, sem necessidade de containers ou instalações extras)
- **Segurança & Auth:** Flask-Login (gerenciamento de sessão) e bcrypt (hash de senhas)
- **Geração de PDF:** ReportLab
- **Front-end / UI:** Vanilla HTML, CSS e Jinja2 (Templates)
- **Design System:** Design Premium "Mobile-First", focado em usabilidade, *glassmorphism* e tema dark moderno.

---

## 🛠️ Como rodar o projeto localmente

A grande vantagem dessa arquitetura é que o avaliador **não precisa instalar banco de dados** ou configurações complexas. Tudo já está embutido!

### Pré-requisitos
- **Python 3.8+** instalado na máquina.

### Passo 1: Clonar o repositório
```bash
git clone https://github.com/SEU_USUARIO/casa-de-apostas.git
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

---

## 🔐 Credenciais de Acesso (Login)

Como diferencial, o sistema conta com uma proteção por login. Para facilitar o teste do avaliador, **o usuário Administrador é criado automaticamente no primeiro acesso** se você utilizar as seguintes credenciais na tela de login:

- **E-mail:** `admin@casadeapostas.com`
- **Senha:** `admin123`

---

## ✨ Funcionalidades e Requisitos Atendidos

✅ **CRUD de Clientes:** Criar, visualizar, editar e excluir clientes (Nome, E-mails, Telefones, Data de Registro).  
✅ **CRUD de Contatos:** Criar, visualizar, editar e excluir contatos vinculados a um cliente.  
✅ **Relacionamento 1:N:** Um cliente pode possuir múltiplos contatos associados.  
✅ **Relatório de Clientes e Contatos:** Visualização em tela no Painel e botão para download do arquivo **PDF** detalhado.  

### Diferenciais Implementados:
⭐ **Documentação Clara:** Este README detalhando a configuração de ambiente.  
⭐ **Apresentação Visual Premium:** Design totalmente customizado sem dependência pesada de frameworks (apenas CSS puro), garantindo um layout lindo, dinâmico e responsivo.  
⭐ **Login e Segurança:** Fluxo de Login implementado com armazenamento de senha encriptada (Hash BCrypt).

---

Feito com ☕ e muito código limpo.
