from flask import render_template,request,Blueprint
from flask_login import current_user
from models import TravelPost, User

core = Blueprint('core',__name__)

@core.route('/', methods=['POST','GET'])
def home():
    page = request.args.get('page', 1, type=int)
    tp = TravelPost.query.order_by(TravelPost.date.desc()).paginate(page=page, per_page=3)
    return render_template('home.html', user=current_user, posts=tp)

@core.route('/<int:user_id>')
def account(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    return render_template('account.html', user=user)