# OpenAI File Analyzer

A simple Python CLI tool that analyzes large text or log files using OpenAI models.
It automatically chunks large files to stay within token limits and aggregates results
into a concise final answer.

## Features
- Handles very large files via chunking
- CLI-based and easy to use
- Focused summaries based on a user-defined question
- Uses OpenAI Chat Completions API

## Requirements
- Python 3.9+
- An OpenAI API key

## Installation
```bash
pip install openai
```


Usage
export OPENAI_API_KEY="your_api_key_here"
python analyzer.py

You’ll be prompted for:

Path to the file to analyze

What you want to find or summarize

Example
Path to the file to analyze: server.log
What do you want to find or summarize? Errors and warnings

Notes

Designed for text-based files (logs, reports, dumps)

Large files are chunked automatically
