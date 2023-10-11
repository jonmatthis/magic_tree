# magictreedict 🌱✨

"Defines the `MagicTreeDict` class - which extends  `defaultdict` into an auto-building recursive tree for intuitive 
manipulation, analysis, and visualization of hierarchical data 🌱✨"

# Installation 
 - `git clone https://gitub.com/jonmatthis/magictree`
 - `cd magictree`
 - `pip install -e .`

# Demo
 - Run the demo script: `python magictree/demo.py`
   - or `python -m magictree.demo` if you're into that
   
Expected output (2023-10-11):
```
C:\Users\jonma\AppData\Local\pypoetry\Cache\virtualenvs\magictree-xRvLYKaC-py3.11\Scripts\python.exe C:\Users\jonma\github_repos\jonmatthis\magictree\magic_tree\helpers\demo.py 
Print as regular dict:

{'a': {'b': {'c': {'woo': [1, 2, 13], 'woo2': '✨', 'hey': [71, 8, 9]}, 'bang': [[1, 2, 3], [4, 5, 6], [7, 8, 9]]}, 'c': {'pow': [4, 51, 6]}}}
Original MagicTreeDict:
🌱
└── a
    ├── b
    │   ├── c
    │   │   ├── woo: [1, 2, 13]
    │   │   ├── woo2: ✨
    │   │   └── hey: [71, 8, 9]
    │   └── bang: [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    └── c
        └── pow: [4, 51, 6]



Print Table:

+----+--------------------------+----------------------+--------------------------+
|    |   ('a', 'b', 'c', 'woo') | ('a', 'b', 'bang')   |   ('a', 'b', 'c', 'hey') |
|----+--------------------------+----------------------+--------------------------|
|  0 |                        1 | [1, 2, 3]            |                       71 |
|  1 |                        2 | [4, 5, 6]            |                        8 |
|  2 |                       13 | [7, 8, 9]            |                        9 |
+----+--------------------------+----------------------+--------------------------+
Filter tree on `c`:

🌱
└── a
    ├── b
    │   └── c
    │       ├── woo: [1, 2, 13]
    │       ├── woo2: ✨
    │       └── hey: [71, 8, 9]
    └── c
        └── pow: [4, 51, 6]


Process finished with exit code 0
```



