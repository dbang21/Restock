from flask import Blueprint, render_template, redirect
from flask import request
import database.db_connector as db

view_stores = Blueprint('view_stores', __name__)

# route for Stores page
@view_stores.route("/", methods=["POST", "GET"])
def stores():
    db_connection = db.connect_to_database()
    # Separate out the request methods, in this case this is for a POST
    # CREATE: insert a store into the Stores entity
    if request.method == 'POST':
        # fire off if user presses the Add Store button
        if request.form.get("Add_Stores"):
            # grab user form inputs
            name = request.form["name"]
            address = request.form["address"]
            hours_open = request.form["hours_open"]

            # account for null hours_open
            if hours_open == "":
                query = "INSERT INTO Stores (name, address) VALUES (%s, %s)"
                cur = db.execute_query(db_connection=db_connection, query=query, query_params=(name, address))
                results = cur.fetchall()
                db_connection.close()

            # no null inputs
            else:
                query = "INSERT INTO Stores (name, address, hours_open) VALUES (%s, %s, %s)"
                cur = db.execute_query(db_connection=db_connection, query=query, query_params=(name, address, hours_open))
                results = cur.fetchall()
                db_connection.close()
            # redirect back to stores page
            return redirect("/stores")

    # READ: Grab Stores data so we send it to our template to display
    if request.method == 'GET':
        query = 'SELECT Stores.id_store AS ID, Stores.name AS Name, Stores.address AS Address, Stores.hours_open AS "Hours Open" FROM Stores;'
        cur = db.execute_query(db_connection=db_connection, query=query)
        results = cur.fetchall()

    return render_template("stores.j2", stores=results)

# Stores DELETE route
# we want to pass the 'id' value of that person on button click (see HTML) via the route
@view_stores.route("/stores-delete/<int:id>")
def stores_delete(id):
    db_connection = db.connect_to_database()
    # mySQL query to delete the store with our passed id
    query = "DELETE FROM Stores WHERE id_store = '%s';"
    db.execute_query(db_connection=db_connection, query=query, query_params=(id,))
    db_connection.close()

    # redirect back to stores page
    return redirect("/stores")

# Stores UPDATE route
# similar to our delete route, we want to the pass the 'id' value of that store on button click (see HTML) via the route
@view_stores.route("/stores-edit/<int:id>", methods=["POST", "GET"])
def stores_edit(id):
    db_connection = db.connect_to_database()
    if request.method == "GET":
        # mySQL query to grab the info of the store with our passed id
        query = "SELECT Stores.id_store AS ID, Stores.name AS Name, Stores.address AS Address, Stores.hours_open AS 'Hours Open' FROM Stores WHERE id_store = %s" % (id)
        cur = db.execute_query(db_connection=db_connection, query=query)
        results = cur.fetchall()

        # mySQL query to grab store id/name data for our dropdown
        query2 = "SELECT id_store, name FROM Stores"
        cur = db.execute_query(db_connection=db_connection, query=query2)
        results2 = cur.fetchall()
        db_connection.close()

        # render stores-edit page passing our query data and Stores data to the stores-edit template
        return render_template("stores-edit.j2", stores=results, stores_dropdown=results2)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user presses the Edit Store button
        if request.form.get("Edit_Stores"):
            # grab user form inputs
            name = request.form["name"]
            address = request.form["address"]
            hours_open = request.form["hours_open"]

            # account for null hours_open
            if hours_open == "":
                query = "UPDATE Stores SET name = %s, address = %s, hours_open = NULL WHERE id_store = %s;"
                cur = db.execute_query(db_connection=db_connection, query=query, query_params=(name, address, id))
                results = cur.fetchall()
                db_connection.close()

            # no null inputs
            else:
                query = "UPDATE Stores SET name = %s, address = %s, hours_open = %s WHERE id_store = %s;"
                cur = db.execute_query(db_connection=db_connection, query=query, query_params=(name, address, hours_open, id))
                results = cur.fetchall()
                db_connection.close()

            # redirect back to stores page
            return redirect("/stores")