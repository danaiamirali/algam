# algam
Combining hot topics across different social media platforms into one. 

![alt text](img/algam.png)

The project is comprised of three components:
1. A Python Package, `algamlib`, for fetching hot topics from social media platforms
2. A FastAPI + Postgres Backend, using `algamlib` on a timer to update a running database of trending topics over time and serving these topics on an API route
3. A ReactJS Frontend using the FastAPI route to show current hot topics in a word cloud interface

## `algamlib`

To use algamlib, simply run:
```
cd algamlib
pip install -r requirements.txt
pip install ./
```

When developing algamlib, verify functionality using the `pytest` framework.
```
cd algamlib
pip install -r requirements-test.txt
pytest tests/
```

## The Backend

To start the backend server, simply run:
```
cd backend
pip install -r requirements.txt
python3 -m uvicorn main:app --host 0.0.0.0 --port 8080
```

## The Frontend

To run the frontend, simply run:
```
cd frontend/algam
npm start
```
For the frontend to be functional, the backend server must also be running. You may have to modify the specific routes called in `App.js` depending on where you host the backend.
