import requests

from users.app_settings import ACCESS_FROM_REFRESH_URL


def create_new_access_token(oauth_obj):
    """
    create new access token on the basis of refresh
    token, and informs angular
    :return: None
    """
    if not oauth_obj:
        return

    refresh_obj = oauth_obj.user.refreshtoken_set.last()
    _client_id = oauth_obj.client.client_id
    _client_secret = oauth_obj.client.client_secret
    _refresh_token = refresh_obj.token
    _grant_type = ['refresh_token']

    payload = {
        "client_id": _client_id,
        "client_secret": _client_secret,
        "refresh_token": _refresh_token,
        "grant_type": _grant_type,
    }

    result = requests.post(ACCESS_FROM_REFRESH_URL, data=payload)

    if result.status_code == 200:
        # TODO: hitting angular to return new  access token token
        print (result.content)

    return
