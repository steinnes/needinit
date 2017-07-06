from setuptools import setup, find_packages
import fastentrypoints
from pip.req import parse_requirements
from pip.download import PipSession


def get_requirements():
    requirements = parse_requirements(
        os.path.join(os.path.dirname(__file__), "requirements.txt"),
        session=PipSession())
    return [str(req.req) for req in requirements]


def get_version():
    __version__ = None
    with open('needinit/_version.py') as version_src:
        exec(version_src.read())
    return __version__

setup(
    name='needinit',
    version=get_version(),
    description='Prevent callability on un-initialized objects',
    url='https://github.com/steinnes/needinit',
    author='Steinn Eldjarn Sigurdarson',
    author_email='steinnes@gmail.com',
    keywords=['library', 'object initialization'],
    install_requires=[str(req.req) for req in parse_requirements("requirements.txt", session=PipSession())],
    packages=find_packages(),
)
