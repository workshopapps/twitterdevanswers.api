from typing import Union

app = FastAPI()
@app.route('/signup',  methods=['POST'])
def sign_up():
    from auth import SignUp
    all_json = request.get_json()
    user_name = all_json.get('user_name')
    #first_name = all_json.get('first_name')
    # last_name = all_json.get('last_name')
    # email = all_json.get('email')
    # password_hash = all_json.get('password_hash')
    # image_url = all_json.get('image')
    

    usr = db.session.query(User).filter_by(user_name=user_name).first()
    print(usr) 

    if not usr:
        new_user = User(**all_json)
        db.session.add(new_user)
        db.session.commit()
        return {"usr": "Signup successful"}
    else:
        return {'Error': "Username already exist"}, 409


