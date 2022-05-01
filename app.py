from flask import Flask, request, jsonify
from pymongo import MongoClient
from olx.constants import RESULTS_PER_PAGE, DB_NAME, FIELDS
from olx.olx import Olx
from datetime import date
from helpers import dictlist_to_csv, send_mail
import json

app = Flask(__name__)


client = MongoClient('localhost', 27017)
olx_db = client[DB_NAME]

@app.route("/search", methods=["POST"])
def search_query_olx():
    # EXAMPLE REQUEST BODY
    # query_data = {"query":"BMW", "results_count":200, "email":"a.khaled.abdrabou@gmail.com"}

    query_data = json.loads(request.data)
    results_count = query_data.get("results_count") if query_data.get("results_count") > 20 else 20
    query = query_data.get("query") 
    email_to = query_data.get("email")

    coll_list = olx_db.list_collection_names()
    coll_name = f'{date.today()}+{query}'

    if coll_name in coll_list:
        documents_count = olx_db[coll_name].count_documents({})
        # Data Scraped before this day and results count can be retrieved from DB.
        if documents_count >= results_count:
            try:
                items_dictionaries = list(olx_db[coll_name].find().sort("price").limit(results_count))
                dictlist_to_csv("items",items_dictionaries,FIELDS)
                send_mail(email_to)
                return jsonify({
                            'msg':"Data retrieved from your database and emailed to you successfully."
                        }) , 200
            except Exception as e:
                return jsonify({
                        'msg':f"Error: {e}"
                    }) , 400
        # Data Scraped before this day but results count is more than the existing,
        # so we scrap the difference save them in DB then we retrieve all from DB.
        else:
            try:
                requested_results_count = results_count - documents_count
                items_dict_list = Olx.scrap_items(query=query,results_count=requested_results_count)
                olx_db[coll_name].insert_many(items_dict_list)
                items_dictionaries = olx_db[coll_name].find().sort("price")
                dictlist_to_csv("items",items_dictionaries,FIELDS)
                send_mail(email_to)
                return jsonify({
                            'msg':"Some data retrieved from your database, some scraped from Olx and both emailed to you successfully."
                        }) , 200
            except Exception as e:
                return jsonify({
                        'msg':f"Error: {e}"
                    }) , 400
    # Data isn't available so we scrap it and save it to the DB and then retrieve it.
    else:
        try:
            items_dict_list = Olx.scrap_items(query=query,results_count=results_count)
            olx_db[coll_name].insert_many(items_dict_list)
            items_dictionaries = list(olx_db[coll_name].find().sort("price"))
            dictlist_to_csv("items",items_dictionaries,FIELDS)
            send_mail(email_to)
            return jsonify({
                    'msg':"Data scraped, saved in your database and emailed to you successfully."
                }) , 200
        except Exception as e:
            return jsonify({
                    'msg':f"Error: {e}"
                }) , 400



app.run(host='localhost',debug=True)