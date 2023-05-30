import sys
import os
# Add the parent directory to the path so we can import the util package
sys.path.append(os.path.join(os.path.dirname(__file__),"../"))


a = [1,2,3,4,5,6,7,8,9,10]
b = []
for i in a:
    if i == 5:
        a.remove(i)
        continue
    b.append(i)

print(a)
print(b)