from setuptools import setup, find_packages

setup(
    name="micropython_sevenseg",              
    version='1.1.0',                  
    description='A simple MicroPython library for controlling 7-segment displays.',
    author='Kritish Mohapatra',       
    author_email='kritishmohapatra06norisk@gmail.com',  
    url="https://github.com/kritishmohapatra/micropython-sevenseg",  
    packages=find_packages(),         
    py_modules=['sevenseg'],          
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
