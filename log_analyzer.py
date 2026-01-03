import os
from typing import List

from openai import OpenAI

# Chunk large files so each request stays within token limits.
def _chunk_text(text: str, max_chars: int = 12000) -> List[str]:
    return [text[i : i + max_chars] for i in range(0, len(text), max_chars)] or [""]


def analyze_file_with_openai(path: str, question: str, model: str = "gpt-4o-mini") -> str:
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("Set OPENAI_API_KEY in your environment before running this script.")

    if not os.path.isfile(path):
        raise FileNotFoundError(f"File not found: {path}")

    with open(path, "r", encoding="utf-8", errors="ignore") as handle:
        content = handle.read()

    client = OpenAI()
    chunks = _chunk_text(content)

    # First pass: summarize each chunk with the given question in mind.
    chunk_summaries = []
    for idx, chunk in enumerate(chunks, start=1):
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a concise log/text analysis assistant. Summarize key points relevant to the user's question.",
                },
                {"role": "user", "content": f"Question: {question}\nChunk {idx}/{len(chunks)}:\n{chunk}"},
            ],
            temperature=0.2,
        )
        chunk_summaries.append(response.choices[0].message.content.strip())

    # Second pass: consolidate chunk summaries into a final answer.
    summary_blob = "\n\n".join(f"Chunk {i+1}: {s}" for i, s in enumerate(chunk_summaries))
    final = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You aggregate prior summaries to answer the user's question. Be direct and brief, list findings if needed.",
            },
            {"role": "user", "content": f"Question: {question}\nHere are the chunk summaries:\n{summary_blob}"},
        ],
        temperature=0.2,
    )
    return final.choices[0].message.content.strip()


def main() -> None:
    print("Log/Text Analyzer (OpenAI-powered)")
    target = input("Path to the file to analyze: ").strip()
    question = input("What do you want to find or summarize? ").strip()

    try:
        answer = analyze_file_with_openai(target, question)
    except Exception as exc:  # Keep simple for CLI friendliness
        print(f"Error: {exc}")
        return

    print("\n--- Analysis ---")
    print(answer)


if __name__ == "__main__":
    main()
