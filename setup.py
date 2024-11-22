from setuptools import setup

setup(
    name='ARFlappy',
    version='0.1.0',
    description='Classic Flappy Game with Augmented Reality',
    url='https://github.com/shuds13/pyexample',
    author='Stephen Hudson',
    author_email='shudson@anl.gov',
    license='BSD 2-clause',
    packages=['pyexample'],
    install_requires=['mediapipe',
                        'pygame',
                        'pyglet',
                        'screeninfo',
                        'opencv-python',
                        'openpyxl',
                        'pandas',
    ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)