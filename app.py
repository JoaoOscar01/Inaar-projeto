import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Criação da aplicação Flask
app = Flask(__name__)
app.secret_key = 'secreta'  # Necessário para sessões

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://inaar_db_u15h_user:GOhmuBhb6P1Q46iaNI9UCwBdw4c6MqBd@dpg-cv9o0ctds78s73br3q30-a/inaar_db_u15h'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuração do diretório de upload de imagens
UPLOAD_FOLDER = 'static/img/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Banco de dados
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Função para verificar extensões de imagem
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Modelos do banco de dados
class Comidas(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_produto = db.Column(db.String(200), nullable=False)
    descricao_produto = db.Column(db.String(150), nullable=False)
    preco_produto = db.Column(db.Float, nullable=False)
    disponivel = db.Column(db.Boolean, default=True)
    imagem_produto = db.Column(db.String(100), nullable=True)
    link_imagem = db.Column(db.String(200), nullable=True)
    categoria_produto = db.Column(db.String(50), nullable=False)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_usuario = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(100), nullable=False)

# Criar as tabelas no banco (caso não existam)
with app.app_context():
    db.create_all()

# Rotas
@app.route('/')
def home():
    return render_template("pagina1.html")

@app.route('/contatos')
def contato():
    return render_template("contact.html")

@app.route("/cadastrar", methods=["GET", "POST"])
def cadastro_comida():
    if request.method == 'POST':
        nome = request.form['nome_comida']
        descricao = request.form['descricao']
        preco = float(request.form['valor_comida'])
        link_imagem = request.form['link_imagem']
        categoria = request.form['categoria_produto']
        imagem = request.files.get('imagem')

        if not imagem or not allowed_file(imagem.filename):
            flash("Erro: Nenhuma imagem enviada ou formato inválido.", "error")
            return redirect(request.url)
        
        filename = secure_filename(imagem.filename)
        imagem.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        nova_comida = Comidas(
            nome_produto=nome,
            descricao_produto=descricao,
            preco_produto=preco,
            imagem_produto=filename,
            link_imagem=link_imagem,
            categoria_produto=categoria
        )

        db.session.add(nova_comida)
        db.session.commit()
        flash("Comida cadastrada com sucesso!", "success")
        return redirect(url_for('cardapio_admin'))
    
    return render_template("cadastrar_comida.html")

@app.route("/cardapio_admin")
def cardapio_admin():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    comidas = Comidas.query.all()
    return render_template("cardapio_admin.html", comidas=comidas)

@app.route("/alterar_status/<int:id>", methods=["POST"])
def alterar_status(id):
    comida = Comidas.query.get(id)
    if comida:
        comida.disponivel = not comida.disponivel
        db.session.commit()
    return redirect(url_for('cardapio_admin'))

@app.route("/excluir/<int:id>", methods=["POST"])
def excluir_comida(id):
    comida = Comidas.query.get(id)
    if comida:
        db.session.delete(comida)
        db.session.commit()
    return redirect(url_for('cardapio_admin'))

@app.route("/cardapio_cliente")
def cardapio_cliente():
    comidas = Comidas.query.all()
    return render_template("cardapio_cliente.html", comidas=comidas)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        nome_usuario = request.form['usuario']
        senha = request.form['senha']
        
        if nome_usuario == "inaar" and senha == "luciano123":
            session['logged_in'] = True
            return redirect(url_for('cardapio_admin'))
        else:
            flash("Usuário ou senha incorretos!", "error")
    return render_template("login.html")

if __name__ == '__main__':
    app.run(debug=True)
