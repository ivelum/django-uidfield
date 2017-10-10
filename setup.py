from setuptools import setup

version = '0.1.1'

setup(
    name='django-uidfield',
    version=version,
    description='django-uidfield is a library which includes class UIDField for models.',
    keywords='django model field',
    license='MIT',
    author='ivelum',
    author_email='info@ivelum.com',
    url='https://github.com/ivelum/django-uidfield/',
    install_requires=[
        'django',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=['django_uidfield'],
    include_package_data=True,
    test_suite="tests",
)
