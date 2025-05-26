from setuptools import setup, find_packages

setup(
    name='cisco-mds-release-agent',
    version='1.0.0',
    author='Your Name/Team',
    author_email='your.email@example.com',
    description='A system for consolidating and querying Cisco MDS release notes.',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'requests',
        'beautifulsoup4',
        'PyYAML',
        'langchain',
        'langsmith',
        'google-gemini'
    ],
    entry_points={
        'console_scripts': [
            'run_dca=scripts.run_dca:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)