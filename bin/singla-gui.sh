BINDIR=$(dirname $(readlink -f ${0}))
cd ${BINDIR}/../
./venv/bin/python ./main.py