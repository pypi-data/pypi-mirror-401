# Accuracy Evaluation Prompt

You are evaluating documentation accuracy by comparing it against source code.

## Source Code
{{SOURCE_CODE}}

## Generated Documentation
{{DOC_CONTENT}}

## Task

Rate the accuracy of the documentation on a scale of 1-5:

| Score | Meaning |
|-------|---------|
| 1 | Major factual errors, hallucinations present |
| 2 | Several inaccuracies that could mislead readers |
| 3 | Mostly accurate with some minor errors |
| 4 | Accurate with only trivial issues |
| 5 | Completely accurate, matches source code |

## What to Check

1. **Function Signatures**
   - Do the documented function names exist in code?
   - Are parameter types correct?
   - Are return types accurate?

2. **API Endpoints**
   - Are HTTP methods correct (GET vs POST)?
   - Are paths accurate?
   - Do request/response schemas match?

3. **Data Models**
   - Do struct/type names exist?
   - Are field names and types correct?
   - Are relationships accurate?

4. **Business Logic**
   - Is the described behavior correct?
   - Are any features hallucinated?
   - Are error conditions accurately described?

## Output Format

Respond with JSON only:

```json
{
  "score": <1-5>,
  "errors": [
    {
      "location": "Section or line reference",
      "issue": "What is wrong",
      "correct": "What it should be (if known)"
    }
  ],
  "summary": "Brief summary of accuracy assessment"
}
```
