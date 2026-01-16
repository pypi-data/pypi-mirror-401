class Client:
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def say_api(self) -> str:
        return f"API Key is: {self.api_key}"
