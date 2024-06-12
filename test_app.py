import pytest
from app import app, recipes_collection
from bson.objectid import ObjectId

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            recipes_collection.delete_many({})
            recipes_collection.insert_many([
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
            ])
            yield client

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Recipes' in response.data

def test_add_recipe(client):
    new_recipe = {
        'name': 'Tomato Soup',
        'ingredients': 'Tomatoes, Onion, Garlic, Olive Oil, Salt, Pepper',
        'instructions': 'Cook all ingredients together. Blend until smooth.'
    }
    response = client.post('/add', data=new_recipe, follow_redirects=True)
    assert response.status_code == 200
    assert b'Tomato Soup' in response.data

def test_update_recipe(client):
    recipe = recipes_collection.find_one({'name': 'Pasta'})
    update_data = {
        'name': 'Spaghetti',
        'ingredients': 'ALOT OF PEPER JAJAJA !!! Tomatoes, Onion, Garlic, Olive Oil, Salt, Pepper',
        'instructions': 'Cook all ingredients together. Blend until smooth.'
    }
    response = client.post(f'/update/{recipe["_id"]}', data=update_data, follow_redirects=True)
    assert response.status_code == 200
    assert b'Spaghetti' in response.data

def test_delete_recipe(client):
    recipe = recipes_collection.find_one({'name': 'Pasta'})
    response = client.post(f'/delete/{recipe["_id"]}', follow_redirects=True)
    assert response.status_code == 200
    assert b'Pasta' not in response.data