# summer-holiday

## api (python)
prerequisite: an up to date version of python

in the command line, go to the api folder:
```bash
cd api
```

### setup
initialise a virtual environment (this may be different with conda):
```bash
# create venv
python -m venv .venv
# activate venv
.venv/Scripts/activate
```

install dependencies
```bash
pip install -r requirements.txt
```

### development
```bash
fastapi dev main.py
```

## web (svelte + ts)
prerequisite: npm must be installed 

in the command line, go to the web folder:
```bash
cd web
```

### setup
install dependencies:
```bash
npm install
```

### development
to run dev server:
```bash
npm run dev
```