from logging import error
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy.sql.sqltypes import INTEGER
from models import setup_db, Question, Category


QUESTIONS_PER_PAGE = 10

# Setting up pagination for questions


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    @TODO: Set up CORS. Allow '*' for origins.
    Delete the sample route after completing the TODOs
    '''
    cors = CORS(app, resources={"/": {"origins": "*"}})
    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    '''
    @TODO:
    Create an endpoint to handle GET requests -->> Done
    for all available categories.
    '''
    @app.route('/categories')
    def get_categories():
        # getting all categories and adding them to a dictionary to match
        # the requirements of the front-end
        categories = Category.query.all()
        categories_dict = {}
        for category in categories:
            categories_dict[category.id] = category.type

        # abort 404 if no categories found
        if (len(categories_dict) == 0):
            abort(404)

        # return data to view
        return jsonify({
            'success': True,
            'categories': categories_dict
        })
    '''
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories. -->> DONE

    TEST: At this point, when you start the application -->> DONE
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the
    screen for three pages.
    Clicking on the page numbers should update the questions.
    '''

    @app.route('/questions', methods=['GET'])
    def get_questions():
        # getting all the questions and applying the required pagination
        questions = Question.query.all()
        formatted_questions = paginate_questions(request, questions)

        # abort (404) if no questions were obtained
        if len(formatted_questions) == 0:
            abort(404)
        '''
        getting the categories as a dictionary in the '/questions' route
        to fulfill the front-end requirements
        '''
        categories = Category.query.all()

        categories_dict = {}
        for category in categories:
            categories_dict[category.id] = category.type

        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'total_questions': len(questions),
            'categories': categories_dict
        })

    '''
    @TODO:
    Create an endpoint to DELETE question using a question ID. -->> DONE

    TEST: When you click the trash icon next to a question,
    the question will be removed.
    This removal will persist in the database and when you refresh the page.
    '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            # getting the question by id
            question = Question.query.filter(
                        Question.id == question_id).one_or_none()

            # abort (404) if no question found
            if question is None:
                abort(404)

            # delete the question
            question.delete()
            current_questions = Question.query.all()

            return jsonify({
              'success': True,
              'deleted': question_id,
              'questions': current_questions,
              'total_questions': len(current_questions)
            })

        except Exception as error:
            print(error)
            # abort (422) if an error occured during deleting process
            abort(422)

    '''
    @TODO:
    Create an endpoint to POST a new question, -->> DONE
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab, -->> DONE
    the form will clear and the question will appear at the end
    of the last page
    of the questions list in the "List" tab.
    '''

    @app.route('/questions', methods=['POST'])
    def post_question():
        # loading the request body
        body = request.get_json()

        # loading data from body
        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)

        # ensure all fields have data
        if ((new_question is None) or (new_answer is None)
                or (new_difficulty is None) or (new_category is None)):
            abort(422)

        try:
            # creating a new question
            question = Question(question=new_question, answer=new_answer,
                                category=new_category,
                                difficulty=new_difficulty)

            # inserting the question
            question.insert()

            # getting all of the questions and applying pagination
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            # returning data to the front-end
            return jsonify({
              'success': True,
              'created': question.id,
              'question_created': question.question,
              'questions': current_questions,
              'total_questions': len(Question.query.all())
            })

        except Exception as error:
            print(error)
            abort(422)
    '''
    @TODO:
    Create a POST endpoint to get questions based on a search term. -->> DONE
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''
    @app.route('/questions/search', methods=['POST'])
    def search_question():
        # getting the request body
        body = request.get_json()

        # getting the search term provided by the user
        search_term = body.get('searchTerm')

        # query the database using search term
        selection = Question.query.filter(Question.question.ilike(
          f'%{search_term}%')).all()

        # 404 if no results found
        if (len(selection) == 0):
            abort(404)

        # paginate the results
        questions_paginated = paginate_questions(request, selection)

        # return results
        return jsonify({
            'success': True,
            'questions': questions_paginated,
            'total_questions': len(Question.query.all())
              })

    '''
    @TODO:
    Create a GET endpoint to get questions based on category. -->> DONE

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''
    @app.route('/categories/<int:id>/questions')
    def get_questions_by_category(id):
        # getting the category by id
        category = Category.query.filter_by(id=id).one_or_none()

        # abort (400) if no category was found
        if (category is None):
            abort(400)

        # getting questions of the selected category
        selection = Question.query.filter_by(category=category.id).all()

        # applying pagination on the questions obtained
        questions_paginated = paginate_questions(request, selection)

        # return data to the front-end
        return jsonify({
          'success': True,
          'questions': questions_paginated,
          'total_questions': len(selection),
          'current_category': category.type
        })

    '''
    @TODO:
    Create a POST endpoint to get questions to play the quiz. -->> DONE
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''
    @app.route('/quizzes', methods=['POST'])
    def get_random_quiz_question():

        # loading the request body
        body = request.get_json()

        # getting the previous question
        previous = body.get('previous_questions')

        # getting the category
        category = body.get('quiz_category')

        # abort 400 if category or previous questions isn't found
        if ((category is None) or (previous is None)):
            abort(400)

        # loading all questions if 'ALL' is selected
        if (category['id'] == 0):
            questions = Question.query.all()

        # otherwise loading questions of a certain selected category
        else:
            questions = Question.query.filter_by(category=category['id']).all()

        # counting of questions obtained
        questions_obtained_count = len(questions)

        # random selection of a question from the obtained ones
        def get_random_question():
            return questions[random.randrange(0, questions_obtained_count, 1)]

        # checking if the questions has been already used
        def check_if_used(question):
            used = False
            for q in previous:
                if (q == question.id):
                    used = True

            return used

        # getting a random question by calling the previously defined function
        question = get_random_question()

        # Ensuring that the question was not used before
        while (check_if_used(question)):
            question = get_random_question()

        # if all obtained questions have been used, return without a question
        # that's necessary if the category questions count is less than 5
            if (len(previous) == questions_obtained_count):
                return jsonify({
                    'success': True
                })

            return jsonify({
                    'success': True,
                    'question': question.format()
                })

    '''
    @TODO:
    Create error handlers for all expected errors -->> DONE
    including 404 and 422.
    '''

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
            }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
            }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable entity"
            }), 422

    return app
