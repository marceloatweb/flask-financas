from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # Garante que o JSON seja exibido corretamente com acentos

# Criar o banco de dados SQLite
def criar_banco():
    conn = sqlite3.connect("financas.db")
    conn.execute("PRAGMA encoding = 'UTF-8'")  # Força o banco a trabalhar com UTF-8
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lancamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            tipo TEXT NOT NULL,
            valor REAL NOT NULL,
            descricao TEXT NOT NULL,
            categoria TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

criar_banco()

# Rota para adicionar um lançamento
@app.route('/lancamentos', methods=['POST'])
def adicionar_lancamento():
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Nenhum dado recebido"}), 400

    conn = sqlite3.connect("financas.db")
    conn.text_factory = str  # Garante que os textos sejam armazenados corretamente
    cursor = conn.cursor()
    cursor.execute("INSERT INTO lancamentos (data, tipo, valor, descricao, categoria) VALUES (?, ?, ?, ?, ?)",
                   (dados["data"], dados["tipo"], dados["valor"], dados["descricao"], dados["categoria"]))
    conn.commit()
    conn.close()

    return jsonify({"mensagem": "Lançamento registrado com sucesso!"})

# Rota para listar todos os lançamentos
@app.route('/lancamentos', methods=['GET'])
def listar_lancamentos():
    conn = sqlite3.connect("financas.db")
    conn.text_factory = str  # Garante a recuperação correta dos textos
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM lancamentos")
    dados = cursor.fetchall()
    conn.close()

    lancamentos = []
    for lancamento in dados:
        lancamentos.append({
            "id": lancamento[0],
            "data": lancamento[1],
            "tipo": lancamento[2],
            "valor": lancamento[3],
            "descricao": lancamento[4],
            "categoria": lancamento[5]
        })

    # Retorna JSON com UTF-8 forçado
    return jsonify(lancamentos), 200, {'Content-Type': 'application/json; charset=utf-8'}


# Iniciar o servidor Flask
import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Render define a porta automaticamente
    app.run(host='0.0.0.0', port=port, debug=True)
