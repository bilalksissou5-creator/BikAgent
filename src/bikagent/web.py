from flask import Flask, request, jsonify, render_template
from .agent import BikAgent

app = Flask(__name__)
agent = BikAgent()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    prompt = data.get('prompt', '')
    response = agent.run(prompt)
    return jsonify({'response': response})

if __name__ == '__main__':
    print("✅ تم تشغيل الخادم! افتح متصفح هاتفك واذهب إلى: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
