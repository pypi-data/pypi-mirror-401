# AskUserQuestion UI Test Suite

This test file demonstrates the interactive UI for the `AskUserQuestion` tool integration.

## Running the Tests

```bash
cd /Users/kalilbouzigues/Projects/browgents/reverse-api
uv run python test_ask_user_ui.py
```

## Test Scenarios

### Test 1: Single-Select with Descriptions
Shows a single-choice question where each option has a descriptive label.

**Example:**
```
  ? Agent Question

  Authentication Method

 > Which authentication method should I implement?

   Cookie-based session - Uses session cookies stored in browser
   Bearer token - Uses JWT or API tokens in Authorization header
   Both methods - Auto-detect and support both authentication types
```

**Navigation:**
- Use ↑/↓ arrow keys to navigate
- Press Enter to select
- Selected option label is returned (without description)

---

### Test 2: Multi-Select with Descriptions
Shows a multiple-choice question with checkboxes where each option has a description.

**Example:**
```
  ? Agent Question

  Feature Selection

 > Which features should I include in the API client?

   ○ Automatic retry logic - Retry failed requests with exponential backoff
   ○ Rate limiting - Throttle requests to respect API limits
   ○ Response caching - Cache responses to reduce API calls
   ○ Detailed logging - Add comprehensive debug logging
```

**Navigation:**
- Use ↑/↓ arrow keys to navigate
- Press Space to select/deselect
- Press Enter when done
- Returns comma-separated labels: "Automatic retry logic, Response caching"

---

### Test 3: Multiple Questions in One Call
Demonstrates asking several questions sequentially in a single tool call.

**Example:**
```
  ? Agent Question

  Auth
 > Which authentication method?
   Cookies - Session-based authentication
   Tokens - Token-based authentication

  → Cookies

  Error Handling
 > Should I implement retry logic?
   Yes - Auto-retry with exponential backoff
   No - Fail immediately on errors

  → Yes

  Features
 > Which additional features?
   ○ Logging - Debug logging
   ○ Caching - Response caching
   ○ Metrics - Request metrics tracking

  → Logging, Caching
```

---

### Test 4: Single-Select without Descriptions
Shows a simple single-choice question with labels only (no descriptions).

**Example:**
```
  ? Agent Question

  Use Case

 > What's the primary use case?

   Web scraping
   Data extraction
   API testing
   Automation
```

---

### Test 5: Multi-Select without Descriptions
Shows a checkbox question with labels only.

**Example:**
```
  ? Agent Question

  HTTP Methods

 > Which HTTP methods to support?

   ○ GET
   ○ POST
   ○ PUT
   ○ DELETE
   ○ PATCH
```

---

### Test 6: Mixed Descriptions
Some options have descriptions, others don't (falls back gracefully).

**Example:**
```
  ? Agent Question

  Implementation

 > Choose your preferred approach

   Simple - Basic implementation with minimal features
   Standard
   Advanced - Full-featured with all bells and whistles
```

## Special Features

### User Cancellation (Ctrl+C)
- Pressing Ctrl+C during any question will skip it
- Returns empty string for that answer
- Agent continues execution gracefully

### Answer Format
- **Single-select:** Returns the selected label as a string
  - Example: `"Cookie-based session"`
- **Multi-select:** Returns comma-separated labels
  - Example: `"Automatic retry logic, Response caching, Detailed logging"`

### Return Value Structure
```python
{
    "behavior": "allow",
    "updatedInput": {
        "questions": [...],  # Original questions passed through
        "answers": {
            "Which authentication method?": "Cookies",
            "Should I implement retry logic?": "Yes",
            "Which additional features?": "Logging, Caching"
        }
    }
}
```

## UI Styling

All prompts use your existing theme:
- **Primary color** (`#ff5f50` - Coral Red): Question marks, selected items
- **Secondary color** (white): Question text
- **Dim color** (`#555555`): Context headers and feedback

## Integration with ClaudeEngineer

When the Claude agent calls `AskUserQuestion` during HAR analysis:

1. The `canUseTool` callback intercepts the tool call
2. Questions are displayed with styled prompts
3. User provides answers interactively
4. Answers are returned to the agent
5. Agent continues with the user's preferences

This creates a conversational, interactive experience during API client generation!
