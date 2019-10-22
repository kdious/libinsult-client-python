"""
File:           test_client.py
Description:    Unit tests for all functions within libinsult.client.py
                Theses unit tests do call the actual LibInsult production
                API in order to test against potential API changes.
"""
from bs4 import BeautifulSoup
from mock import Mock
import pytest
from libinsult.client import (
    build_url,
    ClientError,
    LIB_INSULT_BASE_URL,
    retrieve_insult,
    retrieve_insult_text_raw,
)


# Test retrieve_insult function

def test_retrieve_insult():
    result = retrieve_insult()
    # Since the insults are randomly generated strings the best
    # we can do is make sure that result is actually a string.
    assert isinstance(result, str)

def test_retrieve_insult_invalid(mocker):
    response = {'error': True, 'error_message': 'Invalid Call'}
    mocker.patch('libinsult.client.retrieve_insult_text_raw', return_value=response)
    with pytest.raises(ClientError):
        retrieve_insult()


# Test retrieve_filtered_text_raw

def test_retrieve_insult_raw_html(mocker):
    who = 'The Johnsons'
    plural = True
    url = 'https://insult.mattbas.org/api/insult.html/?who=The+Johnsons&plural=on'
    mocker.patch('libinsult.client.build_url', return_value=url)
    result = retrieve_insult_text_raw('html', who=who, plural=plural)

    # Parse the HTML using BeautifulSoup
    parsed_html = BeautifulSoup(result, "html.parser")

    # Since the insults are randomly generated strings the best
    # we can do is make sure that result is valid HTML.
    assert bool(parsed_html.find()) is True

    # The insult is contained in the h1 tag (the only one)
    h1_tags = parsed_html.find_all('h1')
    assert len(h1_tags) == 1
    assert h1_tags[0] is not None


def test_retrieve_insult_raw_json(mocker):
    who = 'The Johnsons'
    plural = True
    url = 'https://insult.mattbas.org/api/insult.json/?who=The+Johnsons&plural=on'
    mocker.patch('libinsult.client.build_url', return_value=url)
    result = retrieve_insult_text_raw('json', who=who, plural=plural)

    # Since the insults are randomly generated strings the best
    # we can do is make sure that result is actually a dict.
    assert isinstance(result, dict)

    # Make sure that an insult was returned
    assert ('insult' in result and result['insult'])

    # Make sure that the language was as expected
    assert result['args']['lang'] == 'en'

    # Make sure the default template was returned
    assert result['args']['template'] == ('The Johnsons are as <adjective> as '
                                          '<article target=adj1> <adjective min=1 max=3 id=adj1> '
                                          '<amount> of <adjective min=1 max=3> <animal> '
                                          '<animal_part>')

    # Make sure no error was reported
    assert result['error'] is False

    # Make sure no error message was returned in the payload
    assert 'error_message' not in result


def test_retrieve_insult_raw_txt(mocker):
    who = 'The Johnsons'
    plural = True
    url = 'https://insult.mattbas.org/api/insult.txt/?who=The+Johnsons&plural=on'
    mocker.patch('libinsult.client.build_url', return_value=url)
    result = retrieve_insult_text_raw('txt', who=who, plural=plural)

    # Since the insults are randomly generated strings the best
    # we can do is make sure that result is a valid string.
    assert isinstance(result, str)

# Test build_url function

def test_build_url():
    full_url = build_url('insult', 'txt', language_code='en', who='Kristen', plural=True)
    expected_url = 'https://insult.mattbas.org/api/en/insult.txt?who=Kristen&plural=on'
    assert full_url == expected_url, "Should be '{}".format(expected_url)
     

def test_build_url_invalid_request_type():
    with pytest.raises(ValueError):
        build_url('invalid', 'txt', language_code='en', who='Campbell', plural=False)


def test_build_url_no_request_type():
    with pytest.raises(ValueError):
        build_url('', 'txt', language_code='en', who='Kristen', plural=False)


def test_build_url_invalid_response_format():
    with pytest.raises(ValueError):
        build_url('insult', 'invalid', language_code='en', who='Wakanda', plural=False)


def test_build_url_no_response_format():
    with pytest.raises(ValueError):
        build_url('insult', '', language_code='en', who='Beyonce', plural=False)


def test_build_url_invalid_language_code():
    with pytest.raises(ValueError):
        build_url('insult', 'json', language_code=3, who='The Avengers', plural=True)


def test_build_url_invalid_who():
    with pytest.raises(ValueError):
        build_url('insult', 'json', language_code='en', who=7, plural=False)


def test_build_url_invalid_plural():
    with pytest.raises(ValueError):
        build_url('insult', 'json', language_code='en', who='Mace Windu', plural='invalid')


# Test retrieve_insult_text_raw function

def test_retrieve_insult_text_raw_invalid_response_format():
    with pytest.raises(ValueError):
        retrieve_insult_text_raw('invalid')


