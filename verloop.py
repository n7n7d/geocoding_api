#!/usr/bin/python
# -*- coding: utf-8 -*

from flask import Flask, request, jsonify
import dicttoxml
import requests
from secret_keys import GOOGLE_API_KEY
import logging


def get_lat_lng(address):
    """Method to convert and return coordinates for an address"""
    lat, lng = None, None
    api_key = GOOGLE_API_KEY
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    end_point = f"{base_url}?address={address}&key={api_key}"
    req = requests.get(end_point)

    if req.status_code not in range(200, 299):
        return None, None

    try:
        results = req.json()['results'][0]
    except Exception as error:
        logging.warning(f"JSON Parsing error : {error}")

    lat = results.get('geometry', {}).get('location', {}).get('lat', '')
    lng = results.get('geometry', {}).get('location', {}).get('lng', '')
    return lat, lng


app = Flask(__name__)


@app.route('/getAddressDetails', methods=['POST'])
def getAddressDetails():
    """Method to return the relevant outputs"""
    raw_json = request.get_json(force=True)
    address = raw_json.get('address', '')
    (lat, long) = get_lat_lng(address)
    output_format = raw_json.get('output_format', '')
    result = {'coordinates': {'lat': lat, 'lng': long},
              'address': address}
    if output_format.lower() == 'json':
        return jsonify(result)
    if output_format.lower() == 'xml':
        return dicttoxml.dicttoxml(result)


@app.errorhandler(500)
def invalid_req(e):
    """Method to handle invalid requests/ internal server errors"""
    result = {
        "error": "Invalid Request"
    }
    return jsonify(result)
