from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

# Criação da aplicação Flask
app = Flask(__name__)

app.secret_key = 'secreta'  # Necessário para sessões

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:castelo12@localhost/db_inaar'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuração do banco de dados luan
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345@localhost/db_inaar'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Definindo o modelo de Comidas no banco de dados
class Comidas(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_produto = db.Column(db.String(200), nullable=False)
    descricao_produto = db.Column(db.String(150), nullable=False)
    preco_produto = db.Column(db.Float, nullable=False)
    disponivel = db.Column(db.Boolean, default=True)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_usuario = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(100), nullable=False)

# Rota principal
@app.route('/')
def home():
    return render_template("pagina1.html")

@app.route("/cadastrar", methods=["GET", "POST"])
def cadastro_comida():
    if request.method == 'POST':
        nome = request.form['nome_comida']
        descricao = request.form['descricao']
        preco = float(request.form['valor_comida'])

        # Cria um novo objeto de comida
        nova_comida = Comidas(nome_produto=nome, descricao_produto=descricao, preco_produto=preco)

        # Adiciona no banco de dados
        db.session.add(nova_comida)
        db.session.commit()

        # Redireciona para o cardápio de comidas
        return redirect(url_for('cardapio_admin'))

    return render_template("cadastrar_comida.html")

# Rota do cardápio de admin
@app.route("/cardapio_admin")
def cardapio_admin():
    if 'logged_in' not in session:
        return redirect(url_for('login'))  # Redireciona para o login se não estiver logado

    comidas = Comidas.query.all()
    return render_template("cardapio_admin.html", comidas=comidas)

@app.route("/alterar_status/<int:id>", methods=["POST"])
def alterar_status(id):
    comida = Comidas.query.get(id)
    if comida:
        comida.disponivel = not comida.disponivel  # Alterna entre disponível e indisponível
        db.session.commit()
    return redirect(url_for('cardapio_admin'))

@app.route("/excluir/<int:id>", methods=["POST"])
def excluir_comida(id):
    comida = Comidas.query.get(id)
    if comida:
        db.session.delete(comida)  # Exclui o item do banco
        db.session.commit()
    return redirect(url_for('cardapio_admin'))

# Rota do cardápio para o cliente
@app.route("/cardapio_cliente")
def cardapio_cliente():
    comidas = Comidas.query.all()
    return render_template("/cardapio_cliente.html", comidas=comidas)

# Rota de login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        nome_usuario = request.form['usuario']
        senha = request.form['senha']
        
        # Verificar se o nome de usuário e a senha são corretos
        if nome_usuario == "inaar" and senha == "luciano123":
            session['logged_in'] = True  # Marca o admin como logado
            return redirect(url_for('cardapio_admin'))
        else:
            return "Usuário ou senha incorretos!", 401

    return render_template("login.html")

# Rodando o servidor
if __name__ == '__main__':
    app.run(debug=True)
