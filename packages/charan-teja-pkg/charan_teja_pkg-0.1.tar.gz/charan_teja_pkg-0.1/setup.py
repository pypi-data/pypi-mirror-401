from setuptools import setup,find_packages

setup(
    name = "charan_teja_pkg",
    version = '0.1',
    author = 'Rachaveti Charan Teja',
    author_email = 'charante153624@gmail.com',
    description= 'This speech to plain text package'
)
packages = find_packages(),

install_requirements = [
    'selenium',
    'Webdriver_manager'
]

