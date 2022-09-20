from flask import Blueprint, render_template, redirect
from flask import request
import database.db_connector as db

view_items_types = Blueprint('view_items_types', __name__)

@view_items_types.route("/", methods=["POST", "GET"])
def items_types():
    db_connection = db.connect_to_database()
    
    # Add a new item type
    if request.method == 'POST':
        if request.form.get("Add_Items_Types"):
            name = request.form["name"]
            
            # No null inputs
            query = "INSERT INTO Items_Types (name) VALUES (%s)"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(name,))
            results = cursor.fetchall()
            db_connection.close()
        
            return redirect("/items-types")

    # View item types
    if request.method == 'GET':
        query = 'SELECT Items_Types.id_item_type AS ID, name AS "Item Type" FROM Items_Types;'
        cur = db.execute_query(db_connection=db_connection, query=query)
        db_connection.close()
        results = cur.fetchall()

    return render_template("items-types.j2", items_types=results)


@view_items_types.route("/items-types-edit/<int:id>", methods=["POST", "GET"])
def items_types_edit(id):
    db_connection = db.connect_to_database()

    # View selected item type
    if request.method == "GET":
        query = "SELECT Items_Types.name FROM Items_Types WHERE id_item_type = %s;" % (id)
        cur = db.execute_query(db_connection=db_connection, query=query)
        results = cur.fetchall()

        # View stores
        query2 = "SELECT id_store, name FROM Stores;"
        cur = db.execute_query(db_connection=db_connection, query=query2)
        results2 = cur.fetchall()
        db_connection.close()

        return render_template("items-types-edit.j2", items_types=results, stores_dropdown=results2)

    # Update selected item type
    if request.method == "POST":
        if request.form.get("Edit_Items_Types"):
            name = request.form["name"]

            # No null inputs
            query = "UPDATE Items_Types SET name = %s WHERE id_item_type = %s;"
            cur = db.execute_query(db_connection=db_connection, query=query, query_params=(name, id))
            results = cur.fetchall()
            db_connection.close()

            return redirect("/items-types")


@view_items_types.route("/items-types-delete/<int:id>")
def items_types_delete(id):
    db_connection = db.connect_to_database()

    query = "DELETE FROM Items_Types WHERE id_item_type = '%s';"
    db.execute_query(db_connection=db_connection, query=query, query_params=(id,))
    db_connection.close()
    return redirect("/items-types")