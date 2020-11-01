# xorshift128plus-cracker
⚙️A python script that "cracks" the Xorshift128+ pseudorandom number generator.

Only works on Math.random() in Firefox. But it only requires small changes to make it work in other browsers.
# Getting Started 
## 1. Install dependencies
```
$ pip install -r requirements.txt
```
## 2. Generate random numbers
Generate 3 or more numbers with Math.random() in **Firefox**
```
[Math.random(), Math.random(), Math.random(), Math.random()]
> [ 0.20984993117622008, 0.031103469229328495, 0.6396434426372385, 0.16934810845148796 ]
```
## 3. Open CMD and cd into the directory
After that type:
```
$ python xorshift128plus-cracker.py 
```
\+ the 3 numbers that you generated. **DON'T FORGET TO REMOVE SPACES.** 

Example: ```$ python xorshift128plus-cracker.py 0.20984993117622008,0.031103469229328495,0.6396434426372385```
## 4. Done
After that the script will print 15 (this number can be changed) numbers that will be generated next.
