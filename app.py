from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Sudoku Solver!"

@app.route('/solve', methods=['POST'])
def solve_sudoku():
    data = request.get_json()
    # Assume there is a function `solve` that takes a Sudoku puzzle and returns the solution
    solution = solve(data['puzzle'])
    return jsonify({'solution': solution})

@app.route('/static/<path:path>')
def send_static(path):
    return app.send_static_file(path)

if __name__ == '__main__':
    app.run(debug=True)