
import requests
def get_iss_position():
    try:
        r = requests.get("http://api.open-notify.org/iss-now.json", timeout=5)
        return r.json().get("iss_position",{})
    except:
        return {"latitude":0,"longitude":0}
