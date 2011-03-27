import os

from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = ['colander', 'deform', 'pyyaml', 'webob', 'Paste']

setup(name='wiseguy',
      version='0.0',
      description='Wiseguy WSGI deployment framework',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        ],
      keywords='web wsgi',
      author="WSGI Cabal",
      author_email="http://lists.repoze.org/listinfo/wsgi-cabal",
      url="",
      license="MIT",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      tests_require = requires,
      install_requires = requires,
      test_suite="wiseguy.tests",
      entry_points = """\
      [console_scripts]
      wiseguy = wiseguy.scripts.command:main
      [wiseguy.component]
      pipeline = wiseguy.components.pipeline:PipelineComponent
      cascade = wiseguy.components.cascade:CascadeComponent
      gzip = wiseguy.components.gzip:GZipComponent
      helloworld = wiseguy.components.helloworld:HelloWorldComponent
      notfound = wiseguy.components.notfound:NotFoundComponent
      """
      )

