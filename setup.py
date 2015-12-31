"""
Flask-Neo4jv2
-------------

Flask extension that provides integration with the Neo4j graph database using
the py2neo library. Under initial development.

"""
from setuptools import setup


setup(
    name='Flask-Neo4j',
    version='0.4.2',
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
        'Flask >= 0.10',
        'py2neo >= 2.0.1'
    ],
    test_suite='test_flask_neo4j.suite',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)