import africastalking

# TODO: Initialize the SDK
username = 'sandbox'  # must be 'sandbox' for testing
api_key = 'atsk_40303b14f9e27e8c0f08d18ea3b8327cdf8cb7f1f8c036d198ac38ee5aea7e27b0e6a746'  # go to https://account.africastalking.com/apps/sandbox/settings to get it
africastalking.initialize(username, api_key)

class SendSMS:
    def __init__(self):
        self.sms = africastalking.SMS

    # TODO: Send Message
    def sending(self):
        recipients = ["+2349013413496"]  # Replace with your own phone number in international format
        message = "Hey AT Ninja!"
        sender = "XXYYZZ"  # For sandbox, use 'AFRICASTKNG' as the default sender ID

        try:
            response = self.sms.send(message, recipients, sender)
            print("Message sent successfully:", response)
        except Exception as e:
            print(f"Houston, we have a problem: {e}")

# TODO: Call SMS method
if __name__ == "__main__":
    SendSMS().sending()
