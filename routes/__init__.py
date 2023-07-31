# routes/__init__.py

from flask import render_template
from app import app

# Error handling for 404 (Page Not Found) response
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

# Error handling for 500 (Internal Server Error) response
@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

