import json
from flask import Flask, render_template, request

app = Flask(__name__)

# define a function to handle requests based on their priority
def handle_priority(priority, additional_info):
    if priority == 'high':
        # if the priority is high, send a slack message to notify someone
        with open('high_priority.json', 'a') as file:
            data = {"priority": priority, "additional_info": additional_info}
            json.dump(data, file)
            file.write('\n')

    elif priority == 'medium':
        # if the priority is medium, log the request to trello
        with open('medium_priority.json', 'a') as file:
            data = {"priority": priority, "additional_info": additional_info}
            json.dump(data, file)
            file.write('\n')

    elif priority == 'low':
        with open('low_priority.json', 'a') as file:
            data = {"priority": priority, "additional_info": additional_info}
            json.dump(data, file)
            file.write('\n')

# create a route to serve the request form
@app.route('/')
def serve_request_form():
    return render_template('request_form.html')

# create a route to receive requests and process them
@app.route('/request', methods=['POST'])
def handle_request():
    # get the priority and additional_info from the request form
    priority = request.form['priority']
    additional_info = request.form['additional_info']

    # call the handle_priority function to handle the request based on its priority
    handle_priority(priority, additional_info)

    # return a response to the client
    return 'Request processed successfully'

if __name__ == '__main__':
    app.run(debug=True)
