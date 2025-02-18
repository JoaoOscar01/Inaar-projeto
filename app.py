from flask import Flask

# Criação da aplicação Flask
app = Flask(__name__)

# Definindo a rota
@app.route('/')
def home():
    return '<h1>Iniciando projeto</h1>'

# Rodando o servidor
if __name__ == '__main__':
    app.run(debug=True)
