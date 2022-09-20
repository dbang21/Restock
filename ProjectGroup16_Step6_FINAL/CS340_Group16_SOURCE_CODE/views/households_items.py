from flask import Blueprint, render_template, redirect
from flask import request
import database.db_connector as db

view_households_items = Blueprint('view_households_items', __name__)

@view_households_items.route('/', methods=['POST', 'GET'])
def households_items():
    db_connection = db.connect_to_database()

    # Add a new household item
    if request.method == 'POST':
        if request.form.get('Add_Households_Items'):
            item_type = request.form['item_type']
            name = request.form['name']
            best_if_used_by = request.form['best_if_used_by']

            # No null inputs
            query = 'INSERT INTO Households_Items (id_item_type, name, best_if_used_by) VALUES (%s, %s, %s);'
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(item_type, name, best_if_used_by))
            results = cursor.fetchall()
            db_connection.close()
            return redirect('/households-items')

    # View household items
    if request.method == 'GET':
        query = "SELECT Households_Items.id_item AS ID, Items_Types.name AS 'Item Type', Households_Items.name AS Name, Households_Items.best_if_used_by AS 'Best If Used By' FROM Households_Items INNER JOIN Items_Types ON Items_Types.id_item_type = Households_Items.id_item_type;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()

        # View item types
        query2 = "SELECT Items_Types.id_item_type, name FROM Items_Types;"
        cursor = db.execute_query(db_connection=db_connection, query=query2)
        results2 = cursor.fetchall()
        db_connection.close()

    return render_template("households-items.j2", households_items=results, items_types_dropdown=results2)


@view_households_items.route('/households-items-edit/<int:id>', methods=['POST', 'GET'])
def households_items_edit(id):
    db_connection = db.connect_to_database()

    # View selected household item
    if request.method == 'GET':
        query = "SELECT Households_Items.id_item AS ID, Items_Types.name AS 'Item Type', Households_Items.name AS Name, Households_Items.best_if_used_by AS 'Best If Used By' FROM Households_Items INNER JOIN Items_Types ON Items_Types.id_item_type = Households_Items.id_item_type WHERE id_item = %s;"
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(id,))
        results = cursor.fetchall()
        
        # View item types
        query2 = "SELECT Items_Types.id_item_type, name FROM Items_Types;"
        cursor = db.execute_query(db_connection=db_connection, query=query2)
        results2 = cursor.fetchall()
        db_connection.close()
        return render_template("households-items-edit.j2", households_items=results, items_dropdown=results2)
    
    # Update selected household item
    if request.method == 'POST':
        if request.form.get('Edit_Households_Items'):
            id_item_type = request.form['id_item_type']
            name = request.form['name']
            best_if_used_by = request.form['best_if_used_by']
            
            # No null inputs
            query = 'UPDATE Households_Items SET id_item_type = %s, SET name = %s, SET best_if_used_by = %s WHERE id_item = %s;'
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(id_item_type, name, best_if_used_by, id))
            results = cursor.fetchall()
            db_connection.close()
            return redirect('/households-items')


@view_households_items.route('/households-items-delete/<int:id>')
def households_items_delete(id):
    db_connection = db.connect_to_database()

    query = "DELETE FROM Households_Items WHERE id_item = '%s';"
    db.execute_query(db_connection=db_connection, query=query, query_params=(id,))
    db_connection.close()
    return redirect('/households-items')