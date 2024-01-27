import os  # Import the os module for interacting with the file system
import subprocess  # Import the subprocess module for running shell commands
from flask import Flask, request, jsonify, render_template, make_response, redirect, url_for  # Import necessary Flask components
import time  # Import the time module for working with timestamps
import shutil  # Import the shutil module for file operations
import requests

app = Flask(__name__)  # Create a Flask app instance

@app.route('/')  # Define the home route
def home():
    user_info = {  # Create a dictionary with user information
        'ip': request.remote_addr,  # Get the user's IP address
        'user_agent': request.user_agent.string,  # Get the user's user agent string
        'cookies': request.cookies  # Get the user's cookies
    }
    password = request.cookies.get('password')  # Get the password from the user's cookies
    if password != 'nopassword':  # Check if the password is correct
        return redirect('/password')  # Redirect to the password page if the password is incorrect
    response = make_response(render_template('home.html', user_info=user_info))  # Render the home page with user information
    if 'logout' in request.args:  # Check if the user wants to log out
        response.delete_cookie('shell_id')  # Delete the shell_id cookie
        response.delete_cookie('password')  # Delete the password cookie
    return response  # Return the response

@app.route('/login', methods=['POST'])  # Define the login route
def login():
    password = request.form['password']  # Get the password from the form data
    if password == 'nopassword':  # Check if the password is correct
        response = make_response(redirect('/'))  # Redirect to the home page
        response.set_cookie('password', password)  # Set the password cookie
        return response  # Return the response
    else:
        return redirect('/password')  # Redirect to the password page if the password is incorrect

@app.route('/password')  # Define the password route
def password():
    return render_template('password.html')  # Render the password input page

@app.route('/shell')  # Define the shell route
def shell():
    password = request.cookies.get('password')  # Get the password from the user's cookies
    if password != 'nopassword':  # Check if the password is correct
        return redirect('/password')  # Redirect to the password page if the password is incorrect
    return render_template('shell.html')  # Render the shell interface page

@app.route('/shell/execute')  # Define the execute route
def execute():
    command = request.args.get('command', '')  # Get the command from the request arguments
    shell_id = request.cookies.get('shell_id', '')  # Get the shell_id from the user's cookies

    if not shell_id:  # Check if the shell_id is not set
        shell_id = str(os.urandom(16).hex())  # Generate a new shell_id

    shell_dir = f'sessions/{shell_id}'  # Create the shell directory path
    os.makedirs(shell_dir, exist_ok=True)  # Create the shell directory if it doesn't exist

    # Check if the user's session has expired
    last_active = request.cookies.get('last_active', '')
    if last_active and time.time() - float(last_active) > 3600:
        shutil.rmtree(shell_dir)  # Remove the expired session directory
        shell_id = str(os.urandom(16).hex())  # Generate a new shell_id
        shell_dir = f'sessions/{shell_id}'  # Create the new shell directory path
        os.makedirs(shell_dir, exist_ok=True)  # Create the new shell directory

    # Get the current working directory for the user
    cwd = request.cookies.get('cwd', shell_dir)

    # Parse the command and check if it's a 'cd' command
    parts = command.split()
    if len(parts) > 0 and parts[0] == 'cd':
        if len(parts) > 1:
            # Change the current working directory for the user
            cwd = os.path.join(cwd, parts[1])
        else:
            # Change the current working directory to the user's home directory
            cwd = shell_dir

    try:
        # Execute the command in the current working directory
        output = subprocess.check_output(command, shell=True, cwd=cwd)
        output = output.decode('utf-8')  # Decode the output
    except subprocess.CalledProcessError as e:
        output = f"Command '{command}' failed with return code {e.returncode}"  # Handle command errors

    response = make_response(jsonify({'output': output}))  # Create a JSON response with the command output
    response.set_cookie('shell_id', shell_id)  # Set the shell_id cookie
    response.set_cookie('last_active', str(time.time()))  # Set the last_active cookie
    response.set_cookie('cwd', cwd)  # Set the cwd cookie
    return response  # Return the response

@app.route('/camphish')  # Define the camphish route
def camphish():
    res = requests.get("https://www.google.com")
    return f'Camphish page coming soon...\n\n{res}'  # Return a placeholder message
