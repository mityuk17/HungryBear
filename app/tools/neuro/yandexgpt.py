from config import settings
import aiohttp




class YandexGPT_API:
    def __init__(self, token: str, catalog_id: str, model: str):
        self.API_TOKEN = token
        self.modelUri = f"gpt://{catalog_id}/{model}/latest"
        self.stream = False
        self.temperature = 0.6
        self.maxTokens = 2_000
        self.auth_header = {"Authorization": f"APi-Key {token}"}
        
    
    async def text_completion(self, messages: list) -> str:
        url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        body = {
            "modelUri": self.modelUri,
            "completionOptions": {
                "stream": self.stream,
                "temperature": self.temperature,
                "maxTokens": self.maxTokens
            },
            "messages": messages
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, json=body, headers=self.auth_header) as response:
                response = await response.json()
                
                answer = response["result"]["alternatives"][0]["message"]["text"]

                return answer
            
                
YandexGPT = YandexGPT_API(token=settings.YANDEX_API_TOKEN, catalog_id=settings.YANDEX_CATALOG_ID, model=settings.YANDEX_GPT_MODEL)

    