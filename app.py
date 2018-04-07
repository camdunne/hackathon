from flask import Flask, flash, redirect, render_template, request, session, abort
from flask import jsonify
import os
import json
import urllib
import urllib.request

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'client')
app = Flask(__name__, template_folder=tmpl_dir)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/send_urls', methods=['POST'])
def process_user_history():
    print("[POST] process_user_history(): was called")

    received_data = request.get_json()

    if("urls" in received_data):
    	url_list = received_data['urls']
    	print(len(url_list), "urls received...")
    	print(url_list)
    else:
    	print("ERROR: No firld of URLs received")
    # print("User asked to process: "+request.form['user_data'])

    # user_text =  request.form['user_data']
    
    analyzed_data = "Stupid java!!"
    print("Returning:",analyzed_data)
    return jsonify(analyzed_data)

if __name__ == "__main__":
    app.run(debug=True, port=8888)
