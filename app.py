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
    months = parameters.get("amount").get("amount")   
    princ_amt = parameters.get("duration").get("amount")
    #months=12
    #princ_amt=2000
    interest_rate = 0.13
    
    
        
    #emi = (princ_amt*interest_rate*(1+interest_rate)**months)/((1+interest_rate)**(months-1))    
    #print(emi)    
    #cost = {'Europe':100, 'North America':200, 'South America':300, 'Asia':400, 'Africa':500}

    #speech = "The cost of shipping to"+str(emi)
    speech_response = "We will assist you with the financial assistance of "+str(months)+"Your monthly EMI will be approximately "+str(princ_amt)+"!!!!!!!"+"Do you have any existing vehicle loan in your name?"
    
    print("Response:")
    print(speech)

    return {
        "speech": speech_response,
        "displayText": speech_response,
        #"speech": speech,
        #"displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "apiai-onlinestore-shipping"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
