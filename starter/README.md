# Full Stack API Final Project

## Full Stack Trivia

This project is a questions game where users can test their knowledge answering trivia questions. The task for the project was to create an API and test suite for implementing the following functionality:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category without repeating questions.
6. Show the results of the player after he / she finishes his / her test.

## Getting Started

### Installing Dependencies

Developers using this project should already have Python3, pip, node, and npm installed.

#### Frontend Dependencies

This project uses NPM to manage software dependencies. npm Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:
```
    npm install
```
#### Backend Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the `/backend` directory and running:
```
    pip install -r requirements.txt
```
## Running the Frontend in Dev Mode

* The frontend app was built using create-react-app. In order to run the app in development mode use `npm start`.

* Open `http://localhost:3000` to view it in the browser. The page will reload if you make edits.
```
    npm start
```
## Running the Server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

`export FLASK_APP=flaskr`
`export FLASK_ENV=development`
`flask run`

## Testing

* To run the tests, run in your terminal
```
    dropdb trivia_test
    createdb trivia_test
    psql -U postgres trivia_test
    python test_flaskr.py
```
* Omit the `dropdb trivia_test` command the first time you run tests.

## API Reference

### Getting Started

* Base URL: Currently this application is only hosted locally. The backend is hosted at `http://127.0.0.1:5000/`
* Authentication: This version does not require authentication or API keys.

### Error Handling

Errors are returned as JSON in the following format:

```json
{
    "success": False,
    "error": 404,
    "message": "resource not found"
}
```
The API will return three types of errors:

> * 400 – bad request
> * 404 – resource not found
> * 422 – unprocessable


### Endpoints

#### **GET /categories**

* General: Returns a list categories.
* Sample: `curl http://127.0.0.1:5000/categories`

```json
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}
```
#### **GET /questions**

> * Returns a list questions.
> * Results are paginated in groups of 10.
> * Also returns list of categories and total number of questions.

Sample: ```curl http://127.0.0.1:5000/questions```

```json
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "questions": [
    {
      "answer": "Abu Bakr El-Razi", 
      "category": 1, 
      "difficulty": 5, 
      "id": 3, 
      "question": "Who is the first one who separate Pharmacy away from Medicine?"
    }, 
    {
      "answer": "4", 
      "category": 6, 
      "difficulty": 1, 
      "id": 15, 
      "question": "How many times does Germany wins World Cup?"
    }, 
    {
      "answer": "Cairo", 
      "category": 3, 
      "difficulty": 1, 
      "id": 18, 
      "question": "What is the name of Egypt Capital?"
    }, 
    {
      "answer": "Mediterranean Sea", 
      "category": 3, 
      "difficulty": 1, 
      "id": 19, 
      "question": "What is the name of the sea north to Egypt?"
    }, 
    {
      "answer": "Guido Van Rossum", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "Who is the Python inventor ?"
    }, 
    {
      "answer": "Nicolas Cage", 
      "category": 2, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who is the star of Lord of Wars movie?"
    }, 
    {
      "answer": "Ahmed Helmy", 
      "category": 5, 
      "difficulty": 1, 
      "id": 22, 
      "question": "Who is the star of Asal Aswad Movie?"
    }, 
    {
      "answer": "HIV", 
      "category": 1, 
      "difficulty": 2, 
      "id": 23, 
      "question": "What is the virus that causes AIDS?"
    }, 
    {
      "answer": "Neuer", 
      "category": 6, 
      "difficulty": 2, 
      "id": 24, 
      "question": "Who is Germany national football team goal keeper?"
    }, 
    {
      "answer": "Jeff Bezos", 
      "category": 5, 
      "difficulty": 3, 
      "id": 25, 
      "question": "Who is the owner of Amazon?"
    }
  ], 
  "success": true, 
  "total_questions": 11
}
```

#### **DELETE /questions/<int:id>**

> * Deletes a question by id using url parameters.
> * Returns id of deleted question upon success.

Sample: ```curl http://127.0.0.1:5000/questions/3 -X DELETE```

```json
    {
        "deleted": 3, 
        "success": true
    }
```

#### **POST /questions** -- Create New Questions

> * Creates a new question using JSON request parameters.
> * Returns JSON object with newly created question, as well as paginated questions.

Sample: ```curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{ "question": "Who is the star of Lord of Wars movie?", "answer": "Nicolas Cage", "difficulty": 3, "category": 2 }'```

```json
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  1948  100  1833  100   115  29095   1825 --:--:-- --:--:-- --:--:-- 30920{
  "created": 27,
  "question_created": "Who is the star of Lord of Wars movie?",
  "questions": [
    {
      "answer": "Abu Bakr El-Razi",
      "category": 1,
      "difficulty": 5,
      "id": 3,
      "question": "Who is the first one who separate Pharmacy away from Medicine?"
    },
    {
      "answer": "4",
      "category": 6,
      "difficulty": 1,
      "id": 15,
      "question": "How many times does Germany wins World Cup?"
    },
    {
      "answer": "Cairo",
      "category": 3,
      "difficulty": 1,
      "id": 18,
      "question": "What is the name of Egypt Capital?"
    },
    {
      "answer": "Mediterranean Sea",
      "category": 3,
      "difficulty": 1,
      "id": 19,
      "question": "What is the name of the sea north to Egypt?"
    },
    {
      "answer": "Guido Van Rossum",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "Who is the Python inventor ?"
    },
    {
      "answer": "Nicolas Cage",
      "category": 2,
      "difficulty": 3,
      "id": 21,
      "question": "Who is the star of Lord of Wars movie?"
    },
    {
      "answer": "Ahmed Helmy",
      "category": 5,
      "difficulty": 1,
      "id": 22,
      "question": "Who is the star of Asal Aswad Movie?"
    },
    {
      "answer": "HIV",
      "category": 1,
      "difficulty": 2,
      "id": 23,
      "question": "What is the virus that causes AIDS?"
    },
    {
      "answer": "Neuer",
      "category": 6,
      "difficulty": 2,
      "id": 24,
      "question": "Who is Germany national football team goal keeper?"
    },
    {
      "answer": "Jeff Bezos",
      "category": 5,
      "difficulty": 3,
      "id": 25,
      "question": "Who is the owner of Amazon?"
    }
  ],
  "success": true,
  "total_questions": 12
}

```
#### **POST /questions/search** -- Search Questions using searchTerm

> * Searches for questions using search term in JSON request parameters.
> * Returns JSON object with paginated matching questions.

Sample: ```curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm": "Egypt"}'```

```json
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   429  100   406  100    23   8638    489 --:--:-- --:--:-- --:--:--  9127{
  "questions": [
    {
      "answer": "Cairo",
      "category": 3,
      "difficulty": 1,
      "id": 18,
      "question": "What is the name of Egypt Capital?"
    },
    {
      "answer": "Mediterranean Sea",
      "category": 3,
      "difficulty": 1,
      "id": 19,
      "question": "What is the name of the sea north to Egypt?"
    }
  ],
  "success": true,
  "total_questions": 12
}

```

#### **GET /categories/<int:id>/questions**

> * Gets questions by category id using url parameters.
> * Returns JSON object with paginated matching questions.

Sample: ```curl http://127.0.0.1:5000/categories/1/questions```

```json
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   618  100   618    0     0   603k      0 --:--:-- --:--:-- --:--:--  603k{
  "current_category": "Science",
  "questions": [
    {
      "answer": "Abu Bakr El-Razi",
      "category": 1,
      "difficulty": 5,
      "id": 3,
      "question": "Who is the first one who separate Pharmacy away from Medicine?"
    },
    {
      "answer": "Guido Van Rossum",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "Who is the Python inventor ?"
    },
    {
      "answer": "HIV",
      "category": 1,
      "difficulty": 2,
      "id": 23,
      "question": "What is the virus that causes AIDS?"
    }
  ],
  "success": true,
  "total_questions": 3
}

```
#### **POST /quizzes**

> * Allows users to play the quiz game.
> * Uses JSON request parameters of category and previous questions.
> * Returns JSON object with random question not among previous questions.

Sample: ```curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [15, 16], "quiz_category": {"type": "Science", "id": "1"}}'```

```json
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   264  100   183  100    81   178k  81000 --:--:-- --:--:-- --:--:--  257k{
  "question": {
    "answer": "Guido Van Rossum",
    "category": 1,
    "difficulty": 4,
    "id": 20,
    "question": "Who is the Python inventor ?"
  },
  "success": true
}
```

