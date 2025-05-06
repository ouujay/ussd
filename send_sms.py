import africastalking

# TODO: Initialize the SDK
username = 'sandbox'  # Must be 'sandbox' for test environment
api_key = 'atsk_40303b14f9e27e8c0f08d18ea3b8327cdf8cb7f1f8c036d198ac38ee5aea7e27b0e6a746'  # Your sandbox API key
africastalking.initialize(username, api_key)

class send_sms:
    def __init__(self):
        self.sms = africastalking.SMS

    # TODO: Send Message
    def sending(self):
        # Set the numbers in international format
        recipients = ["+2349013413496"]  # Replace with your number added in simulator
        # Set your message
        message = "Hey AT Ninja!"
        # Set your shortCode or senderId
        sender = "AFRICASTKNG"  # Required sender for sandbox

        try:
            response = self.sms.send(message, recipients, sender)
            print(response)
        except Exception as e:
            print(f"Houston, we have a problem: {e}")
