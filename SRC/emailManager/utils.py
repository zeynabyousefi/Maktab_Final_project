
from kavenegar import *


def send_otp_code(phone_number, code):
    try:
        api = KavenegarAPI('7374545872633753574B653031727362456F68534837677A6A5334325352502F584E4F656C315768486A673D')
        params = {
            'sender': '',
            'receptor': phone_number,
            'message': f'{code} کد تایید شما '
        }
        response = api.sms_send(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)