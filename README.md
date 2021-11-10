# matrix

<!--
title: parse bbc.com
layout: Doc
-->

## How to run

From the directory:
```
$ docker build -t matrix . 
$ docker run -v $(pwd):/app --rm -it matrix /bin/bash
$ python3 main.py ./config.yaml # to run the main
$ python3 search_engine.py ./data "radio live" # to run the search engine (search on articles in data folder)
```

[comment]: <> (C:\Users\tomer\Desktop\matrix_final )

[comment]: <> (docker run -v C:\Users\tomer\Desktop\matrix_final:/app --rm -it matrix /bin/bash)
