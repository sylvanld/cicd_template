import setuptools

setuptools.setup(
    name='tmsgit',
    description='Help maintaining a clean git project!',
    version='0.0.2',
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'tmsgit=tmsgit.__main__:main'
        ]
    },
    install_requires=[
        'argcomplete'
    ]
)
