from crypt import methods
from flask import Flask, jsonify
from app import app
from app.configs import homedir, read_json, opt
import os, json

# @app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def home():
    return "<h1>Server Is Running</h1>"

@app.route("/coins", methods=["GET"])
def get_available_crypto():
    all_crypt = dict()
    all_crypt['crypto_symbols'] = opt['symbol']
    return jsonify(all_crypt)

@app.route("/data", methods=["GET"])
def get_graph_data():
    return read_json(os.path.join(homedir, f"output-data.json"))

@app.route("/analysis", methods=["GET"])
def get_analysis_data():
    return read_json(os.path.join(homedir, f"output-analysis.json"))