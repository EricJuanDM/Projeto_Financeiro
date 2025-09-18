import sqlite3
from flask import Flask, render_template, request, redirect, flash


app = Flask(__name__)
app.secret_key = '1234'


def get_db_connection():
    conn = sqlite3.connect('financeiro.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    conn = get_db_connection()

    transacoes = conn.execute('SELECT * FROM transacoes ORDER BY data DESC').fetchall()

    categorias = conn.execute('SELECT * FROM categorias ORDER BY nome').fetchall()

    saldo = 0
    for t in transacoes:
        if t['tipo'] == 'receita':
            saldo += t['valor']
        else:
            saldo -= t['valor']

    conn.close()

    return render_template('index.html', transacoes=transacoes, saldo=saldo, categorias=categorias)

@app.route('/add', methods=['POST'])
def add_transaction():
    descricao = request.form['descricao']
    valor = request.form['valor']
    data = request.form['data']
    tipo = request.form['tipo']
    categoria_id = request.form['categoria_id']

    conn = get_db_connection()
    conn.execute('INSERT INTO transacoes (descricao, valor, data, tipo, categoria_id) VALUES (?, ?, ?, ?, ?)',
                (descricao, valor, data, tipo, categoria_id))
    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/delete/<int:id>', methods=['POST'])
def delete_transaction(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM transacoes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)