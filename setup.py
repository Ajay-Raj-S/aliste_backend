from setuptools import setup

setup(
    name='aliste',
    packages=['aliste'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-mysqldb',
    ],
)
