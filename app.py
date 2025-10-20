import sqlite3
from flask import Flask, render_template, request, redirect, flash
import os
from dotenv import load_dotenv 
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///financeiro.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)

class Categoria(db.Model):
    id = db.Column(db.Interger, primary_key = True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    
    transacoes = db.relationship('Transacao', backref='categoria', lazy=True)

class Transacao(db.Model):
    id = db.Column(db.Intergrer, primary_key=True)
    descricao = db.Column(db.String(200))

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
    flash('Transação adicionada com sucesso!', 'success')
    return redirect('/')

@app.route('/delete/<int:id>', methods=['POST'])
def delete_transaction(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM transacoes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Transação apagada com sucesso!', 'success')
    return redirect('/')

@app.route('/edit/<int:id>')
def edit_transaction(id):
    conn = get_db_connection()
    transacao = conn.execute('SELECT * FROM transacoes WHERE id = ?', (id,)).fetchone()
    categorias = conn.execute('SELECT * FROM categorias ORDER BY nome').fetchall()
    conn.close()
    return render_template('edit.html', transacao=transacao, categorias=categorias)

@app.route('/update/<int:id>', methods=['POST'])
def update_transaction(id):
    descricao = request.form['descricao']
    valor = request.form['valor']
    data = request.form['data']
    tipo = request.form['tipo']
    categoria_id = request.form['categoria_id']

    conn = get_db_connection()
    conn.execute('UPDATE transacoes SET descricao = ?, valor = ?, data = ?, tipo = ?, categoria_id = ? WHERE id = ?',
                (descricao, valor, data, tipo, categoria_id, id))
    conn.commit()
    conn.close()

    flash('Transação atualizada com sucesso!', 'success')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)