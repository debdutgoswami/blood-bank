import requests, json, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import app_secrets

def sendsms(name: str, location: str, bloodgroup: str, phone: str, rphone: str):
    url = 'https://www.fast2sms.com/dev/bulk'
    headers = {
        'authorization': app_secrets.FAST2SMS_KEY,
        'cache-control': "no-cache",
        'content-type': "application/x-www-form-urlencoded"
    }

    payload = "sender_id=FSTSMS&language=english&route=qt&numbers={}".format(phone)+"&message=24021&variables={#DD#}|{#FF#}|{#AA#}|{#CC#}&variables_values="+"{}|{}|{}|{}".format(name,location.split(',')[0],bloodgroup,rphone)
    response = requests.request("POST", url, data=payload, headers=headers)
    try:
        status_code = json.loads(response.text)["status_code"]
    except KeyError:
        pass

def sendemail(server, name: str, location: str, bloodgroup: str, email: str, phone: str):
    fromaddr = "debdutgoswami7@gmail.com"
    toaddr = email
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "IMPORTANT: Urgent need of Blood"
    body = f"""{name} from {location} needs {bloodgroup} blood immediately.
    Kindly contact him/her on {phone}.

    YOUR BLOOD CAN GIVE A LIFE TO SOMEONE.
    """
    msg.attach(MIMEText(body))
    text = msg.as_string()
    
    return text
