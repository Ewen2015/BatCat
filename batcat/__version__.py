VERSION = (0, 2, 50)

__version__ = '.'.join(map(str, VERSION))

# python3 setup.py bdist_wheel
# python3 -m twine upload dist/*

# pip3 install dist/my-project.whl