from flask import Blueprint, render_template, redirect
from flask import request
import database.db_connector as db

view_stores_inventories = Blueprint('view_stores_inventories', __name__)

@view_stores_inventories.route("/", methods=["POST", "GET"])
def stores_inventories():
    db_connection = db.connect_to_database()

    # Add store inventory
    if request.method == 'POST':
        if request.form.get("Add_Stores_Inventories"):
            id_item_type = request.form["id_item_type"]
            id_store = request.form["id_store"]

            # No null inputs
            query = "INSERT INTO Stores_Inventories (id_item_type, id_store) VALUES (%s, %s)"
            cur = db.execute_query(db_connection=db_connection, query=query, query_params=(id_item_type, id_store))
            results = cur.fetchall()
            db_connection.close()
            return redirect("/stores-inventories")

    # View store inventory
    if request.method == 'GET':
        query = "SELECT Items_Types.name AS 'Item Type', Stores.name AS Store FROM Stores_Inventories INNER JOIN Items_Types ON Items_Types.id_item_type = Stores_Inventories.id_item_type INNER JOIN Stores ON Stores.id_store = Stores_Inventories.id_store;"
        cur = db.execute_query(db_connection=db_connection, query=query)
        results = cur.fetchall()

        # View item types
        query2 = "SELECT Items_Types.id_item_type, name FROM Items_Types;"
        cursor = db.execute_query(db_connection=db_connection, query=query2)
        results2 = cursor.fetchall()

        # View stores
        query3 = "SELECT Stores.id_store, name FROM Stores;"
        cursor = db.execute_query(db_connection=db_connection, query=query3)
        results3 = cursor.fetchall()
        db_connection.close()

    return render_template("stores-inventories.j2", stores_inventories=results, items_types_dropdown=results2, stores_dropdown=results3)


# @view_stores_inventories.route("/stores-inventories-delete/<int:id>")
# def stores_inventories_delete(id):
#     db_connection = db.connect_to_database()
#     query = "DELETE FROM Stores_Inventories WHERE id_item_type = '%s';"
#     db.execute_query(db_connection=db_connection, query=query, query_params=(id,))
#     return redirect("/stores-inventories")