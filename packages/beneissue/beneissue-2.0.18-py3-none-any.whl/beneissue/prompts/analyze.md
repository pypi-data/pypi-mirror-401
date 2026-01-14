Analyze GitHub issue and determine fix approach.

**Title**: {issue_title}

**Body**:
{issue_body}

## Classification Rules

### Step 0: Bug Reproduction Check (for bug reports only)

If this issue reports a bug (error, exception, parsing failure, etc.):
1. Check if the issue can be reproduced with `samples/pdf/1901.03003.pdf`
2. If YES → proceed to Step 1
3. If NO (issue requires a specific document to reproduce):
   - Set fix_decision: "comment_only"
   - Set comment_draft: "We couldn't reproduce this issue with our test documents. Could you please send a sample file that reproduces the problem to open.dataloader@hancom.com? This will help us investigate and fix the issue."
   - Skip remaining steps

### Step 1: Code change needed?
- No (docs question, usage help, discussion) → **comment_only**
- Yes → Step 2

### Step 2: Auto-fix eligible? (ALL must be true)
- [ ] Self-contained: No external service setup or credential creation needed
- [ ] Requirements clear: Issue describes what to do (not just the problem)
- [ ] Single-session: No iterative human feedback loops required
- [ ] Accessible: All affected code is in this repository

All true → **auto_eligible**, otherwise → **manual_required**

## Assignee
1. Read `.claude/skills/beneissue/beneissue-config.yml` for team members
2. If team members exist with `available: true` and non-empty `github_id`: assign best specialty match
3. If no valid team members configured: assign to repo owner "{repo_owner}"
4. Always provide an assignee - never leave it null

## Output (JSON only)

```json
{{
  "summary": "2-3 sentences: what the issue is, root cause, fix approach",
  "affected_files": ["path/to/file.py"],
  "fix_decision": "auto_eligible | manual_required | comment_only",
  "reason": "1-sentence justification for fix_decision",
  "priority": "P0 | P1 | P2",
  "story_points": 1 | 2 | 3 | 5 | 8,
  "labels": ["bug"],
  "assignee": "github_id (required - always assign someone)",
  "comment_draft": "null, or response if comment_only"
}}
```
