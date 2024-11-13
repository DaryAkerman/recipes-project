from flask import Flask, request, render_template, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)
client = MongoClient(os.getenv('MONGO_URI'))
db = client.recipes_db
recipes_collection = db.recipes

default_recipes = [
    {
        'name': 'Pasta',
        'ingredients': 'Pasta, Tomato Sauce, Olive Oil, Garlic, Basil',
        'instructions': 'Boil pasta. Heat sauce with olive oil and garlic. Mix with pasta and garnish with basil.'
    },
    {
        'name': 'Chicken Salad',
        'ingredients': 'Chicken, Lettuce, Tomato, Cucumber, Olive Oil, Lemon Juice',
        'instructions': 'Cook chicken. Mix with chopped vegetables. Dress with olive oil and lemon juice.'
    },
    {
        'name': 'Chocolate Cake',
        'ingredients': 'Flour, Sugar, Cocoa Powder, Baking Powder, Eggs, Milk, Butter',
        'instructions': 'Mix dry ingredients. Add eggs, milk, and butter. Bake at 350°F for 30 minutes.'
    }
]

if recipes_collection.count_documents({}) == 0:
    recipes_collection.insert_many(default_recipes)

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
    app.run(host='0.0.0.0', port=5000, debug=True)
