from gettext import install
from setuptools import setup,find_packages

setup(
    name='DockS-STT',
    version='0.1',
    author='Satyam Singh',
    author_email='satyam23153065@gmail.com',
    description='This is a speech to text package created'
)
packages = find_packages(),
install_requirement=[
    'selenium',
    'webdriver_manager'
]