<<<<<<< HEAD
VERSION = (0, 2, 16)
=======
VERSION = (0, 2, 20)
>>>>>>> 07ef2c440c2838dbd316a022c1bfc6284e5df02a

__version__ = '.'.join(map(str, VERSION))

# python3 setup.py bdist_wheel
# python3 -m twine upload dist/*

# pip3 install dist/my-project.whl