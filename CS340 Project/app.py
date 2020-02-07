"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask
from flask import render_template as render
app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app


@app.route('/')
def index():
    return render("menu.html")

@app.route('/Items')
def Items():
    return render("Items.html")

@app.route('/Orders')
def Orders():
    return render("Orders.html")

@app.route('/Customers')
def Customers():
    return render("Customers.html")

@app.route('/Employees')
def Employees():
    return render("Employees.html")


if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
