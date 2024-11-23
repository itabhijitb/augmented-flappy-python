from setuptools import setup, find_packages

setup(
    name='ARFlappy',
    version='0.1.0',
    description='Classic Flappy Game with Augmented Reality',
    url='https://github.com/itabhijitb/augmented-flappy-python',
    author='Aditya Bhattacharjee',
    author_email='email.adityab@gmail.com',
    license='MIT',
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "mycli=flappy.LandingPage:main",  # Format: command=module:function
        ],
    },
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
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Games/Entertainment',
    ],
)