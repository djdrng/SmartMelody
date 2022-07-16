# :musical_note: SmartMelody

**University of Waterloo**

**Department of Electrical & Computer Engineering**

- Arnav Singh
- Ayan Khan
- Devinn Doering
- Ted Liu
- Zahin Zaman

## Installation

:one: Install [Python](https://www.python.org/).

:two: Create and activate Python virtual environment (optional but recommended).

```bash
python3 -m venv env
source env/bin/activate # Linux & MacOS
source env/Scripts/activate # Windows
```

:three: Install backend dependencies

```bash
cd backend/
pip3 install -r requirements.txt
```

## Running the Server

```bash
cd backend/
uvicorn server:app --reload
```

This should start the server running at `http://localhost:8000/`.

To get a recommendation, send a GET request to the `/get-recommendations` endpoint.

```bash
curl http://localhost:8000/get-recommendations?mood=happy
```

## API Documentation

![API Docs](img/api_docs_screenshot.png)
