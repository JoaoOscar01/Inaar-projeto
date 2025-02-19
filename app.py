from flask import Flask, render_template

# Criação da aplicação Flask
app = Flask(__name__)

# Definindo a rota de telas
@app.route('/')
def home():
    return render_template("pagina1.html")


@app.route("/cadastrar")
def cadastro_comida():
        return render_template("cadastrar_comida.html")

# Rodando o servidor
if __name__ == '__main__':
    app.run(debug=True)
