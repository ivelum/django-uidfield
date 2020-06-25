from setuptools import setup, Command

version = '0.2.0'


class TestCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from django.conf import settings
        settings.configure(
            DATABASES={'default': {
                'NAME': ':memory:',
                'ENGINE': 'django.db.backends.sqlite3'}
            },
            INSTALLED_APPS=('django_uidfield', 'django.contrib.contenttypes')
        )
        from django.core.management import call_command
        import django

        django.setup()

        call_command('test', 'django_uidfield')


setup(
    name='django-uidfield',
    version=version,
    description='django-uidfield is a library which includes class UIDField for models.',
    long_description=open('README.rst').read(),
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
    cmdclass={'test': TestCommand},
)
