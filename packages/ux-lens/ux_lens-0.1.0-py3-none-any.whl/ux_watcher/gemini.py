"""Gemini video analysis module using google.genai."""

import os
import time
from google import genai


def analyze_video(video_path: str) -> str:
    """
    Send video to Gemini for UX critique.

    Args:
        video_path: Path to the video file

    Returns:
        UX critique text from Gemini
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set.")

    model_name = os.getenv("GEMINI_MODEL", "gemini-3-flash-preview")

    client = genai.Client(api_key=api_key)

    # Upload video using module-level function
    video_file = client.files.upload(file=video_path)

    # Wait for the file to be processed
    while video_file.state.name == "PROCESSING":
        time.sleep(2)
        video_file = client.files.get(name=video_file.name)

    if video_file.state.name == "FAILED":
        raise ValueError(f"Video processing failed: {video_file.name}")

    prompt = """You are a world-class frontend developer and UX expert.

Watch this complete user session on a website. Provide a comprehensive, brutal critique covering:

## UX Issues
- Navigation clarity and flow problems
- User confusion points
- Call-to-action effectiveness
- Information hierarchy issues

## Frontend Problems
- Visual design issues (spacing, typography, color)
- Responsive behavior problems
- Accessibility violations
- Component consistency issues

## Performance
- Loading states and perceived performance
- Animation smoothness
- Interaction feedback

## Actionable Fixes
For each issue, provide:
1. What is wrong (be specific)
2. Why it matters
3. Concrete code suggestion to fix it

Be honest and detailed. Focus on issues that would frustrate real users."""

    response = client.models.generate_content(
        model=model_name,
        contents=[prompt, video_file]
    )

    return response.text


if __name__ == "__main__":
    # Quick test - requires video file
    import sys
    if len(sys.argv) > 1:
        print(analyze_video(sys.argv[1]))
    else:
        print("Usage: python -m ux_watcher.gemini <video_path>")