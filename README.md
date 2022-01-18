#Pi Display
A display designed for the official Raspberry Pi 7" touchscreen (should work on most screens though).  Includes integration with [Snapcast](https://github.com/badaix/snapcast) for controlling client sound and sources (more integrations coming soon!).

![Pi Display](https://i.imgur.com/D5hvAvE.gifv)

##Requirements
[Gtk 3](https://www.gtk.org)
[Python 3](https://www.python.org/)
[PyGObject dependencies](https://pygobject.readthedocs.io/en/latest/getting_started.html)

## Setup
1. Create a virtual environment in the root directory (and activate it):
    - `python3 -m venv env`
    - `source env/bin/activate`
2. Install dependencies: `pip install -r requirements.txt`
3. Rename `src/.env.example` to `src/.env` and update variables
    - Setting `ENVIRONMENT=dev` prevents the screen from opening maximized
4. Start the application with `python src/main.py`
