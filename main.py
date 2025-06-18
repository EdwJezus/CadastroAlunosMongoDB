######################################## Iniciando Flask

from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)

######################################## Comunicação com o MongoDB

from pymongo import MongoClient

client = MongoClient("localhost", 27017)

db = client.BancoCadeiraAline

pessoas = db.pessoas

for pessoa in pessoas.find(): ## Imprimi as pessoas no Terminal para testar
    print(pessoa)

######################################## Comunicação HTML -> Flask -> MongoDB

@app.route('/') ## Definindo a rota de inicialização
def index():
    return render_template("form.html")

@app.route('/submit', methods=['POST']) ## Puxando informações enviadas no form HTML
def submit():
    nome = request.form['nome']
    idade = request.form['idade']
    sexo = request.form['sexo']
    estado = request.form['estado']
    cidade = request.form['cidade']

    if not all([nome, idade, sexo, estado, cidade]):
        return "Campos faltando", 400 # aqui pode chamar uma função que apareça um alerta no javascript.

    pessoas.insert_one({ ## Enviando informações do form para o Banco, e criando uma nova pessoa
        "nome": nome,
        "idade": idade,
        "sexo": sexo,
        "estado": estado,
        "cidade": cidade
    })

    return redirect('/')

@app.route('/view', methods=['GET'])
def view():
    result = list(pessoas.find({}, {"estado": 0})) # segunda chave faz o resultado não exibir "estado"
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)