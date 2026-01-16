from setuptools import setup, find_packages

setup(name='mpets',
      version='0.9.16',
      description='API for game AmazingPets',
      packages=find_packages(include=["mpets", "mpets.*"]),
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
