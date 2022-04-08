from flask import Flask
from flask import request, session, redirect, render_template
from os import environ
import requests
import uuid

from app_orig import PROFILE_URL

CHANNEL_ID = environ['CHANNEL_ID']
CHANNEL_SECRET = environ['CHANNEL_SECRET']
CALLBACK_URL = environ.get('CALLBACK_URL', 'http://localhost:8080/callback')
LINE_LOGIN_URL = environ.get('LINE_LOGIN_URL', 'https://access.line.me/oauth2/v2.1/authorize')
AUTH_TOKEN_URL = environ.get('AUTH_TOKEN_URL', 'https://api.line.me/oauth2/v2.1/token')
LINE_PROFILE_URL = environ.get('LINE_PROFILE_URL', 'https://api.line.me/oauth2/v2.1/verify')
SCOPE = environ.get('LINE_LOGIN_URL', 'openid')


def get_secret():
    return uuid.uuid4().hex


def urlencode(string):
    return requests.utils.quote(string, safe='')


login_test_app = Flask(__name__, template_folder='html')
login_test_app.secret_key = environ.get('APP_SECRET', get_secret())


@login_test_app.route('/')
def index():
    return render_template('index.html')


@login_test_app.route('/callback')
def callback():

    correct_state = session.get('state', None)
    current_state = request.args.get('state', None)
    code = request.args.get('code', None)
    if None in (correct_state, current_state) or correct_state != current_state or code is None:
        print('states are', correct_state, 'and', current_state)
        print('code is', code)
        return render_template('error.html', error_msg='Bad state or code')

    args = []
    for k, v in request.args.items():
        if k in ('code', 'state'):
            continue
        args.append(f'{k}={v}')
    args = '&'.join(args)

    get_token_payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': CHANNEL_ID,
        'client_secret': CHANNEL_SECRET,
        'redirect_uri': f'{CALLBACK_URL}?{args}',
    }

    r = requests.post(
        AUTH_TOKEN_URL,
        data=get_token_payload,
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )

    token_resp_data = r.json()
    if r.status_code != 200:
        return render_template(
            'error.html',
            error_msg=f'Bad response code {r.status_code} ({token_resp_data})'
        )

    print('Data returned on token request')
    print(token_resp_data)

    get_profile_payload = {
        'client_id': CHANNEL_ID,
        'id_token': token_resp_data['id_token'],
    }

    r = requests.post(
        PROFILE_URL,
        data=get_profile_payload,
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )

    profile_resp_data = r.json()
    if r.status_code != 200:
        return render_template(
            'error.html',
            error_msg=f'Bad response code {r.status_code} ({profile_resp_data})'
        )

    print('Data returned on profile request', profile_resp_data)

    return render_template(
        'profile.html',
        user_name=profile_resp_data["name"],
        user_picture=profile_resp_data["picture"],
        client_id=profile_resp_data["sub"],
        channel_id=profile_resp_data["aud"],
        gen_timestamp=profile_resp_data["iat"],
        exp_timestamp=profile_resp_data["exp"],
        login_provider=profile_resp_data["iss"]
    )


@login_test_app.route('/login')
def refirect():
    session['state'] = get_secret()

    some_example_argumets = {
        "super_secret_val": get_secret(),
        "super_secret_name": "tssss.itsasecret",
    }

    line_url_with_args = (
        f'{LINE_LOGIN_URL}?response_type=code'
        f'&client_id={CHANNEL_ID}'
        f'&redirect_uri={urlencode(CALLBACK_URL + "?" + "&".join([f"{k}={v}" for k, v in some_example_argumets.items()]))}'
        f'&state={session["state"]}'
        f'&scope=profile%20{SCOPE}'
    )

    print('request will be redirected to', line_url_with_args)

    return redirect(line_url_with_args)


if __name__ == '__main__':
    login_test_app.run(host='0.0.0.0', port=8080)
