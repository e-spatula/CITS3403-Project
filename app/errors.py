from flask import render_template, jsonify
from app import app, db

@app.errorhandler(404)
def not_found_error(error):
    return(render_template("error.html", code = 404, title ="Ooops"))

@app.errorhandler(500)
def not_found_error(error):
    return(render_template("error.html", code = 500, title ="Ooops"))
    