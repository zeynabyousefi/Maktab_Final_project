from kavenegar import *


def send_otp_code(phone_number, code):
    try:
        api = KavenegarAPI('653168444F61354169375251423577713448526B79545A766D424E5059524C4F3132667A586F6E76432F6B3D')
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