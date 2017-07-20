from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item

app = Flask(__name__)

engine = create_engine('sqlite:///categoryitem.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/categories')
def showCategories():
  categories = session.query(Category).all()
  lasttenitems = session.query(Item).order_by(Item.id.desc()).limit(10)
  return render_template('categories.html', categories = categories, lasttenitems = lasttenitems)

@app.route('/categories/JSON')
def showCategoriesJSON():
  categories = session.query(Category).all()
  return jsonify(Categories = [c.serialize for c in categories])

@app.route('/category/new', methods = ['GET', 'POST'])
def newCategory():
  if request.method == 'POST':
    newCategory = Category(
      name = request.form['name'])
    session.add(newCategory)
    session.commit()
    flash("New category created")
    return redirect(url_for('showCategories'))
  else:
    return render_template('newcategory.html')

@app.route('/category/<string:category_name>/edit', methods = ['GET', 'POST'])
def editCategory(category_name):
  categoryToEdit = session.query(Category).filter_by(name = category_name).one()
  if request.method == 'POST':
    if request.form['name']:
      categoryToEdit.name = request.form['name']
    session.add(categoryToEdit)
    session.commit()
    flash("Category successfully edited")
    return redirect(url_for('showCategories'))
  else:
    return render_template('editcategory.html', category_name = category_name, category = categoryToEdit)

@app.route('/category/<string:category_name>/delete', methods = ['GET', 'POST'])
def deleteCategory(category_name):
  categoryToDelete = session.query(Category).filter_by(name = category_name).one()
  if request.method == 'POST':
    session.delete(categoryToDelete)
    session.commit()
    flash("Category successfully deleted")
    return redirect(url_for('showCategories'))
  else:
    return render_template('deletecategory.html', category_name = category_name, category = categoryToDelete)

@app.route('/category/<string:category_name>/')
@app.route('/category/<string:category_name>/items')
def showItemsInCategory(category_name):
  category = session.query(Category).filter_by(name = category_name).one()
  items = session.query(Item).filter_by(category_id = category.id).all()
  return render_template('categoryitems.html', category = category, items = items)

@app.route('/category/<string:category_name>/JSON')
def showItemsInCategoryJSON(category_name):
  category = session.query(Category).filter_by(name = category_name).one()
  items = session.query(Item).filter_by(category_id = category.id).all()
  return jsonify(Items = [i.serialize for i in items])

@app.route('/category/<string:category_name>/<string:item_name>')
def showItem(category_name, item_name):
  category = session.query(Category).filter_by(name = category_name).one()
  item = session.query(Item).filter_by(category = category).filter_by(name = item_name).one()
  return render_template('item.html', category = category, item = item)

@app.route('/category/<string:category_name>/<string:item_name>/JSON')
def showItemJSON(category_name, item_name):
  category = session.query(Category).filter_by(name = category_name).one()
  item = session.query(Item).filter_by(category = category).filter_by(name = item_name).one()
  return jsonify(Item = [item.serialize])

@app.route('/category/<string:category_name>/new', methods = ['GET', 'POST'])
def newItem(category_name):
  category = session.query(Category).filter_by(name = category_name).one()
  if request.method == 'POST':
    newItem = Item(
      name = request.form['name'],
      description = request.form['description'],
      category = category)
    session.add(newItem)
    session.commit()
    flash("New category created")
    return redirect(url_for('showItemsInCategory', category_name = category_name))
  else:
    return render_template('newitem.html', category_name = category_name)

@app.route('/category/<string:category_name>/<string:item_name>/edit', methods = ['GET', 'POST'])
def editItem(category_name, item_name):
  category = session.query(Category).filter_by(name = category_name).one()
  itemToEdit = session.query(Item).filter_by(category = category).filter_by(name = item_name).one()
  if request.method == 'POST':
    if request.form['name']:
      itemToEdit.name = request.form['name']
    if request.form['description']:
      itemToEdit.name = request.form['description']
    session.add(categoryToEdit)
    session.commit()
    flash("Item successfully edited")
    return redirect(url_for('showItemsInCategory', category_name = category_name))
  else:
    return render_template('edititem.html',category_name = category_name, item_name = item_name)

@app.route('/category/<string:category_name>/<string:item_name>/delete', methods = ['GET', 'POST'])
def deleteItem(category_name, item_name):
  category = session.query(Category).filter_by(name = category_name).one()
  itemToDelete = session.query(Item).filter_by(category = category).filter_by(name = item_name).one()
  if request.method == 'POST':
    session.delete(itemToDelete)
    session.commit()
    flash("Item successfully deleted")
    return redirect(url_for('showItemsInCategory', category_name = category_name))         
  else:
    return render_template('deleteitem.html',category_name = category_name, item_name = item_name)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
