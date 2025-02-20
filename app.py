from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Criação da aplicação Flask
app = Flask(__name__)

# Configuração do banco de dados João
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:castelo12@localhost/db_inaar'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuração do banco de dados luan
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345@localhost/db_inaar'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Definindo o modelo de Comidas no banco de dados
class Comidas(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_produto = db.Column(db.String(200), nullable=False)
    descricao_produto = db.Column(db.String(150), nullable=False)
    preco_produto = db.Column(db.Float, nullable=False)
    disponivel = db.Column(db.Boolean, default=True)


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
        return redirect(url_for('cardapio_user'))

    return render_template("cadastrar_comida.html")

# Rota do cardápio de usuários
@app.route("/cardapio")
def cardapio_user():
    # Consulta todas as comidas cadastradas no banco
    comidas = Comidas.query.all()
    return render_template("cardapio_user.html", comidas=comidas)

@app.route("/alterar_status/<int:id>", methods=["POST"])
def alterar_status(id):
    comida = Comidas.query.get(id)
    if comida:
        comida.disponivel = not comida.disponivel  # Alterna entre disponível e indisponível
        db.session.commit()
    return redirect(url_for('cardapio_user'))

@app.route("/excluir/<int:id>", methods=["POST"])
def excluir_comida(id):
    comida = Comidas.query.get(id)
    if comida:
        db.session.delete(comida)  # Exclui o item do banco
        db.session.commit()
    return redirect(url_for('cardapio_user'))

@app.route("/cardapio_cliente")
def cardapio_cliente():
    # Consulta todas as comidas cadastradas no banco
    comidas = Comidas.query.all()
    return render_template("cardapio_cliente.html", comidas=comidas)




# Rodando o servidor
if __name__ == '__main__':
    app.run(debug=True)
