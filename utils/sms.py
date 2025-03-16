import requests

src = "https://ippanel.com/api/select"


def send_password_code_sms(phone_number, code):
    print('code : ', code)
    json_request = {

        "op": "pattern",
        "user": "09027235390",
        "pass":  "Faraz@4271393037",
        "fromNum": "3000505",
        "toNum": f'{phone_number}',
        "patternCode": "hs7xsxhfkim0jd6",
        "inputData": 	[
            {
                "code": str(code)
            }
        ]
        }

    r = requests.post(src, json=json_request)

    if r.status_code == 200:
        return True, r.content
    else:
        return False, r