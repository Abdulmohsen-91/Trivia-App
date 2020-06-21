import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate(request, selection):
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
  Setting up CORS. Allow '*' for origins.
  '''
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  '''
  Setting Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response

  '''
  Endpoint to handle GET requests for all available categories.
  '''

  @app.route('/categories')
  def get_categories():
    categories = Category.query.order_by(Category.type).all()
    #print(len(categories))
    if len(categories) == 0:
      abort(404)
    
    return jsonify({
      'success': True,
      'categories': {category.id: category.type for category in categories}
    })

  '''
  Endpoint to handle GET requests for questions
  '''

  @app.route('/questions')
  def get_questions():
    selection = Question.query.order_by(Question.id).all()
    questions_paginated = paginate(request, selection)
    categories = Category.query.order_by(Category.type).all()
    if len(questions_paginated) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': questions_paginated,
      'total_questions': len(selection),
      'categories': {category.id: category.type for category in categories}
    })

  '''
  Endpoint to DELETE question using a question ID.
  '''

  @app.route('/questions/<question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.get(question_id)
      question.delete()

      return jsonify({
        'success': True,
        'deleted': question_id
        })
    except:
      abort(422)

  '''
  Endpoint to POST a new question. 
  '''
  @app.route('/questions', methods = ['POST'])
  def add_question():
    jsonBody = request.get_json()

    newQuestion = jsonBody.get('question')
    newAnswer = jsonBody.get('answer')
    newDifficulty = jsonBody.get('difficulty')
    newCategory = jsonBody.get('category')

    try:
      question = Question(question=newQuestion, answer=newAnswer, difficulty=newDifficulty, category=newCategory)
      question.insert()

      return jsonify({
        'success': True,
        'created': question.id
        })
    except:
      abort(422)

  '''
  Endpoint to get questions based on a search term.
  '''

  @app.route('/questions/search', methods=['POST'])
  def search_Question():
    jsonBody = request.get_json()
    search_term = jsonBody.get('searchTerm')

    try:
      results = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
      return jsonify({
        'success': True,
        'questions': [question.format() for question in results],
        'total_questions': len(results)
        })
    except:
      abort(404)

  '''
  Endpoint to get questions based on category.
  '''

  @app.route('/categories/<int:category_id>/questions')
  def get_questions_by_category(category_id):
    try:
      questions = Question.query.filter(Question.category == str(category_id)).all()

      return jsonify({
        'success': True,
        'questions': [question.format() for question in questions],
        'total_questions': len(questions)
        })
    except:
        abort(404)


  '''
  Endpoint to get questions to play the quiz.
  '''

  @app.route('/quizzes', methods=['POST'])
  def play():
    jsonBody = request.get_json()

    category = jsonBody.get('quiz_category')
    previous_questions = jsonBody.get('previous_questions')

    try:
      if category['id'] == 0:
        questions = Question.query.all()  

      else:
        questions = Question.query.filter_by(category=category['id']).all()
        
      next_question = questions[random.randrange(0, len(questions))].format() if len(questions) > 0 else None

      return jsonify({
        'success': True,
        'question': next_question
        })
    except:
      abort(422)

    


  '''
  Error handlers for all expected errors 
  including 404 and 422. 
  '''

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'resource not found'
    }), 404
  
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': 'unprocessable'
    }), 422
  
  return app

    