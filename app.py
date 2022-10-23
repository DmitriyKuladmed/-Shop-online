from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import *
from datetime import datetime
from cloudipsp import Api, Checkout

api = Api(merchant_id=1396424,
          secret_key='test')
checkout = Checkout(api=api)
data = {
    "currency": "USD",
    "amount": 10000
}
url = checkout.url(data).get('checkout_url')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///shop.db"
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    isActive = db.Column(db.Boolean, default=True)
    placement_date = db.Column(db.DateTime, default=datetime.utcnow)
    item_category = db.Column(db.String, nullable=False)

    def __repr__(self):
        return self.title


@app.route('/')
def index():
    items = Item.query.order_by(Item.price).all()
    return render_template('index.html', data=items)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        item_category = request.form['item_category']

        item = Item(title=title, price=price, item_category=item_category)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return "Произошла ошибка!"
    else:
        return render_template('create.html')


if __name__ == "__main__":
    app.run(debug=True)