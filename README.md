This is test task for DF designer project (backend part).
Features:
* files parsing and error log generation (`app.py`, `parse_graph.py`)
* graph layout computing (`layout.py`) via Eades spring embedder
* json from graph
* command line util for files parsing
```
python parse_files.py --folder graphs_to_parse --iterations 100 --width 10 --height 10
```
Here `width` and `height` are low and high ranges for random initialization (to start algorithm)
* [very raw] visualization with html (canvas)  + js.
Backend is implemented on Flask. To launch app:
```
 python app.py --host 0.0.0.0 --port 5050 --folder graphs_to_parse
```
