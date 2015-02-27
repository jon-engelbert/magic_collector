from flask import Flask, Blueprint, render_template, redirect, url_for, request, flash, jsonify

app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#from database_setup import Base, Color, Card
# Import the database object from the main app module
from app.mod_color.models import Base, Color
from app.mod_card.models import Base, Card
from app import db

#engine = create_engine('sqlite:///colormenu.db')
#Base.metadata.bind = engine

#DBSession = sessionmaker(bind=engine)
DBSession = sessionmaker(bind=db)
session = DBSession()

mod_card = Blueprint('card', __name__, url_prefix='/card')

@mod_card.route('/cardu/<int:card_id>/JSON/')
def colorCardJSON(color_id, card_id):
    color = db.session.query(Color).filter_by(id=color_id).one()
    cards = db.session.query(Card).filter_by(color_id=color_id).all()
    return jsonify(cards[card_id].serialize)

@mod_card.route('/colors/<int:color_id>/')
@mod_card.route('/colors/<int:color_id>/menu')
def menu(color_id):
    color = db.session.query(Color).filter_by(id=color_id).one()
    cards = db.session.query(Card).filter_by(color_id=color.id)
    return render_template('card/cards.html', color=color, cards=cards)


# Task 1: Create route for newCard function here
@mod_card.route('/colors/<int:color_id>/new', methods=['GET', 'POST'])
def new(color_id):
    if request.method == 'POST':
        newItem = Card(name=request.form['name'], color_id=color_id)
        db.session.add(newItem)
        db.session.commit()
        flash("new menu card created")
        return redirect(url_for('card.menu', color_id=color_id))
    else:
        return render_template('card/newcarditem.html', color_id=color_id)


#Task 2: Create route for editCard function here
@mod_card.route('/colors/<int:color_id>/<int:card_id>/edit', methods=['GET', 'POST'])
def edit(color_id, card_id):
    editedItem = db.session.query(Card).filter_by(id=card_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        db.session.add(editedItem)
        db.session.commit()
        flash("menu card edited")
        return redirect(url_for('card.menu', color_id=color_id))
    else:
        return render_template('card/editcarditem.html', color_id=color_id, i=editedItem)


#Task 3: Create a route for deleteCard function here
@mod_card.route('/colors/<int:color_id>/<int:card_id>/delete', methods=['GET', 'POST'])
def delete(color_id, card_id):
    cardToDelete = db.session.query(Card).filter_by(id=card_id).one()
    if request.method == 'POST':
        db.session.delete(cardToDelete)
        db.session.commit()
        flash("menu card deleted")
        return redirect(url_for('card.menu', color_id=color_id))
    else:
        return render_template('card/deletecarditem.html', card=cardToDelete)

