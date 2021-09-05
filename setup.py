from setuptools import setup, find_packages

with(open("README.md")) as f:
    long_desc = f.read()

setup(
    name='ipclassifier',
    version='1.0.2',    
    description='Classifies English iambic pentameter poetry by period',
    long_description=long_desc,
    long_description_content_type="text/markdown",
    keywords=["NLP", "iambic pentameter", "meter", "poetry", "English poetry", "scansion", "poetry classification"],
    url='https://github.com/Chad-Mowbray/iamb-classifier',
    author='Chad Mowbray',
    author_email='mail@mail.com',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
                    "click==8.0.1",
                    "joblib==1.0.1",
                    "nltk==3.6.2",
                    "numpy==1.21.2",
                    "regex==2021.8.28",
                    "scikit-learn==0.24.2",
                    "scipy==1.7.1",
                    "sklearn==0.0",
                    "threadpoolctl==2.2.0",
                    "tqdm==4.62.2",
                    "Unidecode==1.2.0 ",               
                      ],
    classifiers=[
        'License :: OSI Approved :: MIT License',       
        'Programming Language :: Python :: 3',
    ],
    
)