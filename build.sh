
./setup.py check
rm -rf ./dist ./*.egg-info
python3 -m build --sdist
if [twine check dist/*] then ;
    twine upload --repository testpypi dist/*
    twine upload dist/*
    sleep 10
    # pip install --upgrade dynascii
fi