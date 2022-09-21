from flask import Flask, render_template, redirect
import os
import database.db_connector as db

from views.households import view_households
from views.households_members import view_households_members
from views.households_inventories import view_households_inventories
from views.households_items import view_households_items
from views.items_types import view_items_types
from views.stores_inventories import view_stores_inventories
from views.stores import view_stores

app = Flask(__name__)
db.connect_to_database()

app.register_blueprint(view_households, url_prefix='/households')
app.register_blueprint(view_households_members, url_prefix='/households-members')
app.register_blueprint(view_households_inventories, url_prefix='/households-inventories')
app.register_blueprint(view_households_items, url_prefix='/households-items')
app.register_blueprint(view_items_types, url_prefix='/items-types')
app.register_blueprint(view_stores_inventories, url_prefix='/stores-inventories')
app.register_blueprint(view_stores, url_prefix='/stores')

# Defining the app's routes
@app.route('/')
def root():
    return redirect('/index.html')
    
@app.route('/index.html')
def index():
    return render_template('index.j2')

# Listening for the port
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 10061))
    app.run(port=port, debug=True)
