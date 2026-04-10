import typer
import splitpdf.toimage as ti_
import splitpdf.totext as tt_
import splitpdf.webapp as wa_
import splitpdf.embed as eb_
import splitpdf.tryout as tryout_

app = typer.Typer()


@app.command(help="Converts the pdf pages to jpeg files")
def to_images(clear_out_dir: bool = False):
    ti_.toimage(clear_out_dir)


@app.command(help="Converts the page images (jpeg) to text files")
def to_texts(clear_out_dir: bool = False):
    tt_.to_text(clear_out_dir)


@app.command(help="Starts the backend")
def start_webapp(port: int = 8000):
    wa_.start(port)


@app.command(help="Embed pages to vector database")
def embed(clear_db: bool = False):
    eb_.embed_pages(clear_db)


@app.command(help="Query the vector database for matching documents")
def query(prompt: str):
    eb_.query(prompt)


@app.command(help="Tryout something")
def tryout():
    tryout_.run()


if __name__ == "__main__":
    app()
