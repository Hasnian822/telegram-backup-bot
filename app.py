from flask import Flask

# Create a Flask app
app = Flask(__name__)

# Flask route for receiving messages from Telegram
@app.route('/')
def webhook():
    return "Web and Bot is active", 200

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)
