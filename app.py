# app.py
from flask import Flask, jsonify, request

app = Flask(__name__)

# Banco de dados em memória
tables = {}  # {'id': {'name': 'Nome da Tabela', 'data': [[...], [...]]}}
next_id = 1

# Rota para listar todas as tabelas
@app.route('/tables', methods=['GET'])
def get_tables():
    return jsonify(tables)

# Rota para criar uma nova tabela
@app.route('/tables', methods=['POST'])
def create_table():
    global next_id
    data = request.json
    table_name = data.get('name')
    table_data = data.get('data', [])
    
    if not table_name:
        return jsonify({'error': 'O nome da tabela é obrigatório'}), 400
    
    table_id = next_id
    tables[table_id] = {'name': table_name, 'data': table_data}
    next_id += 1
    return jsonify({'id': table_id, 'name': table_name, 'data': table_data}), 201

# Rota para atualizar uma tabela
@app.route('/tables/<int:table_id>', methods=['PUT'])
def update_table(table_id):
    if table_id not in tables:
        return jsonify({'error': 'Tabela não encontrada'}), 404
    
    data = request.json
    tables[table_id]['name'] = data.get('name', tables[table_id]['name'])
    tables[table_id]['data'] = data.get('data', tables[table_id]['data'])
    
    return jsonify(tables[table_id])

# Rota para deletar uma tabela
@app.route('/tables/<int:table_id>', methods=['DELETE'])
def delete_table(table_id):
    if table_id not in tables:
        return jsonify({'error': 'Tabela não encontrada'}), 404
    del tables[table_id]
    return jsonify({'message': 'Tabela deletada com sucesso'})

# Rota para obter uma tabela específica
@app.route('/tables/<int:table_id>', methods=['GET'])
def get_table(table_id):
    if table_id not in tables:
        return jsonify({'error': 'Tabela não encontrada'}), 404
    return jsonify(tables[table_id])

if __name__ == '__main__':
    app.run(debug=True)
