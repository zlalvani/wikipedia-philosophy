### Wikipedia Philosophy Crawler

This Python program will produce a distribution of how many clicks it takes to reach a given target article, assuming the first valid link on each article is clicked.

Any Wikipedia article is guaranteed to be visited only once.

Installation:
```
pyvenv venv
source venv/bin/activate
pip install -r requirements.txt
```

Example usage:
```
python main.py Philosophy 500 --plot --save
```

For help:
```
python main.py -h
```
