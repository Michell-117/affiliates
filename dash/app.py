import json

import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

def register_affiliate(affiliate_name, business_unit_id, business_unit_receive):
    url = "https://aff.adrswap.com/support/support/register-affiliate"
    payload = json.dumps({
        "affiliateName": affiliate_name,
        "businessUnitId": business_unit_id,
        "businessUnitRecive": business_unit_receive
    })
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        response_json = response.json()
        partner_id = response_json['payload']['partnerId']
        secret_key = response_json['payload']['secretKey']
        print(partner_id, "<<<<------------")

        # Aquí se van a añadir las IPs
        url = "https://aff.adrswap.com/support/support/register-affiliate-ip"
        ips = ["34.242.60.225", "52.18.206.144", "82.81.51.192", "213.57.116.202", "82.81.48.111", "62.90.205.233"]
        ip_list = []
        for ip in ips:
            payload = {
                "affiliate_id": partner_id, 
                "ip": ip
            }
            ip_list.append(payload)

        for payload in ip_list:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            print(response.text)

        return partner_id
    else:
        print(response.text)
        return None
    
#---------------------------------------------------------------------------------

def createTransaction(bussinesUnitName, tpId, amount, type, pspName, idTransaction):

    urlTransaction = "http://crm-app.tech/api/crm/create-transaction-new"

    payload = json.dumps({
        "bussinesUnitName": bussinesUnitName,
        "tpId": tpId,
        "amount": amount,
        "type": type,
        "pspName": pspName,
        "idTransaction": idTransaction
    })

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", urlTransaction, headers=headers, data=payload)
    if response.status_code == 200:
        return True
    
    return False

#------------------------------------------------------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    name_brand = request.form['name_brand']
    affiliate_manager = int(request.form['affiliate_manager'])

    if affiliate_manager == 1:
        register_affiliate(f"{name_brand} - FxMundo", 6, 20)
        register_affiliate(f"{name_brand} - FxTrategy", 8, 8)
        register_affiliate(f"{name_brand} - Adrswap", 7, 19)
        register_affiliate(f"{name_brand} - Noimarkets ANG", 16, 16)
        register_affiliate(f"{name_brand} - Bearinvester ANG", 22, 22)
    elif affiliate_manager == 2:
        register_affiliate(f"{name_brand} - FxIntegral", 19, 19)
        register_affiliate(f"{name_brand} - Noimarkets", 16, 20)
        register_affiliate(f"{name_brand} - Bearinvester", 22, 22)

    return "Affiliate registered successfully"

@app.route('/create-transaction-on-crm', methods=['POST'])
def registerLead():
    bussinesUnitName = request.form['bussinesUnitName']
    tpId = request.form['tpId']
    amount = request.form['amount']
    type = request.form['type']
    pspName = request.form['pspName']
    idTransaction = request.form['idTransaction']

    if createTransaction(bussinesUnitName, tpId, amount, type, pspName, idTransaction):
        return "Transaction was sent correctly"
    
    return "The transaction could not be sent"


# @app.route('/change-owner-lead', methods=['POST'])
# def changeOwner():


if __name__ == '__main__':
    app.run(debug=True)

