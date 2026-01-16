from setuptools import setup

setup(name='mpets',
      version='0.9.15',
      description='API for game AmazingPets',
      packages=['mpets', 'mpets.api', 'mpets.logic', 'mpets.models', 'mpets.utils'],
      author_email='wilidon@bk.ru',
      install_requires=[
          'python-box[all]',
          'aiohttp',
          'BeautifulSoup4',
          'lxml',
          'aiohttp-socks',
          'pydantic',
          'python_rucaptcha',
          'loguru'
      ],
      zip_safe=False)
