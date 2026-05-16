from setuptools import setup, find_packages
from typing import List
HYPEN_E_DOT = '-e .'
def get_requirements(file_path: str) -> List[str]:
    '''This function will return the list of requirements'''
    
    requirements = []
    with open(file_path) as fobj:
        requirements=fobj.readlines()
        requirements=[req.replace("\n","") for req in requirements]
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    return requirements 
    

setup(
    name="End-to-end-MLproject",
    version="0.0.1",
    author="Sahil",
    author_email="sahil.instincts@gmail.com",
    packages=find_packages(),
    install_requires= get_requirements("requirements.txt")
    
)