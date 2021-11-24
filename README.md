
python3 -m venv venv

source venv/bin/activate

python3 -m unittest TestLotPlacement.py

Total of 17 testcases

The idea is to:
- validate input parameters
- validate lot boundaries
- transform lot boundaries (array of coordinates (x, y)) into matrix ([0, 1, 1, 1, 0])
- add setback to the home size
- find the biggest rectangular size that fits into lots boundaries
- check that home size fits into the biggest rectangular size

Big O and space complexity analysis is in the code in the form of comments

