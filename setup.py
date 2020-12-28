from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='Handwriting Synthesis',
    version='1.0.0',
    description='The handwriting synthesis application.',
    long_description=long_description,
    url='https://github.com/MartinM98/Handwriting-synthesis-with-the-help-of-machine-learning',
    author='Martin Mrugala, Patryk Walczak, Bartlomiej Zyla',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.8'
    ],
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=['opencv-python', 'tensorflow',
                      'scikit-image', 'matplotlib'],  # 'wxPython==4.0.7'
    project_urls={
        'Bug Reports': 'https://github.com/MartinM98/Handwriting-synthesis-with-the-help-of-machine-learning/issues',
        'Source': 'https://github.com/MartinM98/Handwriting-synthesis-with-the-help-of-machine-learning',
    },
)
