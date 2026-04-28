---
name: expand-memory-limit
description: Expand Hermes Agent's persistent memory character limit beyond the default 2,200 chars. Default limit is too small for users who need the agent to remember many facts, preferences, and configurations.
tags: [hermes, config, memory, limit]
---

# Expand Memory Character Limit

Hermes Agent's persistent memory has a default limit of **2,200 characters** for the `memory` store and **1,375** for the `user` profile. This skill shows you how to increase them.

## How to Expand

### Step 1: Locate config.yaml

```bash
# Default location
cat ~/.hermes/config.yaml | grep -A10 'memory:'
```

You should see something like:

```yaml
memory:
  memory_enabled: true
  user_profile_enabled: true
  memory_char_limit: 2200
  user_char_limit: 1375
```

### Step 2: Edit the limit values

Use `patch` to change the values:

```python
from hermes_tools import patch

# Expand memory store to 22000 chars (10x)
patch(path="~/.hermes/config.yaml",
      old_string="  memory_char_limit: 2200",
      new_string="  memory_char_limit: 22000")

# Optionally expand user profile too
patch(path="~/.hermes/config.yaml",
      old_string="  user_char_limit: 1375",
      new_string="  user_char_limit: 10000")
```

Or directly edit with `write_file`:

```bash
# Read the full config
cat ~/.hermes/config.yaml > /tmp/hermes_config.yaml

# Find and edit the memory section
# Change memory_char_limit and user_char_limit to your desired values

# Write back
cp /tmp/hermes_config.yaml ~/.hermes/config.yaml
```

### Step 3: Verify

```bash
grep -A5 'memory_char_limit' ~/.hermes/config.yaml
```

Expected output:
```yaml
  memory_char_limit: 22000
  user_char_limit: 10000
```

### Step 4: Test

Add a memory entry to confirm it works:

```
memory(action="add", target="memory", content="This is a test of the expanded memory limit - it should accept much longer entries now!")
```

## How Much to Set

| Use Case | Recommended Limit |
|----------|------------------|
| Light use (just name & few prefs) | 2,200 (default) |
| Moderate (projects, tools, workflows) | 10,000 |
| Heavy (full personal assistant with many domains) | 22,000 |
| Industrial (agent with extensive knowledge base) | 50,000 |

**Note:** Memory is injected into every LLM turn. Setting it too high (>50,000) increases token usage on every message. 22,000 is a good balance for most users.

## Pitfalls

1. **Memory is not a database.** Don't store large data dumps, logs, or temporary state. Use Notion DBs for structured data, skills for procedural knowledge.
2. **Token cost.** Every character in memory is sent as context on every turn. 22k chars ≈ 5-6k tokens extra per message.
3. **Restart not needed.** Changes take effect immediately on next message.
4. **File location.** If you use a custom `HERMES_HOME` path, the config is at `$HERMES_HOME/config.yaml`, not `~/.hermes/config.yaml`.
