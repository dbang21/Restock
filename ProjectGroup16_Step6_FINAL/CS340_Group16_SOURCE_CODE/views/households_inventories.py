from flask import Blueprint, render_template, redirect
from flask import request
import database.db_connector as db

view_households_inventories = Blueprint('view_households_inventories', __name__)


@view_households_inventories.route('/', methods=['POST', 'GET'])
def households_inventories():
    db_connection = db.connect_to_database()

    # Add a new item to a household
    if request.method == 'POST':
        if request.form.get('Add_Households_Inventories'):
            household = request.form['id_household']
            item = request.form['id_item']
            amount_left = request.form['amount_left']
            restock_status = request.form['restock_status']

            # No null inputs
            query = 'INSERT INTO Households_Inventories (id_household, id_item, amount_left, restock_status) VALUES (%s, %s, %s, %s);'
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(household, item, amount_left, restock_status))
            results = cursor.fetchall()
            db_connection.close()
            return redirect('/households-inventories')

    # View inventory by household
    if request.method == 'GET':
        household = request.args.get('household')
        if household is not None:
            # View one household inventory
            query = "SELECT Households_Inventories.id_household_inventory AS ID, Households.name AS Household, Households_Items.name AS Item, Households_Inventories.amount_left AS 'Amount Left', IF(restock_status=1, 'Restock', '') AS 'Restock Status' FROM Households_Inventories INNER JOIN Households ON Households.id_household = Households_Inventories.id_household INNER JOIN Households_Items ON Households_Items.id_item = Households_Inventories.id_item WHERE Households.id_household = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(household,))
            results = cursor.fetchall()
        else:
            # View all household inventory
            query = "SELECT Households_Inventories.id_household_inventory AS ID, Households.name AS Household, Households_Items.name AS Item, Households_Inventories.amount_left AS 'Amount Left', IF(restock_status=1, 'Restock', '') AS 'Restock Status' FROM Households_Inventories INNER JOIN Households ON Households.id_household = Households_Inventories.id_household INNER JOIN Households_Items ON Households_Items.id_item = Households_Inventories.id_item ORDER BY Households_Inventories.id_household_inventory ASC;"
            cursor = db.execute_query(db_connection=db_connection, query=query)
            results = cursor.fetchall()

        # View households
        query2 = "SELECT id_household, name FROM Households;"
        cursor = db.execute_query(db_connection=db_connection, query=query2)
        results2 = cursor.fetchall()

        # View households items
        query3 = "SELECT id_item, name FROM Households_Items;"
        cursor = db.execute_query(db_connection=db_connection, query=query3)
        results3 = cursor.fetchall()
        db_connection.close()
    
    return render_template("households-inventories.j2", households_inventories=results, household_dropdown=results2, items_dropdown=results3)


@view_households_inventories.route('/households-inventories-edit/<int:id>', methods=['POST', 'GET'])
def households_inventories_edit(id):
    db_connection = db.connect_to_database()

    # View selected household inventory
    if request.method == 'GET':
        query = "SELECT Households_Inventories.id_household_inventory AS ID, Households.name AS Household, Households_Items.name AS Item, Households_Inventories.amount_left AS 'Amount Left', IF(restock_status=1, 'Restock', '') AS 'Restock Status' FROM Households_Inventories INNER JOIN Households ON Households.id_household = Households_Inventories.id_household INNER JOIN Households_Items ON Households_Items.id_item = Households_Inventories.id_item WHERE id_household_inventory = %s ORDER BY Households_Inventories.id_household_inventory ASC;"
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(id,))
        results = cursor.fetchall()

        # View households
        query2 = "SELECT id_household, name FROM Households;"
        cursor = db.execute_query(db_connection=db_connection, query=query2)
        results2 = cursor.fetchall()
        db_connection.close()
        return render_template("households-inventories-edit.j2", households_inventories=results, household_dropdown=results2)
    
    # Update selected household inventory
    if request.method == 'POST':
        if request.form.get('Edit_Households_Inventories'):
            amount_left = request.form['amount_left']
            restock_status = request.form['restock_status']

            query = 'UPDATE Households_Inventories SET Households_Inventories.amount_left = %s, Households_Inventories.restock_status = %s WHERE id_household_inventory = %s;'
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(amount_left, restock_status, id))
            results = cursor.fetchall()
            db_connection.close()
            return redirect('/households-inventories')


@view_households_inventories.route('/households-inventories-delete/<int:id>')
def households_inventories_delete(id):
    db_connection = db.connect_to_database()

    query = "DELETE FROM Households_Inventories WHERE id_household_inventory = '%s';"
    db.execute_query(db_connection=db_connection, query=query, query_params=(id,))
    db_connection.close()
    return redirect('/households-inventories')