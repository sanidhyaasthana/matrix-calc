from flask import Flask, request, jsonify, render_template
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    # Render the HTML form for user input
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    # Get the input from the form
    rows = int(request.form['rows'])
    cols = int(request.form['columns'])
    
    # Build the matrix from the inputs
    matrix = []
    for i in range(rows):
        row = request.form.getlist(f'row_{i}')
        matrix.append(list(map(int, row)))
    
    matrix = np.array(matrix)
    result = {}

    # Process the matrix
    result['Matrix'] = matrix.tolist()
    result['Rank'] = np.linalg.matrix_rank(matrix)
    
    if rows == cols:
        det = round(np.linalg.det(matrix), 2)
        result['Determinant'] = det

        e, v = np.linalg.eig(matrix)
        result['Eigenvalues'] = e.tolist()
        result['Eigenvectors'] = v.tolist()

        if det == 0:
            result['Inverse'] = "The matrix is singular and does not have an inverse."
        else:
            result['Inverse'] = np.linalg.inv(matrix).tolist()
    else:
        result['Message'] = "Determinant, Eigenvalues, and Inverse are not defined for non-square matrices."
    
    result['Trace'] = np.trace(matrix)
    q, r = np.linalg.qr(matrix)
    result['Q'] = q.tolist()
    result['R'] = r.tolist()

    # Return the results as JSON
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
