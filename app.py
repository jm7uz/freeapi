from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://users_data_gjpa_user:lPRq94fX7KBrUbRFg1SqK97goEWAh8Oh@dpg-cpm2nqqj1k6c739vt06g-a.oregon-postgres.render.com:5432/users_data_gjpa'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.BigInteger, primary_key=True)
    full_name = db.Column(db.String, nullable=False)
    quiz_start = db.Column(db.String, nullable=False)
    quiz_end = db.Column(db.String, nullable=False)
    quiz_result = db.Column(db.Integer, nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There jm!</h1>"

@app.route('/api/user_data', methods=['POST'])
def video_watched():
    data = request.get_json()
    user_id = data.get('user_id')
    full_name = data.get('full_name')
    quiz_start = data.get('quiz_start')
    quiz_end = data.get('quiz_end')
    quiz_result = data.get('quiz_result')

    new_user = User(
        id=user_id,
        full_name=full_name,
        quiz_start=quiz_start,
        quiz_end=quiz_end,
        quiz_result=quiz_result
    )
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "Data added."}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@app.route('/api', methods=['GET'])
def video_watcheds():
    try:
        all_users = User.query.all()
        users_list = [{"id": user.id, "full_name": user.full_name, "quiz_start": user.quiz_start, 
                       "quiz_end": user.quiz_end, "quiz_result": user.quiz_result} for user in all_users]
        return jsonify({"users": users_list}), 200
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/top_users', methods=['GET'])
def top_users():
    try:
        query_result = db.session.query(
            User.id,
            User.full_name,
            User.quiz_result,
            func.EXTRACT('EPOCH', (User.quiz_end.cast(db.TIMESTAMP) - User.quiz_start.cast(db.TIMESTAMP))).label('duration_seconds')
        ).order_by(
            User.quiz_result.desc(),
            func.EXTRACT('EPOCH', (User.quiz_end.cast(db.TIMESTAMP) - User.quiz_start.cast(db.TIMESTAMP))).asc()
        ).all()

        results = []
        for row in query_result:
            result_dict = {
                'id': row.id,
                'full_name': row.full_name,
                'quiz_result': row.quiz_result
            }
            results.append(result_dict)

        return jsonify(results), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
