from flask import Flask, render_template, request
import requests
import re

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    gseid = request.form["gseid"].strip().upper()

    url = f"https://ftp.ncbi.nlm.nih.gov/geo/series/{gseid[:-3]}nnn/{gseid}/suppl/"
    response = requests.get(url)

    if response.status_code != 200:
        return render_template("index.html", error="Dataset not found")

    text = response.text.lower()

    files = re.findall(r'href="([^"]+)"', response.text)

    counts_file = None
    meta_file = None
    raw_file = None

    for file in files:
        low = file.lower()

        if any(word in low for word in ["count", "counts", "matrix", "expression"]) and not counts_file:
            counts_file = url + file

        if any(word in low for word in ["meta", "metadata", "clinical", "sample"]) and not meta_file:
            meta_file = url + file

        if any(word in low for word in ["raw", ".tar", ".gz", ".fastq"]) and not raw_file:
            raw_file = url + file

    return render_template(
        "index.html",
        gseid=gseid,
        counts=counts_file,
        meta=meta_file,
        raw=raw_file,
        url=url
    )

if __name__ == "__main__":
    app.run(debug=True)