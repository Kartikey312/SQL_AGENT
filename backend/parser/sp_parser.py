import re
from typing import List


def extract_procedures(sql_text: str) -> List[dict]:
    pattern = re.compile(
        r"CREATE\s+(?:OR\s+ALTER\s+)?PROCEDURE\s+([\w\.]+)\s*(\([^)]*\))?\s+AS\s+(BEGIN.*?END)",
        re.IGNORECASE | re.DOTALL,
    )

    procedures = []
    for match in pattern.finditer(sql_text):
        procedures.append(
            {
                "procedure_name": match.group(1),
                "signature": (match.group(2) or "").strip(),
                "body": match.group(3).strip(),
            }
        )

    return procedures
