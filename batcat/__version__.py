VERSION = (0, 0, 5)

__version__ = '.'.join(map(str, VERSION))

# python3 setup.py bdist_wheel
# twine upload dist/*

# pip3 install dist/my-project.whl