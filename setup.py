"""
Flask-Neo4j
-------------

Flask extension that provides integration with the Neo4j graph database using
the Py2neo library.

Links
`````

* `documentation <http://blah/Flask-Neo4j>`_
"""
from setuptools import setup


setup(
    name='Flask-Neo4j',
    version='0.1.0',
    url='https://github.com/lashex/flask-neo4j',
    license='Apache License, Version 2.0',
    author='Brett Francis',
    author_email='brett@',
    description='Flask extension providing integration with Neo4j.',
    long_description=__doc__,
    py_modules=['flask_neo4j'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'py2neo'
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)