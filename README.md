Full Stack Trivia API "Trivia-App"
-----

### Introduction

 A Full-Stack Web Application based on Flask. Trivia-App is a trivia game with following features:

1) Display questions - both all questions and by category. Questions show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

### Main Files: Project Structure

  ```sh
  ├── README.md
  ├── backend *** Contains API and test suites.
  │   ├── README.md *** Contains backend server setup and API documentations.
  │   ├── config.py *** Contains information for database connection.
  │   ├── models.py
  │   ├── flaskr
  │   │   └── __init__.py *** App creation & API endpoints.
  │   ├── requirements.txt *** The dependencies to be installed with "pip3 install -r requirements.txt"
  │   └── test_flaskr.py *** 9 unittests to check expected behaviour from each endpoints
  │   └── trivia.psql *** database dumb, restore with "psql trivia < trivia.psql"
  └── frontend *** start frontend with "npm start"
      ├── README.md *** Contains Frontend Setup 
      └── src
          └── components *** Contains React Components
  ```

### Setup Project locally

To start the project locally, you need to setup both `backend` and `frontend` seperatly.
I suggest to start with the `backend` setup, because the `React-App` consumes the data from the `flask server`. 

1. [`./frontend/`](./frontend/README.md)
2. [`./backend/`](./backend/README.md)