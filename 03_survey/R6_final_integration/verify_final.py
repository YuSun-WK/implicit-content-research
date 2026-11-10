"""Parse and validate the R6 final manuscript, bibliography, tables and figures."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from lxml import etree

BASE = Path(__file__).resolve().parents[1] / "R5_full_draft"
OUT = Path(__file__).resolve().parent


class BibParser:
    def __init__(self, source: str):
        self.s, self.i = source, 0

    def skip(self):
        while self.i < len(self.s):
            if self.s[self.i].isspace():
                self.i += 1
            elif self.s[self.i] == "%":
                self.i = self.s.find("\n", self.i)
                if self.i < 0:
                    self.i = len(self.s)
            else:
                break

    def token(self):
        m = re.match(r"[A-Za-z][\w:-]*", self.s[self.i:])
        assert m, f"Expected token at offset {self.i}"
        self.i += len(m.group())
        return m.group()

    def value(self):
        self.skip()
        if self.s[self.i] in '{"':
            opener = self.s[self.i]
            closer = "}" if opener == "{" else '"'
            self.i += 1
            depth, chars = 1, []
            while self.i < len(self.s) and depth:
                c = self.s[self.i]
                if c == "\\" and self.i + 1 < len(self.s):
                    chars.extend((c, self.s[self.i + 1]))
                    self.i += 2
                    continue
                if c == opener and opener == "{":
                    depth += 1
                elif c == closer:
                    depth -= 1
                    if depth == 0:
                        self.i += 1
                        break
                chars.append(c)
                self.i += 1
            assert depth == 0, "Unclosed BibTeX value"
            return "".join(chars)
        m = re.match(r"[^,}\s#]+", self.s[self.i:])
        assert m, f"Expected value at offset {self.i}"
        self.i += len(m.group())
        return m.group()

    def parse(self):
        entries = {}
        self.skip()
        while self.i < len(self.s):
            assert self.s[self.i] == "@", f"Expected entry at offset {self.i}"
            self.i += 1
            kind = self.token().lower()
            self.skip()
            assert self.s[self.i] == "{"
            self.i += 1
            self.skip()
            start = self.i
            while self.s[self.i] not in ",}":
                self.i += 1
            key = self.s[start:self.i].strip()
            assert key and key not in entries, f"Duplicate/missing key: {key}"
            assert self.s[self.i] == ","
            self.i += 1
            fields = {}
            while True:
                self.skip()
                if self.s[self.i] == "}":
                    self.i += 1
                    break
                name = self.token().lower()
                assert name not in fields, f"Duplicate field {key}.{name}"
                self.skip()
                assert self.s[self.i] == "=", f"Missing '=' at {key}.{name}"
                self.i += 1
                parts = [self.value()]
                self.skip()
                while self.s[self.i] == "#":
                    self.i += 1
                    parts.append(self.value())
                    self.skip()
                fields[name] = "".join(parts)
                assert fields[name], f"Empty {key}.{name}"
                if self.s[self.i] == ",":
                    self.i += 1
                else:
                    assert self.s[self.i] == "}", f"Expected comma at {key}.{name}"
            assert {"author", "title", "year"} <= fields.keys(), f"Missing required metadata: {key}"
            assert "doi" in fields or "url" in fields or kind in {"book", "incollection"}, f"No source locator: {key}"
            entries[key] = {"type": kind, "fields": fields}
            self.skip()
        return entries


def citekeys(s: str):
    return set(re.findall(r"(?<![\w])@([A-Za-z][\w-]+)", s))


def main():
    draft = (BASE / "Survey_Full_Draft.md").read_text(encoding="utf-8")
    bib = BibParser((BASE / "references.bib").read_text(encoding="utf-8")).parse()
    body, refs = draft.split("# 参考文献\n", 1)
    science = body.split('<a id="appendix-a">', 1)[0]
    keys = set(bib)
    assert len(keys) == 50
    assert citekeys(science) == citekeys(body) == keys, "In-text/Bib mismatch"
    manual = re.findall(r"^\d+\. \*\*([^*]+)\*\*", refs, re.M)
    assert len(manual) == 50 and set(manual) == keys and len(set(manual)) == 50
    numbers = [int(n) for n in re.findall(r"^(\d+)\. \*\*", refs, re.M)]
    assert numbers == list(range(1, 51)), "Manual reference numbering"
    inventory = body.split("# 附录B ", 1)[1]
    inventory_keys = re.findall(r"@([\w-]+)", inventory)
    assert len(inventory_keys) == len(set(inventory_keys)) == 50
    assert set(inventory_keys) == keys
    mapping = (BASE / "Citation_Key_Mapping.md").read_text(encoding="utf-8")
    assert all(f"`{key}`" in mapping for key in keys)
    assert re.findall(r"^# ([1-9]) ", draft, re.M) == list("123456789")
    assert "arxiv.org/html/2506.09301" not in draft
    assert "Table G4" in draft and "Table G4" in (BASE / "tables/T7_Method_Families.md").read_text(encoding="utf-8")
    assert "10.1016/j.inffus.2024.102712" in bib["mao2025pragmatic"]["fields"]["doi"]

    table_results = []
    for p in sorted((BASE / "tables").glob("T*.md")):
        s = p.read_text(encoding="utf-8")
        rows = [line for line in s.splitlines() if line.startswith("|")]
        assert rows and len({line.count("|") for line in rows}) == 1, p
        assert citekeys(s) <= keys, f"Unknown table citekey: {p}"
        table_results.append({"name": p.name, "rows": len(rows)})
    assert len(table_results) == 7
    for target in re.findall(r"!??\[[^\]]*\]\(([^)]+)\)", draft):
        if target.startswith(("https://", "http://", "#")):
            continue
        assert (BASE / target).exists(), f"Broken relative link: {target}"

    expected_figures = {
        "F1.svg": "e13da1664b240ff40e8ec03a949b153fc0a72e52",
        "F2.svg": "98b8a906720cdaecf9460c50cad77e8a7ba744db",
        "F3.svg": "2540e055df498cedb71e2fd176467a1480815441",
        "F4.svg": "7053da691e69b978fa684017a4fb8a5a18e755b0",
        "F5.svg": "7b74ff928d86a3d4ddf28c797b2468e03f453039",
    }
    figures = []
    for name, expected in expected_figures.items():
        p = BASE / "figures" / name
        data = p.read_bytes()
        sha = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        assert sha == expected, f"PR #60 figure changed: {name}"
        svg = etree.fromstring(data)
        assert svg.tag == "{http://www.w3.org/2000/svg}svg"
        assert svg.get("viewBox") or (svg.get("width") and svg.get("height"))
        figures.append({"name": name, "git_blob": sha})
    result = {
        "status": "PASS",
        "bibtex_parsed_entries": len(bib),
        "body_unique_citekeys": len(citekeys(science)),
        "manual_references": len(manual),
        "appendix_b_unique_keys": len(set(inventory_keys)),
        "chapters": 9,
        "tables": table_results,
        "figures": figures,
        "source_main": "49214314d544f865e046aae0a0fe165f08e542f5",
        "source_pr63": "80bad7e668a5510f7897b8ee117d7851ebaa8114",
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "validation.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
