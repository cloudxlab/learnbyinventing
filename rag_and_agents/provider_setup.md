# Provider Setup Guide — Anthropic and OpenAI

This guide covers everything you need to run the curriculum with either provider.
All exercises in the curriculum are written for Anthropic by default.
This file shows you the exact code changes needed to switch to OpenAI.

---

## Part 1 — Installation and API Keys

### Step 1: Install the libraries

Open your terminal and run:

```bash
# For Anthropic
pip install anthropic

# For OpenAI
pip install openai

# For embeddings (used in both tracks — same library either way)
pip install sentence-transformers

# Verify everything installed
python -c "import anthropic; import openai; import sentence_transformers; print('All good.')"
```

### Step 2: Get your API key

**Anthropic**

1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign up or log in.
3. Click **API Keys** in the left sidebar.
4. Click **Create Key**, give it a name (e.g. `rag-curriculum`), copy it.
5. New accounts receive free credits to start. Usage-based billing after that.
6. Pricing reference: Haiku (the model used in exercises) costs approximately $0.25 per million input tokens — running all 11 exercises will cost well under $0.10 total.

**OpenAI**

1. Go to [platform.openai.com](https://platform.openai.com)
2. Sign up or log in.
3. Click your profile → **API keys** → **Create new secret key**.
4. Copy it immediately — OpenAI does not show it again.
5. You may need to add a payment method before your key becomes active.
6. Pricing reference: GPT-4o-mini (the model used in exercises) costs approximately $0.15 per million input tokens — similarly cheap for this curriculum.

### Step 3: Store your key as an environment variable

Never paste your API key directly into code. Store it as an environment variable instead.

**macOS / Linux**

```bash
# Add to your shell config so it persists across sessions
echo 'export ANTHROPIC_API_KEY="sk-ant-your-key-here"' >> ~/.zshrc
echo 'export OPENAI_API_KEY="sk-your-key-here"' >> ~/.zshrc
source ~/.zshrc

# Verify
echo $ANTHROPIC_API_KEY
```

**Windows (Command Prompt)**

```cmd
setx ANTHROPIC_API_KEY "sk-ant-your-key-here"
setx OPENAI_API_KEY "sk-your-key-here"
```

Restart your terminal after running `setx`.

**Windows (PowerShell)**

```powershell
[System.Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "sk-ant-your-key-here", "User")
[System.Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "sk-your-key-here", "User")
```

**In a Jupyter notebook or Google Colab**

```python
import os
os.environ["ANTHROPIC_API_KEY"] = "sk-ant-your-key-here"  # temporary, this session only
os.environ["OPENAI_API_KEY"] = "sk-your-key-here"
```

For Colab, use the Secrets panel (the key icon in the left sidebar) — it is more secure than pasting keys into cells.

---

## Part 2 — Model Reference

Use these model names in the exercises. Swap the string in `model=` to change provider.

| Task | Anthropic model | OpenAI model |
|---|---|---|
| All exercises (fast, cheap) | `claude-haiku-4-5-20251001` | `gpt-4o-mini` |
| Better reasoning (optional) | `claude-sonnet-4-6` | `gpt-4o` |

---

## Part 3 — Code Translation Table

Every API call in the curriculum maps directly between providers.
The pattern is always the same: find the four moving parts and swap them.

### The four moving parts

| Part | Anthropic | OpenAI |
|---|---|---|
| Import | `import anthropic` | `from openai import OpenAI` |
| Client | `anthropic.Anthropic()` | `OpenAI()` |
| Call method | `client.messages.create(...)` | `client.chat.completions.create(...)` |
| Extract text | `response.content[0].text` | `response.choices[0].message.content` |

### Side-by-side examples

**Basic ask function**

```python
# --- ANTHROPIC ---
import anthropic
client = anthropic.Anthropic()

def ask(question):
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=256,
        messages=[{"role": "user", "content": question}]
    )
    return response.content[0].text


# --- OPENAI ---
from openai import OpenAI
client = OpenAI()

def ask(question):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=256,
        messages=[{"role": "user", "content": question}]
    )
    return response.choices[0].message.content
```

**Ask with a system prompt**

```python
# --- ANTHROPIC ---
response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=256,
    system="You are a helpful HR assistant.",          # <-- separate system param
    messages=[{"role": "user", "content": question}]
)
return response.content[0].text


# --- OPENAI ---
response = client.chat.completions.create(
    model="gpt-4o-mini",
    max_tokens=256,
    messages=[
        {"role": "system", "content": "You are a helpful HR assistant."},  # <-- inside messages list
        {"role": "user", "content": question}
    ]
)
return response.choices[0].message.content
```

**Multi-turn conversation (used in Module 5 agent loop)**

```python
# --- ANTHROPIC ---
messages = [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi! How can I help?"},
    {"role": "user", "content": "What is 2 + 2?"},
]
response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=100,
    messages=messages
)
reply = response.content[0].text


# --- OPENAI ---
messages = [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi! How can I help?"},
    {"role": "user", "content": "What is 2 + 2?"},
]
response = client.chat.completions.create(
    model="gpt-4o-mini",
    max_tokens=100,
    messages=messages
)
reply = response.choices[0].message.content
```

The message list format (`role` / `content` dicts) is identical between providers — only the client method and response extraction differ.

---

## Part 4 — Provider-Agnostic Wrapper

Rather than rewriting every exercise, add this block at the top of your script.
Set `PROVIDER = "anthropic"` or `PROVIDER = "openai"` and the rest of your code stays unchanged.

```python
# ── provider_setup.py ──────────────────────────────────────────────────────
# Paste this at the top of any exercise file, then use `llm_call()` throughout.

PROVIDER = "anthropic"  # change to "openai" to switch providers

if PROVIDER == "anthropic":
    import anthropic
    _client = anthropic.Anthropic()

    def llm_call(messages, system=None, max_tokens=512):
        """
        Send a list of messages and return the reply as a plain string.
        messages: list of {"role": ..., "content": ...} dicts
        system:   optional system prompt string
        """
        kwargs = dict(
            model="claude-haiku-4-5-20251001",
            max_tokens=max_tokens,
            messages=messages,
        )
        if system:
            kwargs["system"] = system
        response = _client.messages.create(**kwargs)
        return response.content[0].text

elif PROVIDER == "openai":
    from openai import OpenAI
    _client = OpenAI()

    def llm_call(messages, system=None, max_tokens=512):
        """
        Send a list of messages and return the reply as a plain string.
        messages: list of {"role": ..., "content": ...} dicts
        system:   optional system prompt string
        """
        full_messages = messages
        if system:
            full_messages = [{"role": "system", "content": system}] + messages
        response = _client.chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=max_tokens,
            messages=full_messages,
        )
        return response.choices[0].message.content

else:
    raise ValueError(f"Unknown provider: {PROVIDER}. Choose 'anthropic' or 'openai'.")

# ── End of wrapper ──────────────────────────────────────────────────────────


# Example usage (same code works for both providers):
def ask(question):
    return llm_call([{"role": "user", "content": question}])

def ask_with_system(question, system_prompt):
    return llm_call([{"role": "user", "content": question}], system=system_prompt)

def ask_with_history(messages):
    return llm_call(messages)
```

### How to use the wrapper in each exercise

Replace every `client.messages.create(...)` call in the curriculum with `llm_call(...)`.

**Exercise 1.1 — before and after**

```python
# Before (Anthropic-specific)
response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=256,
    messages=[{"role": "user", "content": question}]
)
return response.content[0].text

# After (works with both providers)
return llm_call([{"role": "user", "content": question}], max_tokens=256)
```

**Exercise 5.1 agent loop — before and after**

```python
# Before
response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=150,
    messages=messages
)
model_text = response.content[0].text

# After
model_text = llm_call(messages, system=TOOL_PROMPT, max_tokens=150)
# Note: move your TOOL_PROMPT into the system= argument to keep messages clean
```

---

## Part 5 — Embeddings

The curriculum uses `sentence-transformers` for embeddings — a local, free library that runs entirely on your machine with no API calls. This is the same regardless of whether you use Anthropic or OpenAI for the language model.

```python
from sentence_transformers import SentenceTransformer

embed_model = SentenceTransformer("all-MiniLM-L6-v2")  # downloads ~80MB on first run

# Embed a list of strings — returns a numpy array of shape (n, 384)
vectors = embed_model.encode(["Hello world", "How are you?"])
```

If you want to use OpenAI's embedding API instead (for consistency, or if you cannot install sentence-transformers), here is the equivalent:

```python
from openai import OpenAI
client = OpenAI()

def embed(texts):
    """
    texts: a list of strings
    returns: list of embedding vectors (each a list of 1536 floats)
    """
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts
    )
    return [item.embedding for item in response.data]

# Usage
vectors = embed(["Hello world", "How are you?"])
print(f"Each vector has {len(vectors[0])} dimensions")  # 1536
```

Note that OpenAI embeddings have 1536 dimensions vs 384 for sentence-transformers. Your dot-product similarity function works identically — just more numbers to multiply.

---

## Part 6 — Troubleshooting

**`AuthenticationError` or `401 Unauthorized`**
Your API key is wrong or not loaded. Run `python -c "import os; print(os.environ.get('ANTHROPIC_API_KEY', 'NOT SET'))"` to check. If it prints `NOT SET`, your environment variable was not saved. Re-run the Step 3 commands and restart your terminal.

**`RateLimitError` or `429 Too Many Requests`**
You are sending too many requests too fast. Add `import time; time.sleep(1)` between API calls in loops.

**`sentence_transformers` is slow on first run**
The model downloads about 80MB on first use. This is normal. It is cached locally after that.

**Responses are cut off mid-sentence**
Increase `max_tokens`. The exercises use 256 for simple questions and 512 for agent steps. Try 1024 if needed.

**OpenAI returns `None` for content**
This happens when the model triggers a content filter. Try rephrasing your test question — the fake Acme Corp documents are safe, but unusual phrasings can occasionally trigger filters.

**`ModuleNotFoundError: No module named 'anthropic'`**
Run `pip install anthropic` in the same Python environment your script uses. If you are in a virtual environment, make sure it is activated.
