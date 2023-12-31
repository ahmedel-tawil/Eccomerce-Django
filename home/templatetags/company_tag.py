# import json
# from oauth2client.client import SignedJwtAssertionCredentials
#
# from django import template
#
# register = template.Library()
#
#
# @register.inclusion_tag('myapp/analytics.html', takes_context=True)
# def analytics(context, next=None):
#     ANALYTICS_CREDENTIALS_JSON = 'absolute/path/to/service.json'
#     ANALYTICS_VIEW_ID = 'Google Analytics View ID here'
#
#     # The scope for the OAuth2 request.
#     SCOPE = 'https://www.googleapis.com/auth/analytics.readonly'
#
#     # The location of the key file with the key data.
#     KEY_FILEPATH = ANALYTICS_CREDENTIALS_JSON
#
#     # Load the kmaey file's private data.
#     with open(KEY_FILEPATH) as key_file:
#         _key_data = json.load(key_file)
#
#     # Construct a credentials objects from the key data and OAuth2 scope.
#     _credentials = SignedJwtAssertionCredentials(
#         _key_data['client_email'], _key_data['private_key'], SCOPE)
#
#     return {
#         'token': _credentials.get_access_token().access_token,
#         'view_id': ANALYTICS_VIEW_ID
#     }
