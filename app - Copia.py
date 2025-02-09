from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Criar o banco de dados SQLite
def criar_banco():
    conn = sqlite3.connect("financas.db")
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

# Criar a tabela ao iniciar o app
criar_banco()

# Rota para receber lançamentos
@app.route('/lancamentos', methods=['POST'])
def adicionar_lancamento():
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Nenhum dado recebido"}), 400

    conn = sqlite3.connect("financas.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO lancamentos (data, tipo, valor, descricao, categoria) VALUES (?, ?, ?, ?, ?)",
                   (dados["data"], dados["tipo"], dados["valor"], dados["descricao"], dados["categoria"]))
    conn.commit()
    conn.close()

    return jsonify({"mensagem": "Lançamento registrado com sucesso!"})

# Rota para listar todos os lançamentos com melhor formatação
@app.route('/lancamentos', methods=['GET'])
def listar_lancamentos():
    conn = sqlite3.connect("financas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM lancamentos")
    dados = cursor.fetchall()
    conn.close()

    # Convertendo para JSON estruturado
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

    return jsonify(lancamentos)


# Iniciar o servidor Flask
if __name__ == '__main__':
    app.run(debug=True)
