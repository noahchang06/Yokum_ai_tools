# Implementation Notes

I treated the assignment as a workflow test, not an app build. The useful part is the structure of the notes, not a polished interface.

I used this recording:

https://projectportal.nc.gov/project-assets/dncr-economic-impact/dncr-economic-impact-info-session-recording-2026-03-31.mp4

The session is about DNCR wanting to estimate the economic impact of its sites and programs.

## Workflow

1. Put transcript text in `input/transcript.txt`.
2. Keep reusable prompts in `prompts/`.
3. Run `python3 run.py`.
4. Review files in `output/`.

## Output Choices

- `extraction.json`: structured facts and missing information
- `agency_brief.md`: agency-facing summary
- `researcher_brief.md`: research questions, data needs, risks
- `student_brief.md`: possible student roles
- `clarifying_questions.md`: follow-up questions
- `evaluation_notes.md`: what worked and what did not

## Blocker

I tried the OpenAI API, but it returned `insufficient_quota`. I used WhisperWeb for transcription:

https://whisperweb.dev

WhisperWeb's free limit was shorter than the recording, so the current transcript is only what I was able to get without paid transcription. A full run would need paid transcription, local Whisper, or working OpenAI credits.

## With Credits

With API credits, I would transcribe the full recording, save it as `input/transcript.txt`, set:

```bash
export OPENAI_API_KEY="sk-..."
```

Then run:

```bash
python3 run.py
```

## Evaluation

- Did the output match the transcript?
- Did it say `not specified` or `unclear from transcript` when needed?
- Did it avoid inventing details?
- Were the briefs useful for different audiences?
- Were the questions specific enough for a follow-up call?
