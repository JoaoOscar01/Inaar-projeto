from flask import Flask, render_template

# Criação da aplicação Flask
app = Flask(__name__)

# Definindo a rota
@app.route('/')
def home():
    return render_template("pagina1.html")

# Rodando o servidor
if __name__ == '__main__':
    app.run(debug=True)
