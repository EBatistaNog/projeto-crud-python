from flask import Flask, render_template, request, redirect, url_for, jsonify
from conexao import conectar

app = Flask(__name__)

@app.route('/')
def home():
    try:
        busca_get = request.args.get('busca', '').strip()
        conn = conectar()
        cursor = conn.cursor(dictionary=True)

        if busca_get != '':
            sql = "SELECT * FROM clientes where nome like %s or email like %s or telefone like %s order by id desc"
            valor_busca = f'%{busca_get}%'
            cursor.execute(sql, (valor_busca, valor_busca, valor_busca))
        else:
            cursor.execute("SELECT * FROM clientes order by id desc")

        clientes = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return render_template('index.html', clientes=clientes, busca = busca_get)      
    
    except Exception as e:
        return f'Erro ao conectar: {e}'


@app.route('/salvar', methods=['POST'])
def salvar():
    id = request.form['id']
    nome = request.form['nome']
    email = request.form['email']
    telefone = request.form['telefone']
    data_cadastro = request.form['data_cadastro'] or None

    conn = conectar()
    cursor = conn.cursor()
    if id:
        cursor.execute("UPDATE clientes SET nome = %s, email = %s, telefone = %s, data_cadastro = %s WHERE id = %s", (nome, email, telefone, data_cadastro, id))
    else:
        cursor.execute("INSERT INTO clientes (nome, email, telefone, data_cadastro) VALUES (%s, %s, %s, %s)", (nome, email, telefone, data_cadastro))   
    conn.commit()
    cursor.close()
    conn.close()
        
    return redirect(url_for('home'))



@app.route('/buscar_cliente/<int:id>')
def editar(id): 
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM clientes where id = %s", (id,))
    cliente = cursor.fetchone()
    cursor.close()
    conn.close()

    if cliente['data_cadastro']:
        cliente['data_cadastro'] = cliente['data_cadastro'].strftime('%Y-%m-%d')


    return jsonify(cliente) 



@app.route('/excluir/<int:id>')
def excluir(id): 
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM clientes where id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
   
    return redirect(url_for('home')) 

#Verifica se o arquivo está sendo executado diretamente
if __name__ == '__main__':
    app.run(debug=True)
