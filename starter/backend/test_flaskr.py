import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres', 'admin','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)


        # sample question for use in tests
        self.new_question = {
            'question': 'Who is the inventor of Windows Operation System?',
            'answer': 'Bill Gates',
            'difficulty': 1,
            'category': 1
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after each test"""
        # deleting a question to keep the database records count constant every time the test is run
        if len(Question.query.all()) > 1:
            Question.query.first().delete()

        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # testing of applying pagination to the questions obtained
    # in case of successful endpoint
    def test_get_paginated_questions(self):

        # create a new question to the database
        question = Question(question=self.new_question['question'], answer=self.new_question['answer'],
                            category=self.new_question['category'], difficulty=self.new_question['difficulty'])
        question.insert()


        # starting the test
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
    
    # in case of unsuccessful endpoint
    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000', json={'rating': 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    #-------------------------------------------------------------------------------------------------------#
    #-------------------------------------------------------------------------------------------------------#    

    # testing endpoint in case of searching for a question using search term
    # in case of search that gets a number of results
    def test_get_question_search_with_results(self):
        res = self.client().post('/questions/search', json={'searchTerm': 'who'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertEqual(len(data['questions']), 1)

    # in case of search that gets no results 
    def test_get_question_search_without_results(self):
        res = self.client().post('/questions/search', json={'searchTerm': 'apple'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    #-------------------------------------------------------------------------------------------------------#
    #-------------------------------------------------------------------------------------------------------#
    
    def test_delete_question(self):

        # getting the question by id
        question_id = Question.query.one_or_none().id

        # delete the question and store response
        res = self.client().delete('/questions/{}'.format(question_id))
        data = json.loads(res.data)

        # check status code and success message
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        # check if question id matches deleted id
        self.assertEqual(data['deleted'], question_id)

    #-------------------------------------------------------------------------------------------------------#
    #-------------------------------------------------------------------------------------------------------#
    
    def test_add_question(self):

        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        # check status code and success message
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        # check count of questions (should be equal to 2)
        self.assertTrue(len(Question.query.all()) == 2)

    #-------------------------------------------------------------------------------------------------------#
    #-------------------------------------------------------------------------------------------------------#

    def test_get_questions_by_category(self):

        res = self.client().get('categories/1/questions')
        data = json.loads(res.data)

        # check response status code and message
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        # check that questions are returned
        self.assertNotEqual(len(data['questions']), 0)

         # check that current category returned is science
        self.assertEqual(data['current_category'], 'Science')

    #-------------------------------------------------------------------------------------------------------#
    #-------------------------------------------------------------------------------------------------------#

    def test_play_quiz_game(self):
    ## Tests playing quiz game success

        # send post request with category and previous questions
        response = self.client().post('/quizzes',
                                      json={'previous_questions': [17,18],
                                            'quiz_category': {'type': 'Science', 'id': '1'}})

        # load response data
        data = json.loads(response.data)

        # check response status code and message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

        # check that a question is returned
        self.assertTrue(data['question'])

        # check that the question returned is in correct category
        self.assertEqual(data['question']['category'], 1)

        # check that question returned is not on previous q list
        self.assertNotEqual(data['question']['id'], 17)
        self.assertNotEqual(data['question']['id'], 18)

                            #-----------------------------------------------#

    def test_play_quiz_fails(self):
    ## Tests playing quiz game failure 400

        # send post request without json data
        response = self.client().post('/quizzes', json={})

        # load response data
        data = json.loads(response.data)

        # check response status code and message
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')
        
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()