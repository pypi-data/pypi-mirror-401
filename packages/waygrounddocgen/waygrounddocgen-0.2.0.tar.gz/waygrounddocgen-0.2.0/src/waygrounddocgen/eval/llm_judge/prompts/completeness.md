# Completeness Evaluation Prompt

You are evaluating if documentation covers all important aspects of a module.

## Module Information

**Name:** {{MODULE_NAME}}
**Description:** {{MODULE_DESCRIPTION}}

**Expected Entry Points:**
{{ENTRY_POINTS}}

**Expected API Endpoints:**
{{API_ENDPOINTS}}

**Expected Data Structures:**
{{STRUCTS}}

## Generated Documentation

{{DOC_CONTENT}}

## Task

Rate the completeness of the documentation on a scale of 1-5:

| Score | Meaning |
|-------|---------|
| 1 | Most items undocumented, major gaps |
| 2 | Many items missing, incomplete coverage |
| 3 | Core items covered, but gaps exist |
| 4 | Good coverage, minor items missing |
| 5 | Comprehensive, all items documented |

## What to Check

1. **Entry Points Coverage**
   - Are all controllers/handlers documented?
   - Are all service methods mentioned?

2. **API Endpoint Coverage**
   - Is every endpoint listed?
   - Are request/response formats shown?
   - Are authentication requirements noted?

3. **Data Model Coverage**
   - Are all structs/types explained?
   - Are important fields described?

4. **Architecture Coverage**
   - Is the overall structure clear?
   - Are dependencies documented?
   - Is the data flow explained?

5. **Error Handling**
   - Are error codes/responses documented?
   - Are edge cases mentioned?

## Output Format

Respond with JSON only:

```json
{
  "score": <1-5>,
  "missing": [
    "List of undocumented items"
  ],
  "insufficient": [
    "Items with weak/incomplete descriptions"
  ],
  "coverage_summary": {
    "entry_points": "X of Y documented",
    "endpoints": "X of Y documented",
    "structs": "X of Y documented"
  },
  "summary": "Brief summary of completeness assessment"
}
```
