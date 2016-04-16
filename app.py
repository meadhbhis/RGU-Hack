""" app.py
Main server file for application.
"""
import csv
import sqlite3

from flask import Flask, request, g, redirect, render_template, url_for, abort

app = Flask(__name__)
imd = {}
DATABASE = 'users.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

with open('postcode.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        #rank, vigintile, population, location name
        imd[row[0].lower().replace(' ', '')] = (row[2], row[5], row[10], row[15])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/postcode-posted', methods=['POST'])
def posted():
    postcode = request.form['postcode'].lower().replace(' ', '')
    print postcode
    try:
        imd[postcode]
        c = get_db().cursor()
        c.execute("INSERT INTO postcodes VALUES (?,?,?,?,?,?)", (None, request.form['name'], postcode, imd[postcode][0], imd[postcode][1], imd[postcode][2]))
        get_db().commit()
        return redirect(url_for('postcode', code=postcode))
    except KeyError:
        abort(404)

@app.route('/postcode/<code>')
def postcode(code):
    input_dict = {'postcode': code, 'rank': imd[code][0], 'vigintile': imd[code][1], 'population': imd[code][2], 'name': imd[code][3]}
    return render_template('postcode.html', input=input_dict)

<<<<<<< HEAD
@app.route('/compare/<code>')
def compare(code):
	input_dict = {'postcode': code, 'rank': imd[code][0], 'vigintile': imd[code][1], 'population': imd[code][2], 'name': imd[code][3]}
	return render_template('comparison.html', input=input_dict)

=======
@app.route('/compare/')
def compare():
    return render_template('comparison.html')
>>>>>>> ab879a27fe1101217a6294077ce3db8f31ac52e5
@app.errorhandler(404)
def not_found(e):
    return "Ye've daen summin wrang here pal", 404

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run(debug=True)
