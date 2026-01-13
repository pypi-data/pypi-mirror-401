from setuptools import setup, find_packages

setup(
    name='auradata',
    version='1.0.1',
    author='Abdul Mofique Siddiqui',
    author_email='mofique7860@gmail.com',
    description='AuraData: A data-centric auditing and diagnostics engine for machine learning datasets, designed to detect noise, duplicates, label issues, and subgroup risks with transparent reporting.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Luckyy0311',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Quality Assurance',
    ],
    python_requires='>=3.8',
    install_requires=[
        'numpy>=1.20',
        'pandas>=1.0',
        'scikit-learn>=1.0'
    ],
)
