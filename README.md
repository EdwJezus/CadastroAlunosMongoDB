# Projeto Cadastro e Login com Flask e MongoDB

Este é um projeto simples de aplicação web desenvolvida com Flask (Python) e MongoDB, que permite o cadastro de usuários, login com autenticação segura (senha criptografada) e exibição de perfil.

O projeto utiliza modelagem embutida e referenciada no MongoDB para armazenar dados de localização e profissão dos usuários.

---

## Funcionalidades

- Cadastro de usuários com dados pessoais (nome, email, senha, idade, sexo, localização e profissão)  
- Criptografia de senha usando `werkzeug.security`  
- Modelagem embutida para dados de localização (estado e cidade)  
- Modelagem referenciada para profissões em coleção separada  
- Login com validação de senha hash  
- Armazenamento de sessão para controle de usuário logado  
- Página de perfil exibindo as informações cadastradas  

---

## Tecnologias utilizadas

- Python 3.x  
- Flask  
- PyMongo  
- MongoDB  
- HTML/Jinja2 para templates  

---

## Instalação e execução

1. Clone o repositório:  
   ```bash
   git clone https://github.com/EdwJezus/CadastroAlunosMongoDB.git
   cd CadastroAlunosMongoDB
   ```

2. Instale as dependências: 
   ```bash
   pip install flask pymongo werkzeug
   ```

3. Certifique-se de que o MongoDB está rodando localmente na porta 27017.

4. Execute a aplicação:  
   ```bash
   python main.py
   ```

5. Acesse em seu navegador:
   ```bash
   http://127.0.0.1:5000/
   ```

---

## Estrutura do projeto

   ```bash
      /
   ├── main.py          # Código principal Flask com rotas e lógica
   ├── templates/       # Pasta com arquivos HTML (form.html, login.html, perfil.html)
   └── README.md        # Este arquivo
   ```

---

## Considerações

- As senhas são armazenadas criptografadas para garantir segurança.
- O sistema utiliza sessões para manter o usuário logado.
- Modelagem híbrida no MongoDB para demonstrar uso de dados embutidos e referenciados.
- Projeto voltado para fins didáticos e acadêmicos.

---

## Licença

MIT License © Eduardo Jesus
