from together import Together


class Llm:
    _client: Together | None = None
    _key: str | None = None

    def __init__(self, key: str):
        self._key = key

    def close(self) -> None:
        if self._client:
            self._client.close()

    def query(self, prompt: str) -> list[str]:
        response = self._get_client().chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        return [choise.message.content for choise in response.choices]

    def _get_client(self) -> Together:
        if self._client is None:
            print("#### using key:", self._key)
            self._client = Together(api_key=self._key)

        return self._client
