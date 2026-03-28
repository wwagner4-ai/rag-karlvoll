import typer
import splitpdf.toimage as _ti
import splitpdf.totext as _tt

app = typer.Typer()


@app.command(help="Converts the pdf pages to jpeg files")
def to_images(clear_out_dir: bool = False):
    _ti.toimage(clear_out_dir)


@app.command(help="Converts the page images (jpeg) to text files")
def to_texts(clear_out_dir: bool = False):
    _tt.to_text(clear_out_dir)


if __name__ == "__main__":
    app()
