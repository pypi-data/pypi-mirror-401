from setuptools import setup, find_packages

setup(
    name ='messages_test_nan',
    version='1.3',
    description='Un paquete con los mensajes para saludar y despedirse',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Eduardo Nanduca',
    author_email='acudnan@gmail.com',
    url='https://www.fb.com/acudnan_',
    license='MIT License',
    packages=find_packages(),
    scripts=[],
    test_suite='tests',
    install_requires=[paquete.strip() 
                      for paquete in open("requirements.txt").readlines()],
    classifiers=[
        'Environment :: Console :: Curses',
        'Programming Language :: Python :: 3.13',
        'Topic :: Utilities',
        'Operating System :: Microsoft :: Windows',
    ]
)