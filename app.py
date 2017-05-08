#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") != "DefaultWelcomeIntent.DefaultWelcomeIntent-custom.vehiclefinance-custom":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    #zone = parameters.get("shipping-zone")    
    months = req.get("result").get("parameters").get("duration").get("amount")
    princ_amt = req.get("result").get("parameters").get("amount").get("amount")
    interest_rate = 0.13
    emi = (princ_amt*interest_rate*(1+interest_rate)**months)/((1+interest_rate)**(months-1))    

    speech = "We will assist you with the financial assistance of "+str(princ_amt)+" INR\n"+"Your monthly EMI will be approximately"+str(emi)+" INR\n"+"Do you have any existing loan against you?"
    
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "apiai-onlinestore-shipping"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
