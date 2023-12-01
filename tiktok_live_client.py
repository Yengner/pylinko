import socket
import time
import requests
import json

class TikTokLiveClient:
    def __init__(self, stream_id):
        self.stream_id = stream_id

        # Replace these with your actual credentials
        client_key = "awjxnv5r9mymezc8"
        client_secret = "dDt0o0d8gLdAzvIBerKSANi1rhKS2Syr"

    def _connect_and_receive(self):
        # Generate stream token
        url = "https://open-api.tiktok.com/r/live/v1/stream/" + self.stream_id + "/token/"
        headers = {
            "Authorization": "Bearer " + self._generate_access_token(),
        }
        response = requests.post(url, headers=headers)
        stream_token_response = json.loads(response.text)
        stream_token = stream_token_response["data"]["stream_token"]

        # Connect to the TikTok Live stream using a socket
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect(("live.tiktok.com", 80))

                # Send the request headers
                request_headers = {
                    "Host": "live.tiktok.com",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",

                    
"Accept": "*/*",
                    "Authorization": "Bearer " + stream_token,
                }

                request = f"GET /r/live/v1/stream/{self.stream_id}/chunk?sdk_version=3.6.1&device_id=1234567890&channel_id={self.stream_id}&is_first_chunk=true HTTP/1.1\r\n"
                for header_key, header_value in request_headers.items():
                    request += f"{header_key}: {header_value}\r\n"
                request += "\r\n"

                sock.sendall(request.encode('utf-8'))

                # Receive the response from the TikTok Live stream
                response = sock.recv(1024)

                return response

        except Exception as e:
            raise RuntimeError(f"Error connecting to TikTok Live: {e}")

    def _generate_access_token(self):
        # Replace these with your actual credentials
        client_key = "YOUR_CLIENT_KEY"
        client_secret = "YOUR_CLIENT_SECRET"

        # Generate access token
        url = "https://open-api.tiktok.com/oauth2/token/"
        data = {
            "grant_type": "client_credentials",
            "client_key": client_key,
            "client_secret": client_secret,
        }
        response = requests.post(url, data=data)
        access_token_response = json.loads(response.text)
        access_token = access_token_response["access_token"]

        return access_token

    def recv(self):
        # Set the retry counter and maximum retries
        retry_count = 0
        max_retries = 3

        while retry_count < max_retries:
            try:
                # Attempt to connect to the TikTok Live stream
                response = self._connect_and_receive()

                # Check if the response indicates a successful connection
                if response.startswith(b'HTTP/1.1 200 OK'):
                    # Extract the raw data from the response
                    received_data = response.split(b'\r\n\r\n')[1]

                    # Data successfully retrieved, return True
                    return True

                else:
                    # Connection error or invalid response
                    raise RuntimeError("Connection error or invalid response")

            except Exception as e:
                # Connection error, retry or break
                print(f"Error connecting to TikTok Live: {e}")
                retry_count += 1

                if retry_count == max_retries:
                    # Maximum retries reached, break the loop
                    break

                # Wait for a delay before retrying
                time.sleep(2)

        # Failed to connect after all retries
        return False
stream_id = "@yengner.png"
tiktok_client = TikTokLiveClient(stream_id)

connected = tiktok_client.recv()

if connected:
    print("Connected to TikTok Live and retrieving data")
else:
    print("Failed to connect to TikTok Live or not retrieving data")
