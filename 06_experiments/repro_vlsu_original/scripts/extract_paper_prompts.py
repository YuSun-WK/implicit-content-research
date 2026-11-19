"""Extract the three classification prompts from the pinned ICLR proceedings PDF."""

import argparse
from hashlib import sha256
from io import BytesIO
from pathlib import Path

from pypdf import PdfReader

PDF_SHA256 = "b38dc2e84d20899132125338b3ef8d31f54873660c2562c281c4d992c1f96aa8"
PROMPTS = {
    "binary.v1.txt": (33, "Prompt for Binary Classification", "Prompt for Three-class Classification Classification"),
    "direct.v1.txt": (33, "Prompt for Three-class Classification Classification", "D.2 MODELRESPONSEEVALUATIONPROMPTS"),
    "structured_cot.v1.txt": (35, "Structured Reasoning", "D.4 EVALUATIONMODELSETTINGS"),
}


def extract(raw):
    if sha256(raw).hexdigest() != PDF_SHA256:
        raise ValueError("PDF SHA-256 differs from the pinned proceedings edition")
    pdf = PdfReader(BytesIO(raw))
    for filename, (page, start, end) in PROMPTS.items():
        text = pdf.pages[page - 1].extract_text()
        prompt = text.split(start + "\n", 1)[1].split("\n" + end, 1)[0]
        yield filename, (prompt.strip() + "\n").encode("utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", required=True, type=Path)
    parser.add_argument("--out", default=Path(".local/prompts"), type=Path)
    args = parser.parse_args()
    prompts = dict(extract(args.pdf.read_bytes()))
    args.out.mkdir(parents=True, exist_ok=True)
    for filename, prompt in prompts.items():
        (args.out / filename).write_bytes(prompt)
        print(f"{sha256(prompt).hexdigest()}  {filename}")


if __name__ == "__main__":
    main()
