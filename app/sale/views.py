from flask import render_template, request, flash
from flask_login import current_user, login_required
from app.models import db, MerchItem, Permission
from . import sale
from flask import jsonify


# page with a list of merch items for sale
@sale.route('/shop', methods=['GET', 'POST'])
def show_items_sale():
    page = request.args.get('page')

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
        items = MerchItem.query.order_by(MerchItem.created.desc())
        pages = items.paginate(page=page, per_page=5)

    return render_template('sales/sales.html', items=items, pages=pages)


# add a product for sale to the database
@sale.route('/add-item', methods=['GET', 'POST'])
@login_required
def add_item_merch():
    if current_user.can(Permission.MODERATE) or current_user.can(Permission.ADMIN):
        if request.method == 'POST':
            name = request.form['name']
            description = request.form['description']
            price = request.form['price']
            item = MerchItem(name=name, description=description, price=price)
            try:
                db.session.add(item)
                db.session.commit()
                flash('You were successfully add item !', category='success')

            except Exception:
                flash('Check your entries !', category= 'error')
        return render_template('sales/add_item_merch.html')


# view existing products from the database
@sale.route('/show-item', methods=['GET'])
@login_required
def show_item():
    # check permission
    if current_user.can(Permission.MODERATE) or current_user.can(Permission.ADMIN):    
        page = request.args.get('page')

        if page and page.isdigit():
            page = int(page)
        else:
            page = 1

        items = MerchItem.query.order_by(MerchItem.created.desc())
        pages = items.paginate(page=page, per_page=5)
        return render_template('sales/list_items.html', items=items, pages=pages)
    return render_template('block.html')


@sale.route('/item/<item_id>', methods=['GET'])
@login_required
def item_detail(item_id):
    item = MerchItem.query.filter_by(id=item_id).first()
    return render_template('sales/item_detail.html', item=item)


@sale.route('<id>/buy', methods=['GET'])
@login_required
def buy_merch_item(item_id):
    item = MerchItem.query.filter_by(id=item_id).first()
    if item:
        return jsonify({'message': f'Item bought name {item.name}'})
    else:
        return jsonify({'message': 'Item not found'}), 404
