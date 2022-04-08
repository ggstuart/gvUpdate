Python library for maintaining json files using Greenview web service
===

Installation
---

Download the source file gvUpdate.py and run it with python

    python gvUpdate.py


Alternatively, write a small script like this - it will need to be located next to the gvUpdate.py for the import to work

    import os.path, logging
    import gvUpdate

    root = os.path.join('path', 'to', 'data', 'location')
    if not os.path.exists(root): os.makedirs(root)
    logFile = os.path.join(root, 'update.log')
    logging.basicConfig(filename=logFile, level=logging.WARNING, format='%(levelname)s: %(asctime)s %(message)s')
    gvUpdate.main(root)
