import requests
import json
from datetime import datetime
from datetime import timedelta

# Rapt API calls
def getToken(username, password):

    url = "https://id.rapt.io/connect/token"

    payload = f'client_id=rapt-user&grant_type=password&username={username}&password={password}'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return(json.loads(response.text))

def getTelemetry(hydrometerId, token):

    #sample Date: 2021-12-20T07:32:46.467Z

    #end date is now
    enddate = datetime.utcnow()
    startdate = enddate - timedelta(hours=1000)


    url = f"https://api.rapt.io/api/Hydrometers/GetTelemetry?hydrometerId={hydrometerId}&startDate={startdate}Z&endDate={enddate}Z"

    payload = {}
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return json.loads(response.text)

def getHydrometerDetails(hydrometerId, token):
    url = f"https://api.rapt.io/api/Hydrometers/GetHydrometer?hydrometerId={hydrometerId}"

    payload = {}
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return(json.loads(response.text))


#Brewdather API calls
def postBFUpdates(url, hydrodetails, telemetry):
    payload = {
          "name": hydrodetails.get('name', hydrodetails['id']), # Required field, this will be the ID in Brewfather
          "temp": telemetry['temperature'],
          "temp_unit": "C", # C, F, K
          "gravity": telemetry['gravity'],
          "gravity_unit": "G", # G, P
          "battery": telemetry['battery']
        }

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

    print(response.text)

    
    

# Press the green button in the gutter to run the script.

if __name__ == '__main__':
    token = getToken('wobbertj%40gmail.com', 'Foy8JW3hedH1')
    hydrometerDetails = getHydrometerDetails('da1b2b03-3a88-463b-bd66-758ec3c98df7',token['access_token'])
    data = getTelemetry('da1b2b03-3a88-463b-bd66-758ec3c98df7', token['access_token'])
    postBFUpdates('http://log.brewfather.net/stream?id=EW5JbPMEBGV41i',hydrometerDetails, data[-1])
    pass

# See PyCharm help at https://www.jetbrains.com/help/pycharm/