import json
import boto3
from flask import Flask, render_template, request

app = Flask(__name__)

sqs = boto3.client('sqs')
HIGH_PRIORITY_QUEUE_URL = 'https://sqs.eu-west-2.amazonaws.com/423598777794/high-priority-queue'
MEDIUM_PRIORITY_QUEUE_URL = 'https://sqs.eu-west-2.amazonaws.com/423598777794/medium-priority-queue'
LOW_PRIORITY_QUEUE_URL = 'https://sqs.eu-west-2.amazonaws.com/423598777794/low-priority-queue'
DLQ_URL = 'https://sqs.eu-west-2.amazonaws.com/423598777794/dead-letter-queue'

# define a function to handle requests based on their priority
def handle_priority(priority, additional_info):
    if priority == 'high':
        # if the priority is high, send a message to the high priority queue
        sqs.send_message(QueueUrl=HIGH_PRIORITY_QUEUE_URL, MessageBody=json.dumps({"priority": priority, "additional_info": additional_info}))

    elif priority == 'medium':
        # if the priority is medium, send a message to the medium priority queue
        sqs.send_message(QueueUrl=MEDIUM_PRIORITY_QUEUE_URL, MessageBody=json.dumps({"priority": priority, "additional_info": additional_info}))

    elif priority == 'low':
        # if the priority is low, send a message to the low priority queue
        sqs.send_message(QueueUrl=LOW_PRIORITY_QUEUE_URL, MessageBody=json.dumps({"priority": priority, "additional_info": additional_info}))

    else:
        # if the priority level is not recognised, send a message to the dead-letter queue
        sqs.send_message(QueueUrl=DLQ_URL, MessageBody=json.dumps({"priority": priority, "additional_info": additional_info}))

# create a route to serve the request form
@app.route('/')
def serve_request_form():
    return render_template('request_form.html')

# create a route to receive requests and process them
@app.route('/request', methods=['POST'])
def handle_request():
    # get the priority and additional_info from the request form
    priority = request.form.get('priority', 'low')
    additional_info = request.form.get('additional_info', '')

    if not additional_info:
        # if the additional_info field is empty, return an error message to the client
        return 'Error: additional information is required'

    # call the handle_priority function to handle the request based on its priority
    handle_priority(priority, additional_info)

    if priority in ('high', 'medium', 'low'):
        # if the priority is recognised, return a success message to the client
        return 'Request processed successfully'
    else:
        # if the priority level is not recognised, return an error message to the client
        return 'Error: priority level not recognized'

if __name__ == '__main__':
    app.run(debug=True)