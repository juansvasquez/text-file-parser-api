from http.client import BAD_REQUEST
from flask import Flask, Response, request, jsonify
from datetime import datetime
import re
import os

app = Flask(__name__)

@app.route('/', methods=['POST'])
def parse_timestamps():
    '''
    Use the JSON provided by the POST input to check 
    for the POST body as defined below:
        curl -XPOST 
        -d '{"filename":"sample1.txt", 
            "from":"2020-07-06T23:00:00Z", 
            "to": "2022-07-06T23:00:00Z"}' 
        -H 'Content-Type: application/json' 
        localhost:8279/
    Return parsed entries within the date time range *inclusively*, 
    in JSON format.
    '''

    #Check for malformed JSON
    try:
        request_data = request.get_json()
    except:
        return Response('[]', status=200, mimetype='application/json')

    #Check that filename/to/from are keys in the JSON
    #Error handling can be improved, for specific exceptions
    try:
        filename = request_data['filename']
        from_ = request_data['from']
        to = request_data['to']
    except:
        return Response('[]', status=200, mimetype='application/json')

    #Send JSON to helper function
    response_body = body_former(request_data)

    #In case helper function found that JSON was malformed
    if response_body is None:
        return Response('[]', status=200, mimetype='application/json')
    
    return jsonify(response_body), 200


def body_former(input):
    '''
    '''
    #Check that filename in input exists
    filename = input['filename']
    try:
        document_path = os.getcwd()+f'/test-files/{filename}'
        document = open(document_path, 'r')
    except FileNotFoundError:
        return None

    #Check for blank/malformed timestamps in 'from' and 'to'
    from_ = input['from']
    to = input['to']
    # Regex to detect ISO8601 format
    regex = r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$'
    match_iso8601 = re.compile(regex).match
    
    if match_iso8601(from_) is None:
        return None

    if match_iso8601(to) is None:
        return None

    #Parse through file, saving timezones that fit between to and from, inclusive
    final_body = []
    with document as file:
        for line in file:
            #Some error handling, in case we run into a malformed line
            try:
                line_l = line.split()
                if (line_l[0] >= from_) and (line_l[0] <= to):
                    mini_dict = {
                        "eventTime": line_l[0],
                        "email": line_l[1],
                        "sessionId": line_l[2]
                    }
                    final_body.append(mini_dict)
            except:
                continue

    return final_body
