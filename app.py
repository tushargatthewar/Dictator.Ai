from flask import Flask, render_template, request, jsonify, redirect, url_for, make_response
from datetime import datetime, timedelta
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from functools import wraps
import requests
import uuid
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus
from prompt import generate_prompt
from prompt2 import generate_prompt1








# ---------------------------
# CONFIG
# ---------------------------
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "super_secret_key")
JWT_SECRET = os.getenv("JWT_SECRET", "super_secret_key_jwt") 
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_MINUTES = 30









# ---------------------------
# MONGO
# ---------------------------
load_dotenv()
username = quote_plus(os.getenv("MONGO_USER"))
password = quote_plus(os.getenv("MONGO_PASS"))
mongo_url = os.getenv("MONGO_URI")
client = MongoClient(mongo_url)
db = client["DictatorsAI"]
users = db["Users"]
chat_sessions = db["chat_sessions"]











# ---------------------------
# NO CACHE HEADERS
# ---------------------------
@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# ---------------------------
# JWT UTILITIES
# ---------------------------
def generate_jwt(username):
    payload = {
        "username": username,
        "exp": datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_MINUTES),
        "iat": datetime.utcnow()
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    # pyjwt returns str in v2+, ensure str
    return token if isinstance(token, str) else token.decode('utf-8')

def verify_jwt(token):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload.get('username')
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None






# ---------------------------
# LOGIN REQUIRED DECORATOR
# ---------------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get('jwt_token')
        if not token:
            return redirect(url_for('login'))
        username = verify_jwt(token)
        if not username:
            return redirect(url_for('login'))
        return f(username, *args, **kwargs)
    return decorated_function





# ---------------------------
# ROUTES - AUTH + PAGES
# ---------------------------
@app.route('/')
@login_required
def home(username):
    response = make_response(render_template('index1.html', username=username))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    return response

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        user = users.find_one({"username": username})
        if user and check_password_hash(user["password"], password):
            token = generate_jwt(username)
            resp = make_response(redirect(url_for('home')))
            resp.set_cookie(
                'jwt_token',
                token,
                httponly=True,
                samesite='Lax',
                secure=False,  # switch to True when serving over HTTPS
                max_age=JWT_EXPIRATION_MINUTES * 60
            )
            return resp
        else:
            return render_template('login.html', error="Invalid username or password")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        if users.find_one({"username": username}):
            return render_template('register.html', error="Username already exists!")
        hashed_pw = generate_password_hash(password)
        users.insert_one({
            "username": username,
            "password": hashed_pw,
            "created_at": datetime.utcnow()
        })
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('login')))
    resp.delete_cookie('jwt_token')
    return resp






# ---------------------------
# CHAT SESSIONS + LLM INTEGRATION
# ---------------------------

@app.route('/new_chat', methods=['POST'])
def new_chat():
    token = request.cookies.get('jwt_token')
    username = verify_jwt(token)
    if not username:
        return jsonify({'status': 'error', 'message': 'Please login first!'}), 401

    session_id = str(uuid.uuid4())
    chat_sessions.insert_one({
        "username": username,
        "session_id": session_id,
        "title": None,     #Here chat histry renameing title
        "messages": [],  # list of {role, content, time}
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    })
    return jsonify({'status': 'ok', 'session_id': session_id})

@app.route('/chat', methods=['POST'])
def chat():
    token = request.cookies.get('jwt_token')
    username = verify_jwt(token)
    if not username:
        return jsonify({'reply': 'Please login first!'}), 401

    data = request.get_json() or {}
    user_message = data.get('message')
    session_id = data.get('session_id')
    selected_role = data.get('role')
    model=data.get('model','private')
    print(selected_role)
    print("######################################################################################")
    print(model)
    if model=="Private":
        prompt=generate_prompt1(selected_role,user_message)
    else:
        prompt=generate_prompt(selected_role,user_message)




    if not user_message:
        return jsonify({'reply': 'Please type a message!'}), 400
    if not session_id:
        return jsonify({'reply': 'Invalid session ID!'}), 400

    # Verify session belongs to user
    sess = chat_sessions.find_one({"username": username, "session_id": session_id})
    if not sess:
        return jsonify({'reply': 'Session not found'}), 404
    # ---- AUTO SET TITLE BASED ON FIRST USER MESSAGE ----
    if sess.get("title") is None:  
        # take first 4 words of the user's first query
        words = user_message.strip().split()
        title = " ".join(words[:4])  # first 4 words

        # save title permanently
        chat_sessions.update_one(
            {"username": username, "session_id": session_id},
            {"$set": {"title": title}}
        )


    # Save user's message to DB
    user_msg_doc = {"role": "user", "content": user_message, "time": datetime.utcnow()}
    chat_sessions.update_one(
        {"username": username, "session_id": session_id},
        {"$push": {"messages": user_msg_doc}, "$set": {"updated_at": datetime.utcnow()}}
    )
    if model=="Public":
        url = os.getenv("LLM_URL1")
        api=os.getenv("LLM_KEY1")


        headers = {
        "Authorization": f"Bearer {api}",
        "Content-Type": "application/json"
        }



        # Prepare payload to LLM
        data = {
            "model": "krishnasuratwala/Dictatorai_speechmodel",
            "messages": [
                {"role":"user", "content": prompt}
            ]
        }
    elif model=="Private":
        url = os.getenv("LLM_URL2")
        api=os.getenv("LLM_KEY2")


        headers = {
        "Authorization": f"Bearer {api}",
        "Content-Type": "application/json"
        }
                # Prepare payload to LLM
        data = {
            "model": "krishnasuratwala/Dictatorai_one_to_one_model",
            "messages": [
                {"role":"user", "content": prompt}
            ]
        }
    else:

        return jsonify({'reply': 'Invalid model selected!'}), 400





    print(data["messages"])

    ai_reply = "⚠️ Error contacting AI server."
    try:
        llm_resp = requests.post(url, json=data, headers=headers, timeout=30)
        llm_resp.raise_for_status()
        llm_json = llm_resp.json()

        # try to robustly extract reply text from common formats
        if isinstance(llm_json, dict):
            # OpenAI-like: choices[0].message.content
            try:
                ai_reply = llm_json["choices"][0]["message"]["content"]
            except Exception:
                # Some APIs return { "choices": [{"text": "..."}] }
                try:
                    ai_reply = llm_json["choices"][0]["text"]
                except Exception:
                    # fallback: maybe top-level "reply" or "output"
                    ai_reply = llm_json.get("reply") or llm_json.get("output") or str(llm_json)
        else:
            ai_reply = str(llm_json)
            # --- MODIFICATION START ---
            # Clean the extracted reply by removing the specific end tag
            if isinstance(ai_reply, str):
                ai_reply = ai_reply.replace("<|im_end|>", "").strip()
            # --- MODIFICATION END ---

            
    except requests.RequestException as e:
        app.logger.error(f"LLM request failed: {e}")
        ai_reply = "⚠️ Error contacting AI server."

    # Save assistant message to DB
    assistant_msg_doc = {"role": "assistant", "content": ai_reply, "time": datetime.utcnow()}
    chat_sessions.update_one(
        {"username": username, "session_id": session_id},
        {"$push": {"messages": assistant_msg_doc}, "$set": {"updated_at": datetime.utcnow()}}
    )

    return jsonify({'reply': ai_reply})






#get chat history

@app.route('/get_history/<session_id>', methods=['GET'])
def get_history(session_id):
    token = request.cookies.get('jwt_token')
    username = verify_jwt(token)
    if not username:
        return jsonify({'status': 'error', 'message': 'Please login first!'}), 401

    chat = chat_sessions.find_one({"username": username, "session_id": session_id}, {"_id": 0})
    if not chat:
        return jsonify({'status': 'error', 'message': 'Session not found'}), 404

    # Convert datetimes to isoformat strings for frontend
    messages = []
    for m in chat.get("messages", []):
        messages.append({
            "role": m.get("role"),
            "content": m.get("content"),
            "time": m.get("time").isoformat() if isinstance(m.get("time"), datetime) else m.get("time")
        })

    return jsonify({'status': 'ok', 'session_id': session_id, 'messages': messages})


#Delete chat session
@app.route('/delete_session/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    token = request.cookies.get('jwt_token')
    username = verify_jwt(token)

    if not username:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    result = chat_sessions.delete_one({
        "username": username,
        "session_id": session_id
    })

    if result.deleted_count == 1:
        return jsonify({"status": "ok"})
    else:
        return jsonify({"status": "error", "message": "Session not found"}), 404
















#JWT AUTHO
@app.route('/sessions', methods=['GET'])
def list_sessions():
    token = request.cookies.get('jwt_token')
    username = verify_jwt(token)
    if not username:
        return jsonify({'status': 'error', 'message': 'Please login first!'}), 401

    #cursor = chat_sessions.find({"username": username}, {"_id": 0, "session_id": 1, "created_at": 1, "updated_at": 1}).sort("updated_at", -1)
    cursor = chat_sessions.find(
    {"username": username},
    {"_id": 0, "session_id": 1, "title": 1, "created_at": 1, "updated_at": 1}
).sort("updated_at", -1) #here is also chnaging for chat histry okay

    sessions = []
    for s in cursor: #here also chnaging for chat histry okay
        sessions.append({
    "session_id": s.get("session_id"),
    "title": s.get("title"),  # <-- ADD THIS
    "created_at": s.get("created_at").isoformat() if isinstance(s.get("created_at"), datetime) else s.get("created_at"),
    "updated_at": s.get("updated_at").isoformat() if isinstance(s.get("updated_at"), datetime) else s.get("updated_at")
})

        # sessions.append({
        #     "session_id": s.get("session_id"),
        #     "created_at": s.get("created_at").isoformat() if isinstance(s.get("created_at"), datetime) else s.get("created_at"),
        #     "updated_at": s.get("updated_at").isoformat() if isinstance(s.get("updated_at"), datetime) else s.get("updated_at")
        # })
    return jsonify({'status': 'ok', 'sessions': sessions})




if __name__ == '__main__':
    app.run(debug=True)
