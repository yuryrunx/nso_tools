from setuptools import setup, find_packages
import nso_tools



setup(
    name='nso_tools',
    version=nso_tools.__version__,
    description='Tools for usefull work with NSO',
    url='https://github.com/yuryrunx/nso_tools.git',
    author=nso_tools.__author__,
    author_email='yury@example.com',
    license=nso_tools.__licence__,
    packages=['nso_tools'],
    zip_safe=False
)