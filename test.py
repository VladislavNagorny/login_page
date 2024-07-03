from flask import Flask, render_template, jsonify, request, redirect, url_for
import re

app = Flask(__name__)

# Simple imitation of a user database
users = {
    'existing_user': 'Qwerty1!'
}


def validate_password(password):
    """Function to validate password"""
    errors = []

    if len(password) < 8 or len(password) > 30:
        errors.append("Password must be between 8 and 30 characters long.")

    if not re.search(r'[A-Z]', password):
        errors.append("Password must contain at least one uppercase letter.")

    if not re.search(r'[a-z]', password):
        errors.append("Password must contain at least one lowercase letter.")

    if not re.search(r'[0-9]', password):
        errors.append("Password must contain at least one digit.")

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append("Password must contain at least one special character.")

    return errors


@app.route('/')
def home():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register():
    errors = []
    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    # Check if username already exists in the database
    if username in users:
        errors.append("Username already exists! Please choose another username.")

    # Check username length
    if len(username) < 6 or len(username) > 20:
        errors.append("Username must be between 6 and 20 characters long.")

    # Validate password
    password_errors = validate_password(password)
    errors.extend(password_errors)

    # Check if passwords match
    if password != confirm_password:
        errors.append("Passwords do not match. Please try again.")

    if not errors:
        # Add new user to the database (dummy example here)
        users[username] = password
        return redirect(url_for('view_users'))

    return render_template('register.html', errors=errors)


@app.route('/users')
def view_users():
    return render_template('users.html', users=users)


@app.route('/api/register', methods=['POST'])
def api_register():
    errors = []
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')
    confirm_password = data.get('confirm_password')

    # Check if username already exists in the database
    if username in users:
        errors.append("Username already exists! Please choose another username.")

    # Check username length
    if len(username) < 6 or len(username) > 20:
        errors.append("Username must be between 6 and 20 characters long.")

    # Validate password
    password_errors = validate_password(password)
    errors.extend(password_errors)

    # Check if passwords match
    if password != confirm_password:
        errors.append("Passwords do not match. Please try again.")

    if not errors:
        # Add new user to the database (dummy example here)
        users[username] = password
        return jsonify({'message': 'User registered successfully'})

    return jsonify({'errors': errors}), 400


@app.route('/api/users', methods=['GET'])
def api_view_users():
    return jsonify({'users': list(users.keys())})


if __name__ == '__main__':
    app.run(debug=True)