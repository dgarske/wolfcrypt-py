set -e
set +x

for PYVERSION in 2.7 3.6 3.7; do
    virtualenv -p /Library/Frameworks/Python.framework/Versions/${PYVERSION}/bin/python${PYVERSION} venv_${PYVERSION}
    . ./venv_${PYVERSION}/bin/activate
    curl https://bootstrap.pypa.io/get-pip.py | python
    pip3 install -r requirements/setup.txt
    python3 setup.py bdist_wheel
    pip3 install -r requirements/test.txt
    set +e
    pip3 uninstall -y wolfcrypt
    set -e
    pip3 install wolfcrypt --no-index -f dist
    rm -rf tests/__pycache__
    py.test tests
    deactivate
done
