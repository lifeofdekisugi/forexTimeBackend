
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///DATABASE.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dbname = db.Column(db.String)
    dbbalance = db.Column(db.String)
    # date_created = db.Column(db.DateTime, default=datetime.utcnow())

@app.route('/')
def hello_world():
    return jsonify({
        'response' : 'Working'
    })

@app.route('/sign-up', methods=['POST'])
def sign_up():
    try:
        signUpData = request.form
                    
        name = signUpData['name']
        balance = signUpData['balance']
            
        new_user = User(dbname=name, dbbalance=balance)
        db.session.add(new_user)
        db.session.commit()
        print("Name " + name)
        print("Balance " + balance)
        
        return jsonify({'response ' : 'success'})
    except Exception:
        return jsonify({"response " : "error"}) 
    
@app.route('/login', methods=['POST'])    
def login():
    
    loginData = request.form
                    
    name = loginData['name']
    balance = loginData['balance']
    
    user = User.query.filter_by(dbname=name, dbbalance=balance).first()
    
    userID = user.id
    userName = user.dbname
    userBalance = user.dbbalance
    
    return jsonify({
        'response' : 'success',
        'id' : userID,
        'name' : userName,
        'balance' : userBalance
    })

@app.route('/view-user', methods=['GET'])
def view_user():
    
    user = User.query.all()
    output = []
        
    for user in user:
        user_data = {}
        user_data['id'] = user.id
        user_data['name'] = user.dbname
        user_data['balance'] = user.dbbalance
                
        output.append(user_data)
            
    return jsonify({
        'All Users' : output
        })

@app.route('/delete-user', methods=['GET'])
def delete_user():
    id = request.args.get('id')
        
    delete_user = User.query.filter_by(id=id).first()
    db.session.delete(delete_user)
    db.session.commit()
        
    return jsonify({
        'response' : 'success'
        })



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)