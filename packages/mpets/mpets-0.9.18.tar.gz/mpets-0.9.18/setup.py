from setuptools import setup, find_packages

setup(name='mpets',
      version='0.9.18',
      description='API for game AmazingPets',
      packages=find_packages(include=["mpets", "mpets.*"]),
      author_email='wilidon@bk.ru',
      install_requires=[
          'aiohttp',
          'BeautifulSoup4',
          'lxml',
          'aiohttp-socks',
          'pydantic',
          'python_rucaptcha',
          'loguru',
          'setuptools',
          'requests',
          'mkdocs-material'
      ],
      zip_safe=False)
