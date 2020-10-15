from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# setup mongo connection
#conn = "mongodb://localhost:27017"
#client = pymongo.MongoClient(conn)

# connect to mongo db and collection
#db = client.my_test_db
#stuff = db.mars_stuff

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


@app.route("/")
def index():

    # Find one record of data from the mongo database
    scraped_mars_data = mongo.db.collection.find_one()

    # render an index.html template and pass it the data you retrieved from the database
    return render_template("index.html", mars_data=scraped_mars_data)



@app.route("/scrape")
def scrape():

    # Run the scrape function
    freshly_scraped_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, freshly_scraped_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
