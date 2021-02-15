#Dependencies 
from flask import Flask, request, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

#Set up Flask
app = Flask(__name__)

#PyMongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

#Routes