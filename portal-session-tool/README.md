# NC Project Portal Session Tool

Small prototype for turning Project Portal session text into structured notes.

Source used for this run:

https://projectportal.nc.gov/project-assets/dncr-economic-impact/dncr-economic-impact-info-session-recording-2026-03-31.mp4

## Workflow

The tool reads `input/transcript.txt` and writes:

- `output/extraction.json`
- `output/agency_brief.md`
- `output/researcher_brief.md`
- `output/student_brief.md`
- `output/clarifying_questions.md`
- `output/evaluation_notes.md`

The prompts are in `prompts/`.

The main rule is: do not fill in missing information. Use `not specified` or `unclear from transcript`.

## Run

```bash
python3 run.py
```

If `python` works on your machine, this also works:

```bash
python run.py
```

To use the OpenAI API:

```bash
export OPENAI_API_KEY="sk-..."
python3 run.py
```
I tried to use the OpenAI API, but the account returned `insufficient_quota`, and with a short test I figured to at least project the idea that I want to pursue. I used WhisperWeb to transcribe the DNCR recording instead:

https://whisperweb.dev

The free transcription had a time limit, so a full run would need paid transcription, local Whisper, or OpenAI credits.

For this submission, I pasted the available (20min) transcript into `input/transcript.txt` and produced the output files from that transcript.

Check:

- preserve uncertainty
- avoid invented deadlines, datasets, or methods
- separate agency, researcher, and student needs
- ask useful follow-up questions
- stay grounded in the transcript

More detail is in `implementation_notes.md` and `output/evaluation_notes.md`.
