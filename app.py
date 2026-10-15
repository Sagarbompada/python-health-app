from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Python Project</title>
    </head>
    <body>
        <h1>Welcome to the Project</h1>
        <p>Your Python application is running successfully.</p>
        <p><a href="/health">Check application health</a></p>
    </body>
    </html>
    """


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "application": "python-health-app"
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
