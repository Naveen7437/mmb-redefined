import requests
from django.core.files.base import ContentFile
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template import Context
from django.template.loader import render_to_string
from requests import request, ConnectionError


from users.app_settings import ACCESS_FROM_REFRESH_URL
from users.models import Profile


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

            user.gender = response['gender']
            user.save()

            profile = Profile(user=user)
            profile.fb_link = response['link']
            profile.save()


def mail_user_activation_key(user, host=None):
    """
    mail user for account verification
    """

    # todo: log error here
    if not user.email:
        return

    link = "http://localhost:8000/#/users/activate/{0}/".format(user.activation_key)
    # TODO: update subject and message and move to task
    subject = "Activate your mmb account"
    from_email = "khnaveen01@gmail.com"
    context = Context({"link": link, "username": user.username})
    text_content = render_to_string('email.txt', context)
    html_content = render_to_string('email.html', context)
    to = [user.email]
    mail = EmailMultiAlternatives(subject, text_content, from_email, to)
    mail.attach_alternative(html_content, "text/html")
    mail.send()
