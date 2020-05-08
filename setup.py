import setuptools

setuptools.setup(
    name='selector',
    version='0.1.0',
    author='Nick Leo Martin',
    author_email='nickleomartin@gmail.com',
    url='https://github.com/NickLeoMartin/singer-selector',
    description=('A singer.io extension to programmatically'
                 ' select streams and fields in a catalog'),
    py_modules=['selector'],
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3 :: Only'
    ],
    install_requires=[
        'backoff == 1.8.0',
        'ciso8601 == 2.1.3',
        'jsonschema == 2.6.0',
        'python-dateutil == 2.8.1',
        'pytz == 2018.4',
        'simplejson == 3.11.1',
        'singer-python == 5.9.0',
        'six == 1.14.0'
    ],
    extras_require={
        'dev': [
            'pylint==2.5.2',
            'flake8==3.7.9',
            'autopep8 == 1.5.2',
            'pytest==5.4.2'
        ]
    },
    entry_points="""
          [console_scripts]
          selector=selector:main
      """,
    packages=['selector'],
    package_data={},
    include_package_data=True,
)
