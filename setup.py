from setuptools import setup


setup(
    name='sequence_transfer',
    version='0.1.0',
    description='A sequence transfer library for NLP',
    url='https://github.com/Pangeamt/sequence_transfer',
    author='Laurent Bié',
    author_email='l.bie@pangeanic.com',
    license='BSD 2-clause',
    packages=['sequence_transfer', 'sequence_transfer.normalizer'],
    install_requires=['colorama'],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.7',
    ],
)
