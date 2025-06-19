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

## Imprime as pessoas no Terminal para testar
for pessoa in colecao_pessoas.find(): 
    print(pessoa)

######################################## Comunicação HTML -> Flask -> MongoDB

    #============== Cadastro

## Definindo a rota de inicialização
@app.route('/') 
def index():
    return render_template("form.html")

## Puxando informações enviadas no form HTML
@app.route('/submit', methods=['POST']) 
def submit():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']
    idade = request.form['idade']
    sexo = request.form['sexo']
    estado = request.form['estado']
    cidade = request.form['cidade']
    profissao = request.form['profissao']

    ## Serve para criptografar e proteger a senha
    senha_hash = generate_password_hash(senha) 

    ## Separa profissão para a coleção profissoes
    nova_profissao = {"nome": profissao} 
    colecao_profissoes = db.profissoes.insert_one(nova_profissao)

    ## Enviando informações do form para o Banco, e criando uma nova pessoa
    colecao_pessoas.insert_one({ 
        "nome": nome,
        "email": email,
        "senha": senha_hash,
        "idade": idade,
        "sexo": sexo,
        ## Modelagem Embutida
        "localizacao": { 
            "estado": estado,
            "cidade": cidade},
        ## Usa Modelagem Referenciada para puxar a profissao da coleção profissoes
        "profissao_id": colecao_profissoes.inserted_id 
    })

    return redirect('/login')

    #============== Login

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        ## Procura no banco pelo email
        usuario = colecao_pessoas.find_one({"email": email}) 
        ## Verifica se usuario existe no banco e se a senha esta correta]
        if usuario and check_password_hash(usuario['senha'], senha): 
            ## Coloca o nome do usuario na sessao
            session['usuario'] = usuario['nome'] 
            ## Se login bem sucedido segue para o perfil
            return redirect('/perfil') 
        
        ## Else caso usuario e senha digitado estejam errados
        else: 
            return "Email ou senha ínvalidos"
        
    return render_template('login.html')

    #============== Perfil

@app.route('/perfil')
def perfil():
    if 'usuario' not in session:
        return redirect('/login')
    
    ## Pega os dados completos da pessoa logada
    pessoa = colecao_pessoas.find_one({"nome": session['usuario']}) 
    
    ## Pega o nome da profissão referenciada se existir
    profissao = db.profissoes.find_one({"_id": pessoa["profissao_id"]}) 
    
    return render_template('perfil.html', pessoa=pessoa, profissao=profissao)

if __name__ == '__main__':
    app.run(debug=True)
