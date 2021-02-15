#Dependencies 
from flask import Flask, request, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

#Set up Flask
app = Flask(__name__)

#PyMongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

#Routes
@app.route("/")
def index():
    mars_data = mongo.db.mars_data.find_one()
    return render_template("index.html", mars_data=mars_data)

@app.route("/scrape")
def scrape():
    mars_data = mongo.db.mars_data
    mars_news = scrape_mars.scrape()
    mars_data.update({}, mars_news, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)