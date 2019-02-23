# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 21:08:40 2019

@author: halfb
"""

from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
from scrape_mars import scrape
from pprint import pprint

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

@app.route('/')
def index():
    mars = mongo.db.mars.find_one()
    pprint(mars)
    return render_template("index.html", mars=mars, titles=mars["mars_h"])

@app.route('/scrape')
def spaceresults():
    mars = mongo.db.mars
    mars_data = scrape()
    # pprint(mars_data['mars_h'])
    mars.update(
        {},
        mars_data,
        upsert=True
    )
    return redirect('/', code=302)

if __name__ == "__main__":
    app.run(debug=True)