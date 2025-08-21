import re
from typing import Dict, List, Any


class TextProfileParser:
    """Parse unstructured candidate text into a coarse JSON structure.

    Handles sections: education, achievements, projects, experience (work & internships), certificates.
    """

    def __init__(self) -> None:
        self.section_headers = {
            "education": ["education"],
            "achievements": ["achievements", "achievement"],
            "projects": ["projects", "project"],
            "experience": ["work experience", "internships", "experience", "internship"],
            "certificates": ["certificate", "certificates", "certifications"],
        }
        self.line_splitter = re.compile(r"\r?\n+")

    def parse(self, text: str) -> Dict[str, Any]:
        if not text:
            return {}
        lines = [ln.strip() for ln in self.line_splitter.split(text) if ln.strip()]

        data: Dict[str, Any] = {
            "education": [],
            "achievements": [],
            "projects": [],
            "experience": [],
            "certificates": [],
            "raw": text.strip(),
        }

        def is_header(ln: str) -> str:
            lower = ln.lower().strip("* :-")
            for key, aliases in self.section_headers.items():
                for a in aliases:
                    if lower.startswith(a):
                        return key
            return ""

        current = None
        buffer: List[str] = []

        def flush():
            nonlocal buffer, current
            if current and buffer:
                chunk = " ".join(buffer).strip()
                if current == "education":
                    data["education"].extend(self._split_items(chunk))
                elif current == "achievements":
                    data["achievements"].extend(self._split_items(chunk))
                elif current == "projects":
                    data["projects"].extend(self._split_items(chunk))
                elif current == "experience":
                    data["experience"].extend(self._split_items(chunk))
                elif current == "certificates":
                    data["certificates"].extend(self._split_items(chunk))
            buffer = []

        for ln in lines:
            header = is_header(ln)
            if header:
                flush()
                current = header
                continue
            buffer.append(ln)
        flush()

        return data

    def _split_items(self, chunk: str) -> List[str]:
        # Split on common separators while keeping phrases together
        parts = re.split(r"\s{2,}|\s*\-\s+|\s*\*\s+|\s*\n\s*", chunk)
        items = [p.strip(" .-") for p in parts if p and len(p.strip()) > 2]
        # De-duplicate while preserving order
        seen = set()
        out: List[str] = []
        for it in items:
            key = it.lower()
            if key not in seen:
                seen.add(key)
                out.append(it)
        return out


