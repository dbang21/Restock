from flask import Blueprint, render_template, redirect
from flask import request
import database.db_connector as db

view_households_members = Blueprint('view_households_members', __name__)

@view_households_members.route('/', methods=['POST', 'GET'])
def households_members():
    db_connection = db.connect_to_database()

    # Add a new household member
    if request.method == 'POST':
        if request.form.get('Add_Households_Members'):
            name = request.form['name']
            id_household = request.form['id_household']
            runner_status = request.form['runner_status']

            # Null household
            if id_household == "":
                query = 'INSERT INTO Households_Members (name, runner_status) VALUES (%s, %s);'
                cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(name, runner_status))
                results = cursor.fetchall()
                db_connection.close()
            # No null inputs
            else:
                query = 'INSERT INTO Households_Members (name, runner_status, id_household) VALUES (%s, %s, %s);'
                cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(name, runner_status, id_household))
                results = cursor.fetchall()
                db_connection.close()

            return redirect('/households-members')

    # View all households members
    if request.method == 'GET':
        query = "SELECT Households_Members.id_household_member AS ID, Households_Members.name AS Name, IF(runner_status=1, 'Dedicated Runner', '') AS 'Runner Status', Households.name AS Household FROM Households_Members LEFT JOIN Households ON Households_Members.id_household = Households.id_household;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()

        # View households
        query2 = "SELECT id_household, name FROM Households;"
        cursor = db.execute_query(db_connection=db_connection, query=query2)
        data = cursor.fetchall()
        db_connection.close()
        return render_template("households-members.j2", households_members=results, household_dropdown=data)


@view_households_members.route('/households-members-edit/<int:id>', methods=['POST', 'GET'])
def households_members_edit(id):
    db_connection = db.connect_to_database()

    # View selected household member
    if request.method == 'GET':
        query = 'SELECT Households_Members.id_household_member AS ID, Households_Members.name AS Name, Households.id_household AS Household, runner_status as "Runner Status" FROM Households_Members LEFT JOIN Households ON Households_Members.id_household = Households.id_household WHERE id_household_member = %s;' % (id)
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        
        # View households
        query2 = "SELECT id_household, name FROM Households;"
        cursor = db.execute_query(db_connection=db_connection, query=query2)
        results2 = cursor.fetchall()
        db_connection.close()
        return render_template("households-members-edit.j2", households_members=results, household_dropdown=results2)
    
    # Update selected household member
    if request.method == 'POST':
        if request.form.get('Edit_Households_Members'):
            name = request.form['name']
            id_household = request.form['id_household']
            runner_status = request.form['runner_status']

            # # All null inputs
            # if id_household == "" and name == "" and runner_status == "":
            #     return redirect('/households-members')
            # # Update id_household only
            # elif name == "" and runner_status == "":
            #     query = 'UPDATE Households_Members SET Households_Members.id_household = %s WHERE id_household_member = %s;'
            #     cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(id_household, id))
            #     results = cursor.fetchall()
            # # Update name only
            # elif id_household == "" and runner_status == "":
            #     query = 'UPDATE Households_Members SET Households_Members.name = %s WHERE id_household_member = %s;'
            #     cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(name, id))
            #     results = cursor.fetchall()
            # # Update runner_status only
            # elif id_household == "" and name == "":
            #     query = 'UPDATE Households_Members SET Households_Members.runner_status = %s WHERE id_household_member = %s;'
            #     cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(runner_status, id))
            #     results = cursor.fetchall()
            # Null household
            if id_household == "" or 0:
                query = 'UPDATE Households_Members SET Households_Members.name = %s, Households_Members.runner_status = %s, Households_Members.id_household = NULL WHERE id_household_member = %s;'
                cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(name, runner_status, id))
                results = cursor.fetchall()      
                db_connection.close()      
            # # Null name
            # elif name == "":
            #     query = 'UPDATE Households_Members SET Households_Members.id_household = %s, Households_Members.runner_status = %s WHERE id_household_member = %s;'
            #     cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(id_household, runner_status, id))
            #     results = cursor.fetchall()
            # # Null runner status
            # elif runner_status == "":
            #     query = 'UPDATE Households_Members SET Households_Members.name = %s, Households_Members.id_household = %s WHERE id_household_member = %s;'
            #     cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(name, id_household, id))
            #     results = cursor.fetchall()
            # No null inputs
            else:
                query = 'UPDATE Households_Members SET Households_Members.name = %s, Households_Members.id_household = %s, Households_Members.runner_status = %s WHERE id_household_member = %s;'
                cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(name, id_household, runner_status, id))
                results = cursor.fetchall()
                db_connection.close()

            return redirect('/households-members')


# Delete by ID only
@view_households_members.route('/households-members-delete/<int:id>')
def households_members_delete(id):
    db_connection = db.connect_to_database()

    query = 'DELETE FROM Households_Members WHERE id_household_member = "%s";'
    db.execute_query(db_connection=db_connection, query=query, query_params=(id,))
    db_connection.close()
    return redirect('/households-members')