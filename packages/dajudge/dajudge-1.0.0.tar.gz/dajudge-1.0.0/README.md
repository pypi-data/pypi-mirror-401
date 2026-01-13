# dajudge
ダジャレを判定するモジュール

# Install
```cmd
# Linux/OS
$ python -m pip install -U dajudge

# Windows
> py -3 -m pip install -U dajudge
```    

# Example 
```py
from dajapy import dajudge

# Simple boolean check
if dajudge("布団が吹っ飛んだ"):
    print("It's a pun!")

# Get detailed info
res = dajudge("アルミ缶の上にあるみかん")
print(f"Score: {res.score}")
print(f"Phrase: {res.phrase}")
print(f"Length: {res.length}")
```