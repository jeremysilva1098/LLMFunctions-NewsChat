from flask import Flask, render_template, request, jsonify
import os
from chat import ChatSession

app = Flask(__name__)
chat_session = None
sys_msg = "You are a chatbot designed to help people answer questions about the news"


@app.route('/')
def index():
    global chat_session
    chat_session = ChatSession(sys_msg)
    return render_template('index.html')


@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.form['user_message']
    response = chat_session.answer_query(user_message)
    # get the latest citations
    citationDict = chat_session.citations.get(response, {})
    if len(citationDict) == 0:
        citationStr = ""
    else:
        citationStr = "Sources: <br> --- <br>"
        for citeTitle, v in citationDict.items():
            citationStr += f"{citeTitle}: <a href='{v['url']}' target='_blank'>{v['url']}</a> from {v['source']}<br>"
    print("Response: ", response)
    print("Citations: ", citationStr)
    return jsonify({'response': response, 'citations': citationStr})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
    #app.run(debug=True)
