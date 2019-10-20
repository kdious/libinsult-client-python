"""
File:           client.py
Description:    A client library for the the public LibInsult REST API
                See: https://insult.mattbas.org/api/
"""
import requests
from urllib.parse import urlencode

LIB_INSULT_BASE_URL = 'https://insult.mattbas.org/api/'
VALID_LANGUAGE_CODES = ['en']
VALID_REQUEST_TYPES = ['adjective', 'insult']
VALID_RESPONSE_FORMATS = ['html', 'json', 'txt']


class ClientError(Exception):
    pass


def build_url(request_type, response_format, language_code, who, plural):
    """
    Builds the query string to use for an LibInsult REST API call
    See https://insult.mattbas.org/api/ for details

    :param request_type: (string) One of the types of requests that can be sent to the API:
        'adjective': Generate a random negative adjective
        'insult': Generate a random result based on the other query string params
    :param response_format: Must be one of the valid response formats for the API:
        html, json, txt
    :param language_code: (string) A code representing the language for the insult
    :param who: (string) The name of the person(s) who are being insulted
    :param plural: (boolean) Indicates where the 'who' should be considered as plural or not for
        purposes of generating the insult.  Setting this parameter only has an effect if 'who' has
        also been set

    :return: (string) The URL for the specified request.
        Ex: 'https://insult.mattbas.org/api/insult?who=The+Kardashians&plural=on'

    :raises: ValueError
    """
    if request_type not in VALID_REQUEST_TYPES:
        raise ValueError("Input param 'request_type' is invalid - must be one of {}"
                         .format(VALID_REQUEST_TYPES))

    if response_format not in VALID_RESPONSE_FORMATS:
        raise ValueError("Input param 'response_format' is invalid - must be one of {}"
                         .format(VALID_RESPONSE_FORMATS))

    if language_code not in VALID_LANGUAGE_CODES:
        raise ValueError("Input param 'language_code' is invalid - must be one of {}"
                         .format(VALID_LANGUAGE_CODES))

    query_string_params = []

    if request_type == 'insult':
        # 'who' and 'plural' being added to the query string only make sense
        # for the 'insult' request type
        if who:
            if not isinstance(who, str):
                raise ValueError("Input param 'who' is a {} (must be a str)".format(type(who)))
            query_string_params.append(('who', who))

            # Plural only makes sense to use when 'who' has been set
            if plural:
                if not isinstance(plural, bool):
                    raise ValueError("Input param 'plural' is a {} (must be a bool)"
                                     .format(type(plural)))
                query_string_params.append(('plural', 'on'))

    query_string = urlencode(query_string_params)

    return ''.join([LIB_INSULT_BASE_URL, '/',
                    language_code, '/', request_type, '.',
                    response_format, '?', query_string])


def retrieve_insult_text_raw(response_format, language_code='en', who=None, plural=False):
    """
    Call the LibInsult REST API using the json request_type and return the raw payload response
    See https://insult.mattbas.org/api/ for details

    :param response_format: (string) The format for the response.  Must be one of: html, json, txt
    :param language_code: (string) A code representing the language for the insult
    :param who: (string) The name of the person(s) who are being insulted
    :param plural: (boolean) Indicates where the 'who' should be considered as plural or not for
        purposes of generating the insult.  Setting this parameter only has an effect if 'who' has
        also been set

    :return: (string) The URL for the specified request.
        Ex: 'https://insult.mattbas.org/api/insult?who=The+Kardashians&plural=on'

    :raises: ValueError
    """
    if response_format not in VALID_RESPONSE_FORMATS:
        raise ValueError("Input param 'response_format' is invalid - must be one of {}"
                         .format(VALID_RESPONSE_FORMATS))

    full_url = build_url('insult', response_format, language_code, who, plural)
    response = requests.get(url=full_url)

    if response_format in ('html', 'txt'):
        response_content = response.content.decode()
    else:
        response_content = response.json()

    return response_content


def retrieve_insult(language_code='en', who=None, plural=False):
    """
    Queries the LibInsult REST API to retrieve a randomly generated insult
    This just uses the 'json' response format call
    See https://insult.mattbas.org/api/ for details

    :param language_code: (string) A code representing the language for the insult
    :param who: (string) The name of the person(s) who are being insulted
    :param plural: (boolean) Indicates where the 'who' should be considered as plural or not for
        purposes of generating the insult.  Setting this parameter only has an effect if 'who' has
        also been set

    :return: (string) The insult string

    :raises: ClientError
    :raises: ValueError
    """
    response_content = retrieve_insult_text_raw('json', language_code, who, plural)

    if response_content['error']:
        raise ClientError(response_content['error_message'])

    return response_content['insult']
