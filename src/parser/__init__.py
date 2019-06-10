"""
General functions for LaTeX manipulation.
Imitating https://github.com/python/cpython/tree/3.7/Lib/html 
"""
with open('/home/yzan/Desktop/Cleanskin/data/paper.tex', mode='r', encoding='utf-8') as f:
    data = f.readlines()

print(data[:50])