import requests
import hmac
import hashlib
import time
import struct
import base64

# Your details
your_account = "priyambajpai22"
gist_id = "ea44aea9685ab2836dafdb3e4593fc50"
email = "bajpaipriyam865@gmail.com"
solution_language = "python"

# Calculate the TOTP
Time_Step_X = 30
T0 = 0
shared_secret = f"{email}HENNGECHALLENGE003"

current_time = int(time.time()) - T0
time_counter = current_time // Time_Step_X
time_counter_bytes = struct.pack(">Q", time_counter)
hmac_hash = hmac.new(shared_secret.encode(), time_counter_bytes, hashlib.sha512).digest()
offset = hmac_hash[-1] & 0x0F
otp = struct.unpack(">I", hmac_hash[offset:offset + 4])[0] & 0x7FFFFFFF
otp = otp % 10000000000  # 10-digit TOTP

# Create the JSON payload
json_payload = {
    "github_url": f"https://gist.github.com/{your_account}/{gist_id}",
    "contact_email": email,
    "solution_language": solution_language
}

# Make the HTTP POST request with Basic Authentication
url = "https://api.challenge.hennge.com/challenges/003"
auth_string = f"{email}:{otp}".encode()
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Basic {base64.b64encode(auth_string).decode()}"
}

response = requests.post(url, json=json_payload, headers=headers)

# Print the response
print(response.status_code)
print(response.json())
