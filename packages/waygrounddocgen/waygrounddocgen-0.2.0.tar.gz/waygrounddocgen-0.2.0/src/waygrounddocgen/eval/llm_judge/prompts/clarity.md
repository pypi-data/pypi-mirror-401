# Clarity Evaluation Prompt

You are evaluating how clear and understandable documentation is.

## Module Information

**Name:** {{MODULE_NAME}}
**Target Audience:** Software developers unfamiliar with this codebase

## Generated Documentation

{{DOC_CONTENT}}

## Task

Rate the clarity of the documentation on a scale of 1-5:

| Score | Meaning |
|-------|---------|
| 1 | Confusing, poorly organized, hard to follow |
| 2 | Below average clarity, significant confusion |
| 3 | Acceptable, some areas unclear |
| 4 | Clear and well-organized, minor issues |
| 5 | Excellent clarity, easy to understand |

## What to Check

1. **Structure & Organization**
   - Is there a logical flow?
   - Are sections well-organized?
   - Is navigation easy?

2. **Language & Writing**
   - Is the writing clear and concise?
   - Is jargon explained?
   - Are sentences easy to parse?

3. **Examples & Illustrations**
   - Are code examples helpful?
   - Do diagrams clarify concepts?
   - Are examples realistic?

4. **Onboarding Value**
   - Could a new developer understand the module?
   - Is the "why" explained, not just "what"?
   - Are common use cases covered?

5. **Technical Accuracy of Explanations**
   - Are technical concepts explained correctly?
   - Is the level of detail appropriate?

## Output Format

Respond with JSON only:

```json
{
  "score": <1-5>,
  "issues": [
    {
      "section": "Section name",
      "problem": "What makes it unclear",
      "suggestion": "How to improve"
    }
  ],
  "strengths": [
    "Things the documentation does well"
  ],
  "summary": "Brief summary of clarity assessment"
}
```
