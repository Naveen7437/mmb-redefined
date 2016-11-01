import requests
from django.core.files.base import ContentFile
from django.core.mail import send_mail
from django.conf import settings
from requests import request, ConnectionError


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
        # TODO: hitting ???
        print (result.content)

    return


def save_user_picture(backend, user, response, is_new,  *args, **kwargs):
    """
    Get the user avatar (and any other details you're interested in)
    and save them
    """

    if backend.name == 'google-plus':
        if response.get('image') and response['image'].get('url'):
            url = response['image'].get('url')
            if user.avatar:
                # if existing avatar stick with it rather than google syncing
                pass
            else:
                try:
                    response = request('GET', url)
                    response.raise_for_status()
                except ConnectionError:
                    pass
                else:
                    # No avatar so sync it with the google one.
                    # Passing '' for name will invoke my upload_to function
                    # saving by username (you prob want to change this!)
                    user.avatar.save(u'',
                                    ContentFile(response.content),
                                    save=False
                                    )
                    user.save()

    elif backend.name == 'facebook' and is_new:
        # TODO: saving only if does not exist
        # if user.avatar:
        #     pass
        # else:
        url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])

        try:
            resp = request('GET', url, params={'type': 'large'})
            resp.raise_for_status()
        except ConnectionError:
            pass
        else:
            user.avatar.save(u'',
                             ContentFile(resp.content),
                             save=False
                             )
            user.fb_link = response['link']
            user.gender = response['gender']
            user.save()


def mail_user_activation_key(user):
    """
    mail user for account verification
    """

    link = "{0}/users/activate/{1}".format(settings.APP_URL, user.activation_key)
    # TODO: update subject and message and move to task
    subject = "Activate your mmb account"
    message = "<b>hola</b>" \
              "<href>{0}</href>".format(link)
    to = [user.email]
    send_mail(subject, message, 'khnaveen01@gmail.com', to, fail_silently=False)

