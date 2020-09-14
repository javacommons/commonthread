pip install wheel
rem python setup.py sdist
rmdir /s /q dist
python setup.py bdist_wheel