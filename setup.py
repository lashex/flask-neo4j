"""
Flask-Neo4j
-------------

Flask extension that provides integration with the Neo4j graph database using
the py2neo library. Under initial development.

"""
from setuptools import setup


setup(
    name='Flask-Neo4j',
    version='0.2.0',
    url='https://github.com/lashex/flask-neo4j',
    license='MIT',
    author='Brett Francis',
    author_email='brett_francis@me.com',
    description='Flask extension providing integration with Neo4j.',
    long_description=__doc__,
    py_modules=['flask_neo4j'],
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'Flask >= 0.9',
        'py2neo >= 1.6'
    ],
    test_suite='test_flask_neo4j.suite',
    classifiers=[
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