from together import Together


class Llm:
    _client: Together | None = None
    _key: str | None = None

    def __init__(self, key: str):
        self._key = key

    def close(self) -> None:
        if self._client:
            self._client.close()

    def system_prompt(self) -> str | None:
        return "Ausgabe als Text ohne Formatierung"

    def query(self, prompt: str) -> list[str]:
        sp = self.system_prompt()
        if sp:
            content = f"""
                {prompt}.\n{sp}
            """.strip()
        else:
            content = prompt

        response = self._get_client().chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
            messages=[{"role": "user", "content": content}],
        )
        return [choise.message.content for choise in response.choices]

    def _get_client(self) -> Together:
        if self._client is None:
            self._client = Together(api_key=self._key)

        return self._client
