import requests
import json
import splitpdf.helper as hlp_


def to_text(clear_out_dir: bool):

    pages_dir = hlp_.pages_dir()
    texts_dir = hlp_.texts_dir()
    texts_dir.mkdir(exist_ok=True, parents=True)
    if clear_out_dir:
        hlp_.clear_dir(texts_dir)
    assert not hlp_.is_empty_dir(texts_dir), f"{texts_dir} must be empty"

    # Url where tika (full) is running
    # 'docker run -d -p 127.0.0.1:9998:9998 apache/tika:latest-full'
    url = "http://localhost:9998/rmeta/text"
    headers = {"Accept": "application/json", "X-Tika-OCRLanguage": "deu"}

    helper_page_nr = 1000
    for image in list(pages_dir.iterdir()):
        if image.suffix == ".jpg":
            try:
                with image.open("rb") as f:
                    response = requests.put(url, data=f, headers=headers)
                response.raise_for_status()  # Raises an error for 4xx/5xx responses
                response_obj = response.json()[0]
                text0 = response_obj["X-TIKA:content"]
                text = text0.replace("-\n", "")
                text = text.replace("\n", " ")
                text = text.strip()
                # print(text0)
                # print(140*"-")
                # print(text)
                # print(70*"- ")
                extracted_page_nr = extract_page_number(text)
                match extracted_page_nr:
                    case str(errer_message):
                        print("WARNING:", errer_message)
                        page_nr = helper_page_nr
                        helper_page_nr += 1
                    case int(page_nr_):
                        page_nr = page_nr_
                obj = {"page_number": f"{page_nr}", "text": text}
                file_name = f"document-{page_nr:04d}.txt"
                file_path = texts_dir / file_name
                with file_path.open("w", encoding="utf-8") as f:
                    json.dump(obj, f, indent=2, ensure_ascii=False)
                print(f"Wrote document {page_nr} {file_path}")

            except FileNotFoundError:
                print(f"Error: The file '{image}' was not found.")
            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")


def extract_page_number(text: str) -> int | str:
    def parse_int(tail_text: str) -> int | None:
        try:
            return int(tail_text)
        except ValueError as _:
            return None

    index = text.rfind(" ")
    tail_text = text[index:]
    page_nr = parse_int(tail_text)
    if page_nr is None:
        tail_doc_text = text[-100:]
        return (
            f"Cannot extract page number from document ending with '...{tail_doc_text}'"
        )
    return page_nr
