.. raw:: html

   <p align="center">

.. image:: https://rawgit.com/tijme/angularjs-csti-scanner/master/.github/logo.svg?pypi=png.from.svg
   :width: 300px
   :height: 300px
   :alt: AngularJS Client-Side Template Injection Logo

.. raw:: html

   <br class="title">

.. image:: https://raw.finnwea.com/shield/?firstText=Donate%20via&secondText=Bunq
   :target: https://bunq.me/tijme/0/Automated%20client-side%20template%20injection%20(sandbox%20escape%2Fbypass)%20detection%20for%20AngularJS
   :alt: Donate via Bunq
   
.. image:: https://raw.finnwea.com/shield/?typeKey=TravisBuildStatus&typeValue1=tijme/angularjs-csti-scanner&typeValue2=master&cache=1
   :target: https://travis-ci.org/tijme/angularjs-csti-scanner
   :alt: Build Status
   
.. image:: https://raw.finnwea.com/shield/?firstText=License&secondText=MIT
   :target: https://github.com/cqr-cryeye-forks/angularjs-csti-scanner/blob/master/LICENSE.rst
   :alt: License: MIT

.. raw:: html

   </p>
   <h1>Angular Client-Side Template Injection Scanner</h1>

ACSTIS helps you to scan certain web applications for AngularJS Client-Side Template Injection (sometimes referred to as CSTI, sandbox escape or sandbox bypass). It supports scanning a single request but also crawling the entire web application for the AngularJS CSTI vulnerability.

Table of contents
-----------------

-  `Installation <#installation>`__
-  `Usage <#usage>`__
-  `Issues <#issues>`__
-  `License <#license>`__

Installation
------------

First make sure you're on `Python 2.7/3.4 <https://www.python.org/>`__ or higher. Then run the command below to install ACSTIS.

``$ pip install https://github.com/cqr-cryeye-forks/angularjs-csti-scanner/archive/master.zip``

Usage
-----

**Scan a single URL**

``acstis -d "https://finnwea.com/some/page/?category=23"``

**Scan a single URL (and verify that the alert pops)**

``acstis -vp -d "https://finnwea.com/some/page/?category=23"``

**Scan an entire domain**

``acstis -c -d "https://finnwea.com/"``

**Scan an entire domain (and stop if a vulnerability was found)**

``acstis -c -siv -d "https://finnwea.com/"``

**Trust the given certificate**

``acstis -d "https://finnwea.com/some/page/?category=23" -tc "/Users/name/Desktop/cert.pem"``

**All command line options**

.. code:: text

   usage: acstis [-h] -d DOMAIN [-c] [-vp] [-av ANGULAR_VERSION] [-vrl VULNERABLE_REQUESTS_LOG] [-siv] [-pmm] [-sos] [-soh] [-sot] [-md MAX_DEPTH] [-mt MAX_THREADS] [-iic] [-tc TRUSTED_CERTIFICATES]

   required arguments:
      -d DOMAIN, --domain DOMAIN                                                       the domain to scan (e.g. finnwea.com)

   optional arguments:
      -h, --help                                                                       show this help message and exit
      -c, --crawl                                                                      use the crawler to scan all the entire domain
      -vp, --verify-payload                                                            use a javascript engine to verify if the payload was executed (otherwise false positives may occur)
      -av ANGULAR_VERSION, --angular-version ANGULAR_VERSION                           manually pass the angular version (e.g. 1.4.2) if the automatic check doesn't work
      -vrl VULNERABLE_REQUESTS_LOG, --vulnerable-requests-log VULNERABLE_REQUESTS_LOG  log all vulnerable requests to this file (e.g. /var/logs/acstis.log or urls.log)
      -siv, --stop-if-vulnerable                                                       (crawler option) stop scanning if a vulnerability was found
      -pmm, --protocol-must-match                                                      (crawler option) only scan pages with the same protocol as the startpoint (e.g. only https)
      -sos, --scan-other-subdomains                                                    (crawler option) also scan pages that have another subdomain than the startpoint
      -soh, --scan-other-hostnames                                                     (crawler option) also scan pages that have another hostname than the startpoint
      -sot, --scan-other-tlds                                                          (crawler option) also scan pages that have another tld than the startpoint
      -md MAX_DEPTH, --max-depth MAX_DEPTH                                             (crawler option) the maximum search depth (default is unlimited)
      -mt MAX_THREADS, --max-threads MAX_THREADS                                       (crawler option) the maximum amount of simultaneous threads to use (default is 20)
      -iic, --ignore-invalid-certificates                                              (crawler option) ignore invalid ssl certificates
      -tc TRUSTED_CERTIFICATES, --trusted-certificates TRUSTED_CERTIFICATES            (crawler option) trust this CA_BUNDLE file (.pem) or directory with certificates

**Authentication, Cookies, Headers, Proxies & Scope options**

These options are not implemented in the command line interface of ACSTIS. Please download the `extended.py <https://github.com/cqr-cryeye-forks/angularjs-csti-scanner/blob/master/extended.py>`_ script and extend it with one or more of the following code snippets. You can paste these code snippets in the `main()` method of the `extended.py` script.

**Please note:** if you use the ``extended.py`` file make sure you call ``python extended.py [your arguments]`` instead of ``acstis [your arguments]``.

*Basic Authentication*

.. code:: python

    options.identity.auth = HTTPBasicAuth("username", "password")

*Digest Authentication*

.. code:: python

    options.identity.auth = HTTPDigestAuth("username", "password")

*Cookies*

.. code:: python

    options.identity.cookies.set(name='tasty_cookie', value='yum', domain='finnwea.com', path='/cookies')
    options.identity.cookies.set(name='gross_cookie', value='blech', domain='finnwea.com', path='/elsewhere')

*Headers*

.. code:: python

    options.identity.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
    })

*Proxies*

.. code:: python

    options.identity.proxies = {
        # No authentication
        # 'http': 'http://host:port',
        # 'https': 'http://host:port',

        # Basic authentication
        # 'http': 'http://user:pass@host:port',
        # 'https': 'https://user:pass@host:port',

        # SOCKS
        'http': 'socks5://user:pass@host:port',
        'https': 'socks5://user:pass@host:port'
    }

*Scope options*

.. code:: python

    options.scope.protocol_must_match = False

    options.scope.subdomain_must_match = True

    options.scope.hostname_must_match = True

    options.scope.tld_must_match = True

    options.scope.max_depth = None

    options.scope.request_methods = [
        Request.METHOD_GET,
        Request.METHOD_POST,
        Request.METHOD_PUT,
        Request.METHOD_DELETE,
        Request.METHOD_OPTIONS,
        Request.METHOD_HEAD
    ]

Testing
-------

The testing can and will automatically be done by `Travis CI <https://travis-ci.org/tijme/angularjs-csti-scanner>`__ on every push. If you want to manually run the unit tests, use the command below.

``$ python -m unittest discover``

Issues
------

Issues or new features can be reported via the GitHub issue tracker. Please make sure your issue or feature has not yet been reported by anyone else before submitting a new one.

License
-------

ACSTIS is open-sourced software licensed under the `MIT license <https://github.com/cqr-cryeye-forks/angularjs-csti-scanner/blob/master/LICENSE.rst>`__.
