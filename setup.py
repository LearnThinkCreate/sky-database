from setuptools import setup, find_packages

setup(
    name="skydb",
    version='0.1.3',
    author='Warren Hyson',
    author_email='warren.hyson5@gmail.com',
    description="For maintinaing Tampa Prep Data Warehouse",
    # url = "https://github.com/LearnThinkCreate/sky-api-python-client",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    test_suite='nose.collector',
)