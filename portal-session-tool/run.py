import json
import os
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "input" / "transcript.txt"
PROMPTS = ROOT / "prompts"
OUTPUT = ROOT / "output"
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


FILES = {
    "extraction": OUTPUT / "extraction.json",
    "agency": OUTPUT / "agency_brief.md",
    "researcher": OUTPUT / "researcher_brief.md",
    "student": OUTPUT / "student_brief.md",
    "questions": OUTPUT / "clarifying_questions.md",
    "evaluation": OUTPUT / "evaluation_notes.md",
}


BRIEFS = [
    ("agency", "02_agency_brief.txt", "Agency Project Snapshot"),
    ("researcher", "03_researcher_brief.txt", "Researcher Brief"),
    ("student", "04_student_brief.txt", "UNC/SDSS Student Action Brief"),
    ("questions", "05_questions.txt", "Clarifying Questions"),
]


def read(path):
    return path.read_text(encoding="utf-8").strip()


def response_text(data):
    parts = []
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                parts.append(content.get("text", ""))
    return "\n".join(parts).strip()


def ask_model(prompt, transcript, json_mode=False):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    body = {
        "model": MODEL,
        "input": [
            {
                "role": "system",
                "content": (
                    "Turn Project Portal session text into structured notes. "
                    "Do not invent details. Use 'not specified' or "
                    "'unclear from transcript' when needed."
                ),
            },
            {"role": "user", "content": f"{prompt}\n\nTRANSCRIPT:\n{transcript}"},
        ],
    }
    if json_mode:
        body["text"] = {"format": {"type": "json_object"}}

    req = urllib.request.Request(
        "https://api.openai.com/v1/responses",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as res:
            return response_text(json.loads(res.read().decode("utf-8")))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenAI API error: {exc.code} {detail}") from exc


def placeholder_extraction():
    return {
        "project_title": "not specified",
        "agency_or_partner": "not specified",
        "public_problem": "unclear from transcript",
        "why_it_matters": "unclear from transcript",
        "target_population": "not specified",
        "available_data": ["not specified"],
        "expected_outputs": ["not specified"],
        "timeline": ["not specified"],
        "stakeholders": ["not specified"],
        "student_entry_points": ["unclear from transcript"],
        "researcher_opportunities": ["unclear from transcript"],
        "unclear_or_missing": [
            "This fallback output shows the expected JSON shape. With a working API key, these fields should be filled from the transcript."
        ],
        "important_quotes_or_evidence": ["not specified"],
    }


def placeholder_md(title):
    return f"""# {title}

unclear from transcript

Expected full run: this section should be generated from `input/transcript.txt` using the matching prompt file.
"""


def evaluation_text(api_used):
    status = (
        "Generated from `input/transcript.txt`. Review against the transcript."
        if api_used
        else "Fallback run. With a working API key, this file should summarize how well the generated outputs matched the transcript."
    )
    return f"""# Evaluation Notes

## Did the tool preserve uncertainty?
Check whether missing details are marked as `not specified` or `unclear from transcript`.

## Did it avoid inventing details?
Check names, datasets, timelines, deliverables, and quotes against the transcript.

## Are the outputs useful for different audiences?
The agency, researcher, and student briefs should not all read the same.

## What would a human reviewer check?
- Whether the source transcript is complete
- Whether important facts were missed
- Whether proposed deliverables are supported by the transcript
- Whether quotes are traceable

## What failed or felt weak?
{status}
"""


def main():
    OUTPUT.mkdir(exist_ok=True)
    transcript = read(INPUT)
    api_used = bool(os.getenv("OPENAI_API_KEY"))

    try:
        if api_used:
            extraction = json.loads(
                ask_model(read(PROMPTS / "01_extract.txt"), transcript, json_mode=True)
            )
        else:
            extraction = placeholder_extraction()

        FILES["extraction"].write_text(
            json.dumps(extraction, indent=2) + "\n", encoding="utf-8"
        )

        context = json.dumps(extraction, indent=2)
        for key, prompt_file, title in BRIEFS:
            if api_used:
                prompt = read(PROMPTS / prompt_file)
                text = ask_model(f"{prompt}\n\nExtraction:\n{context}", transcript)
            else:
                text = placeholder_md(title)
            FILES[key].write_text(text.strip() + "\n", encoding="utf-8")
    except RuntimeError as exc:
        print(f"warning: {exc}")
        print("warning: writing placeholder outputs")
        api_used = False
        FILES["extraction"].write_text(
            json.dumps(placeholder_extraction(), indent=2) + "\n", encoding="utf-8"
        )
        for key, _prompt_file, title in BRIEFS:
            FILES[key].write_text(placeholder_md(title), encoding="utf-8")

    FILES["evaluation"].write_text(evaluation_text(api_used), encoding="utf-8")

    print("done")
    for path in FILES.values():
        print(path)


if __name__ == "__main__":
    main()
