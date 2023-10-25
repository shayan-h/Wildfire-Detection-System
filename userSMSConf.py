import requests
import hmac
import hashlib
import time

# Function to send a message and handle user response
def send_message(phone_number, message, api_key):
    resp = requests.post('https://textbelt.com/text', {
        'phone': phone_number,
        'message': message,
        'key': api_key,
        #'replyWebhookUrl' : 'https://jlmkmojeklwbyra7re3z2eqrgy0cwuzn.lambda-url.us-east-2.on.aws/'
    })
    #s3,
    return resp.json()

# Function to verify the request signature
def verify(api_key, timestamp, request_signature, request_payload):
    my_signature = hmac.new(api_key.encode('utf-8'), (timestamp + request_payload).encode('utf-8'), hashlib.sha256).hexdigest()
    return hmac.compare_digest(request_signature, my_signature)

# Define your own mechanism to check for user responses
def custom_response_checker():
    # Implement your logic to retrieve user responses here
    # For example, you can read from a text file

    try:
        with open('SpaceApps.txt', 'r') as file:     # This file locates in the same path as this ipynotebook file.
            # put response in txt
            user_response = file.read().strip()
        return user_response
    except FileNotFoundError:
        return ""

# Function to poll for user responses
def poll_for_response(phone_number, api_key):
    # Check for user responses periodically
    time.sleep(9)  # Adjust the polling interval as needed
    user_response = custom_response_checker()  # Use your mechanism to retrieve user responses
    # Check user response and send an auto-reply with a request for picture confirmation
    auto_reply = 'Thank you for your response! If possible, reply with a picture for confirmation.'
    response = send_message(phone_number, auto_reply, api_key)
    print(response)


# Sample usage
if __name__ == "__main__":
    # Replace with your API key and phone number
    api_key = 'bcaba946523c2ed296c1bf098ad09e2fc2fcb2ac69gj7xq17NPRuNhsM6qkgL3ve' # delete personal info in production mode!!!
    phone_number = '2064668923' # delete personal info in production mode!!!

    # Send the initial message with options
    initial_message = 'We have detected a potential fire in your vicinity based on satellite data. \n\nPlease confirm if you observe any signs of a fire in your area with \'1\' for Yes or \'2\' for No.'
    response = send_message(phone_number, initial_message, api_key)
    print(response)

    # Start polling for user responses using your custom mechanism
    poll_for_response(phone_number, api_key)

# @title Trigger Emergency Alert
Enter_Phone_Number=''  # @param {type:"string"}
response = send_message(phone_number, initial_message, api_key)