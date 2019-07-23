# marlo_app

Development Environment Setup

Go to the dir where you have the downloaded folder.

You must be running Python 3 to develop on this project. Run python --version and ensure that the print out is 3.x.x (usually it will be 3.6.x). If you see version 2, then try to repeat the command above with python3 --version. If this second approach worked for you then please read the whole of the next paragraph before creating your virtual environment.

Activate the virtual environment with the following code in Command Prompt (Flask does not work in Powershell) in the top level of the repo: venv\Scripts\activate. You should see (venv) appear at the beginning of the next line in your Command Prompt.

To deactivate later, run deactivate. The (venv) should dissapear.

Run the command set FLASK_APP=app.py to set the FLASK_APP environment variable.

Run the command set FLASK_DEBUG=1 during development to make sure your flask application reloads when you make changes.

Run flask run to run the webserver and visit localhost:5000 to see it in action. Now you can get to work.
