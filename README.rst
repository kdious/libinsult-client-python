LibInsult Client
=================

This is a Python client for the
`LibInsult <https://insult.mattbas.org/>`__ web API.

Installation
------------

::

    pip install libinsult-client

or

::

    python setup.py install

Usage
-----

To use the basic filtering you can call the ``contains_profanity`` or
the ``retrieve_filtered_text`` methods from the client:

::

    >>> from libinsult_client import client
    >>> client.retrieve_insult()
    u'You are as ill as a filthy bucketful of ineffectual maggot ooze'

You can also get the raw data that the LibInsult API returns by calling
the ``raw`` version of the APIs:

::

    >>> from libinsult_client import client
    >>> client.retrieve_insult_text_raw('json')
    {u'insult': u'You are as puny as a dirty detestable absurd bucketful of infernal worthless
    leech puke', u'args': {u'lang': u'en', u'template': u'You are as <adjective> as
    <article target=adj1> <adjective min=1 max=3 id=adj1> <amount> of <adjective min=1 max=3>
    <animal> <animal_part>'}, u'error': False}

This can be helpful in the event that the API changes and/or you feel
you can use the raw data in some manner.

You can also see the URL that is created for a specific request by using
the ``build_url`` method (mainly helpful for testing):

::

    >>> client.build_url('insult', 'json', who='The Johnsons', pural=True)
    u'https://insult.mattbas.org/api/insult.json/?who=The+Johnsons&plural=on'

Testing
-------

Tests have been for python 2.7 and python 3 using ``pytest``. The unit
tests do call the actual PurgoMalum production API in order to test
against potential API changes.

Before running tests make sure to install
`pytest <https://pypi.org/project/pytest/>`__,
`pytest-cov <https://pypi.org/project/pytest-cov/>`__,
`pytest-mock <https://pypi.org/project/pytest-mock/>`__, and
`mock <https://pypi.org/project/mock/>`__ (already included in
`requirements.txt <requirements.txt>`__).

To execute the tests and generate a code coverage report run the
following:

::

    pytest --cov-report term-missing --cov=libinsult/

You should see:

::

    Name                   Stmts   Miss  Cover   Missing
    ----------------------------------------------------
    libinsult/__init_.py       0      0   100%
    libinsult/client.py       39     11    72%   43, 47, 51, 60-69, 99
    ----------------------------------------------------
    TOTAL                     39     11    72%

Miscellaneous
-------------

This is one of my first offerings to the open source community. If you see any
issues with this client library and/or potential improvements please let
me know and I will make the necessary updates.

Donation
--------

If this is helpful to you in any please consider a small donation.

|paypal|

.. |paypal| image:: https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif
   :target: https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=GFDDW292XZVDJ&source=url
