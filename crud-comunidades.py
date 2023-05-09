from flask import Flask, redirect, url_for
import database as db
from random import randint 
from datetime import datetime

app = Flask(__name__)

#Ruta crear comunidad
@app.route('/create_community', methods=['POST'])
def create_community(name, description):
    id_community = randint(0,100)
    created_at = datetime.now()

     if name and description and id_community and created_at:
        cursor = db.database.cursor()
        sql = 'INSERT INTO community (id_community, name, description, created_at) VALUES (%s, %s, %s, %s)'
        data = (str(id_community), name, description, created_at)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect (url_for('create_community'))

#Ruta eliminar comunidad
@app.route('/delete_community/<string:id>', methods=['DELETE'])
def delete_community(id):
    cursor = db.database.cursor()
    sql = 'DELETE FROM community WHERE id_community=%s'
    data = (id)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect (url_for('delete_community'))

#Ruta para editar comunidad
@app.route('edit_community/<string:id>', methods=['PUT'])
def edit_community(id, name, description):
    if name and description:
        cursor = db.database.cursor()
        sql = 'UPDATE community SET name=%s, description=%s WHERE id=%s'
        data = (name, description, str(id))
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('edit_community'))





    

