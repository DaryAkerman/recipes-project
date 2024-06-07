from flask import Flask, request, render_template, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://mongo:27017/')
db = client.recipes_db
recipes_collection = db.recipes

@app.route('/')
def index():
    recipes = recipes_collection.find()
    return render_template('index.html', recipes=recipes)

@app.route('/add', methods=['POST'])
def add_recipe():
    recipe = {
        'name': request.form['name'],
        'ingredients': request.form['ingredients'],
        'instructions': request.form['instructions']
    }
    recipes_collection.insert_one(recipe)
    return redirect(url_for('index'))

@app.route('/update/<id>', methods=['POST'])
def update_recipe(id):
    recipes_collection.update_one(
        {'_id': ObjectId(id)},
        {'$set': {
            'name': request.form['name'],
            'ingredients': request.form['ingredients'],
            'instructions': request.form['instructions']
        }}
    )
    return redirect(url_for('index'))

@app.route('/delete/<id>', methods=['POST'])
def delete_recipe(id):
    recipes_collection.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
