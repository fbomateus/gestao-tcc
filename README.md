# 🎓 Sistema de Gestão de TCC

Aplicação web desenvolvida em **Django** para gerenciamento completo do processo de Trabalhos de Conclusão de Curso (TCC). Permite controle de usuários por função (**Administrador**, **Orientador** e **Aluno**), além de cadastro de temas, entregas, feedbacks e administração via painel.

---

## Funcionalidades Principais

* Autenticação com modelo customizado de usuário
* Perfis de usuário:

  * **Administrador**
  * **Orientador**
  * **Aluno**
* CRUD de usuários (apenas Admin)
* Gestão de orientadores
* Cadastro e gestão de temas de TCC
* Upload de entregas (PDF, DOC, DOCX, ZIP)
* Feedback das entregas
* Dashboard pós login
* Django Admin para administração avançada

---

## Arquitetura do Projeto

```
gestao_tcc/
├── manage.py
├── gestao_tcc/        # Configurações do Django
├── core/              # App de usuários
├── tcc/               # App de TCC (temas, entregas, orientadores)
├── static/            # Arquivos estáticos
└── requirements.txt
```

---

## Tecnologias Utilizadas

* Python 3.x
* Django
* SQLite (desenvolvimento)
* HTML, CSS, Bootstrap

---

## Como Rodar o Projeto

### Clonar o Repositório

```bash
git clone https://github.com/seu-usuario/gestao-tcc.git
cd gestao-tcc
```

### Criar Ambiente Virtual

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

### Instalar Dependências

```bash
pip install -r requirements.txt
```

### Aplicar Migrações

```bash
python manage.py migrate
```

### Criar Superusuário

```bash
python manage.py createsuperuser
```

### Rodar o Servidor

```bash
python manage.py runserver
```

Acesse:

* Sistema: **[http://localhost:8000/](http://localhost:8000/)**
* Admin Django: **[http://localhost:8000/admin/](http://localhost:8000/admin/)**

---

## Variáveis de Ambiente

Crie um arquivo `.env` na raiz:

```
SECRET_KEY=sua-chave-secreta
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

---

## Tipos de Usuários

### Administrador

* Controle total do sistema
* Pode gerenciar usuários, orientadores, temas e entregas

###  Orientador

* Cadastro de temas
* Avaliação e feedback das entregas dos alunos
* Área de atuação obrigatória

### Aluno

* Visualiza temas, envia arquivos e acompanha feedbacks
* Matrícula obrigatória

---

## Estrutura dos Principais Apps

### **core/** – Gerenciamento de Usuários

* Modelo customizado de usuário
* Controle de autenticação
* CRUD de usuários (admin)

### **tcc/** – Domínio do Sistema

* Temas de TCC
* Entregas e uploads
* Feedbacks
* Orientadores

---

## URLs Importantes

### Autenticação

* `/login/` – Login
* `/logout/` – Logout
* `/register/` – Registro

### Usuários

* `/usuarios/` – Listagem
* `/usuarios/novo/` – Criar usuário
* `/usuarios/<id>/editar/` – Editar usuário

### TCC

* `/tcc/temas/` – Lista de temas
* `/tcc/temas/novo/` – Criar tema
* `/tcc/temas/<id>/editar/` – Editar tema
* `/tcc/temas/<id>/excluir/` – Excluir tema
* `/tcc/temas/<tema_id>/entregas/` – Entregas do tema
* `/tcc/temas/<tema_id>/entregas/nova/` – Nova entrega
* `/tcc/entregas/<entrega_id>/feedback/` – Feedback

---

## Exemplos de Usuários

### Administradores

* admin / [admin@sistema.com](mailto:admin@sistema.com) / Admin@123
* coordcurso / [coord.curso@sistema.com](mailto:coord.curso@sistema.com) / Coord@123

### Orientadores

* j_silva / [joao.silva@universidade.com](mailto:joao.silva@universidade.com)
* a_oliveira / [ana.oliveira@universidade.com](mailto:ana.oliveira@universidade.com)
* c_pereira / [carlos.pereira@universidade.com](mailto:carlos.pereira@universidade.com)

### Alunos

* m_souza / [maria.souza@aluno.com](mailto:maria.souza@aluno.com) / 20230001
* p_santos / [pedro.santos@aluno.com](mailto:pedro.santos@aluno.com) / 20230002
* j_carvalho / [julia.carvalho@aluno.com](mailto:julia.carvalho@aluno.com) / 20230003
