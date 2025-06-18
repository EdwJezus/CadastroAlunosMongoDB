######################################## Iniciando Flask

from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash ## Criptografia para senha

app = Flask(__name__)
app.secret_key = 'senha'

######################################## Comunicação com o MongoDB

from pymongo import MongoClient

client = MongoClient("localhost", 27017)

db = client.BancoAlunos

colecao_pessoas = db.pessoas

for pessoa in colecao_pessoas.find(): ## Imprime as pessoas no Terminal para testar
    print(pessoa)

######################################## Comunicação HTML -> Flask -> MongoDB

##################### Cadastro

@app.route('/') ## Definindo a rota de inicialização
def index():
    return render_template("form.html")

@app.route('/submit', methods=['POST']) ## Puxando informações enviadas no form HTML
def submit():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']
    idade = request.form['idade']
    sexo = request.form['sexo']
    estado = request.form['estado']
    cidade = request.form['cidade']
    profissao = request.form['profissao']

    senha_hash = generate_password_hash(senha) ## Serve para criptografar e proteger a senha

    nova_profissao = {"nome": profissao} ## Separa profissão para a coleção profissoes
    colecao_profissoes = db.profissoes.insert_one(nova_profissao)

    colecao_pessoas.insert_one({ ## Enviando informações do form para o Banco, e criando uma nova pessoa
        "nome": nome,
        "email": email,
        "senha": senha_hash,
        "idade": idade,
        "sexo": sexo,
        "localizacao": { ## Modelagem Embutida
            "estado": estado,
            "cidade": cidade},
        "profissao_id": colecao_profissoes.inserted_id ## Usa Modelagem Referenciada para puxar a profissao da coleção profissoes
    })

    return redirect('/login')

######################## Login

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        usuario = colecao_pessoas.find_one({"email": email}) ## Procura no banco pelo email
        if usuario and check_password_hash(usuario['senha'], senha): ## Verifica se usuario existe no banco e se a senha esta correta
            session['usuario'] = usuario['nome'] ## Coloca o nome do usuario na sessao
            return redirect('/perfil') ## Se login bem sucedido segue para o perfil
        
        else: ## Else caso usuario e senha digitado estejam errados
            return "Email ou senha ínvalidos"
        
    return render_template('login.html')

########################## Perfil

@app.route('/perfil')
def perfil():
    if 'usuario' not in session:
        return redirect('/login')
    
    pessoa = colecao_pessoas.find_one({"nome": session['usuario']}) ## Pega os dados completos da pessoa logada
    
    profissao = db.profissoes.find_one({"_id": pessoa["profissao_id"]}) ## Pega o nome da profissão referenciada se existir
    
    return render_template('perfil.html', pessoa=pessoa, profissao=profissao)

if __name__ == '__main__':
    app.run(debug=True)
