from flask import Blueprint ,render_template


bp = Blueprint('show_posts', __name__)


@bp.route('/', methods=['GET'])
def view_posts_page():
    return render_template("posts.html")