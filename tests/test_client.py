"""
File:           test_client.py
Description:    Unit tests for all functions within libinsult.client.py
                Theses unit tests do call the actual LibInsult production
                API in order to test against potential API changes.
"""
from bs4 import BeautifulSoup
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


# Test retrieve_filtered_text_raw

def test_retrieve_insult_raw_html(mocker):
    who = 'The Kardashians'
    plural = True
    url = 'https://insult.mattbas.org/api/insult.html/?who=The+Kardashians&plural=on'
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
    who = 'The Kardashians'
    plural = True
    url = 'https://insult.mattbas.org/api/insult.json/?who=The+Kardashians&plural=on'
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
    assert result['args']['template'] == ('The Kardashians are as <adjective> as '
                                          '<article target=adj1> <adjective min=1 max=3 id=adj1> '
                                          '<amount> of <adjective min=1 max=3> <animal> '
                                          '<animal_part>')

    # Make sure no error was reported
    assert result['error'] is False

    # Make sure no error message was returned in the payload
    assert 'error_message' not in result


def test_retrieve_insult_raw_txt(mocker):
    who = 'The Kardashians'
    plural = True
    url = 'https://insult.mattbas.org/api/insult.txt/?who=The+Kardashians&plural=on'
    mocker.patch('libinsult.client.build_url', return_value=url)
    result = retrieve_insult_text_raw('txt', who=who, plural=plural)

    # Since the insults are randomly generated strings the best
    # we can do is make sure that result is a valid string.
    assert isinstance(result, str)

# Test build_url function
