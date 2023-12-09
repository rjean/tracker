from setuptools import setup, find_packages

setup(
    name='Trackingturret',  # Replace with your package's name
    version='0.1',  # Replace with your package's version
    packages=find_packages(),
    install_requires=[
        'tflite-runtime',  # Tensorflow Lite Runtime
        'opencv-python',  # OpenCV2 for Python
        'rtcom', # Real-time communication abstraction
        'pyyaml'
    ],
    author='Raphael Jean',  # Replace with your name
    author_email='raphael.jean@rocketmail.com',  # Replace with your email
    description='A person seeking laser turret',  # Replace with your description
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # If your README is in Markdown
    url='http://raphaeljean..com',  # Replace with your project's URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',  # Adjust depending on your requirements
)

