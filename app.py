import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'mjGoodFood'
app.config["MONGO_URI"] = os.environ.get('MONGO_URI', 'mongodb://localhost')

mongo = PyMongo(app)

@app.route('/')

@app.route('/get_recipes')
def get_recipes():
    return render_template("recipes.html",
    recipes=mongo.db.recipes.find())
    

    
@app.route('/add_recipe')
def add_recipe():
    return render_template('addrecipes.html',
    categories=mongo.db.categories.find())
    
    
@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes = mongo.db.recipes
    recipes.insert_one(request.form.to_dict())
    return redirect(url_for('get_recipes'))
    
    
@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    all_categories = mongo.db.categories.find()
    return render_template('editrecipe.html', recipe=the_recipe, catergories=all_categories)
    
    
@app.route('/update_recipe/<recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
    recipes = mongo.db.recipes
    recipes.update( {'_id': ObjectId(recipe_id)},
    {
        'recipe_name':request.form.get('recipe.name'),
        'category_name':request.form.get('category_name'),
        'recipe_description':request.form.get('recipe_description'),
        'recipe_ingredients':request.form.get('recipe_ingredients'),
        'recipe_method':request.form.get('recipe_method')
    })
    return redirect(url_for('get_recipes'))

    
@app.route('/delete.recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id':ObjectId(recipe_id)})
    return redirect(url_for('get_recipes'))
    

@app.route('/get_categories')
def get_categories():
    return render_template('categories.html',
    categories=mongo.db.categories.find())
    
    
@app.route('/delete_category/<category_id>')
def delete_category(category_id):
    mongo.db.categories.remove({'_id': ObjectId(category_id)})
    return redirect(url_for('get_categories'))
    
    
@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    return render_template('editcategory.html',
    category=mongo.db.categories.find_one({'_id': ObjectId(category_id)}))
    
    
@app.route('/update_category/<category_id>', methods=["POST"])
def update_category(category_id):
    mongo.db.categories.update({'_id': ObjectId(category_id)},
    {'category_name': request.form.get['category_name']})
    return redirect(url_for('get_categories'))
    
    
@app.route('/insert_category', methods=["POST"])
def insert_category():
    category_doc = {'category_name': request.form.get('category_name')}
    mongo.db.categories.insert_one(category_doc)
    return redirect(url_for('get_categories'))
    
    
@app.route('/add_category')
def add_category():
    return render_template('addcategory.html')

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)