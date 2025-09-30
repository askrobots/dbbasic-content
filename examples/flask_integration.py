"""
Flask integration example for dbbasic-content.

Shows how to build a simple blog with Flask.
"""

from flask import Flask, render_template, abort
from dbbasic_content import ContentDB

app = Flask(__name__)
content = ContentDB('/var/app/content')


@app.route('/')
def index():
    """Homepage - list recent posts."""
    posts = content.get_posts(status='published', limit=10)
    return render_template('index.html', posts=posts)


@app.route('/<slug>/')
def post(slug):
    """Individual post page."""
    post = content.get_post(slug)

    if not post:
        abort(404)

    return render_template('post.html', post=post)


@app.route('/category/<category>/')
def category(category):
    """Posts by category."""
    posts = content.get_posts(categories=[category])
    return render_template('category.html', category=category, posts=posts)


@app.route('/tag/<tag>/')
def tag(tag):
    """Posts by tag."""
    posts = content.get_posts(tags=[tag])
    return render_template('tag.html', tag=tag, posts=posts)


@app.route('/search/')
def search():
    """Search posts."""
    from flask import request
    query = request.args.get('q', '')

    if not query:
        return render_template('search.html', results=[], query='')

    results = content.search(query)
    return render_template('search.html', results=results, query=query)


if __name__ == '__main__':
    app.run(debug=True)
