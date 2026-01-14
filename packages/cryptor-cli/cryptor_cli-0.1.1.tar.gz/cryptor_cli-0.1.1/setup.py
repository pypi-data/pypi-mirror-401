from setuptools import setup

setup(
    name='cryptor-cli',
    version='0.1.1',
    py_modules=['cryptor'],
    install_requires=[
        'click',
        'cryptography',
    ],
    entry_points={
        'console_scripts': [
            'cryptor=cryptor:cli',
        ],
    },
    author='Your Name',  # Replace with your name
    author_email='your.email@example.com',  # Replace with your email
    description='A CLI tool for secure file encryption using AES-256-GCM and Argon2.',
    long_description=open('README.md').read() if open('README.md') else '', # Readme.md for detailed description, or empty string if it does not exist
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/cryptor-cli', # Replace with your project's URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License', # Or whatever license you choose
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Security :: Cryptography',
        'Environment :: Console',
    ],
    python_requires='>=3.7',
)
