from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Career(db.Model):
    __tablename__ = 'careers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    category = db.Column(db.String(50))
    budget = db.Column(db.Integer)
    description = db.Column(db.Text)

@app.route('/api/careers', methods=['GET'])
def get_careers():
    user_interest = request.args.get('interest', '')
    user_budget = request.args.get('budget', type=int)

    if user_budget is None:
        return jsonify({"error": "budget parameter is required"}), 400

    careers = Career.query.filter(
        Career.category.ilike(f"%{user_interest}%"),
        Career.budget <= user_budget
    ).all()

    return jsonify([
        {
            "name": c.name,
            "category": c.category,
            "cost": c.budget,
            "description": c.description
        }
        for c in careers
    ])

if __name__ == '__main__':
    app.run()
