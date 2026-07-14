# Learning by Inventing: RAG and Agentic AI

> **Philosophy.** Every concept in this curriculum is something you will build before it is named. You will hit a wall, feel the frustration of a broken approach, and then invent the fix yourself. Only after you have invented it will you learn what the field calls it.
>
> **Prerequisites.** Basic Python (functions, lists, dicts, loops). High school maths (averages, basic probability). No ML background required.
>
> **Companion files** — download these alongside the curriculum:
> - `acme_datasets.py` — all datasets used across every exercise. Import what you need: `from acme_datasets import DOCUMENTS, STRUCTURED_DOCUMENTS, QA_EVAL_SET`
> - `provider_setup.md` — step-by-step instructions for setting up Anthropic or OpenAI, plus a drop-in wrapper so the same code runs on either provider without changes.
>
> **How each exercise works.** Each exercise has four parts:
> 1. **Observe** — run the starter code and see what happens
> 2. **The problem** — a prompt that breaks the starter code
> 3. **Your task** — fix it using only the hints given
> 4. **Reveal** — what you just invented, and what the field calls it

---

## Module 1 — The Knowledge Gap

*The central question: what does an LLM actually know, and what happens when it doesn't?*

---

### Exercise 1.1 — The Amnesiac Oracle

**Difficulty:** ★☆☆☆☆

**Observe.** Install the Anthropic SDK and run this code.

```python
import anthropic

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env

def ask(question):
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=256,
        messages=[{"role": "user", "content": question}]
    )
    return response.content[0].text

print(ask("What is the capital of France?"))
print(ask("Who wrote Hamlet?"))
```

Both answers come back instantly and correctly.

**The problem.** Now ask it something the model cannot possibly know.

```python
# This is a made-up internal document. The model has never seen it.
print(ask("According to Acme Corp's Q3 2024 internal memo, what is the new expense policy for travel?"))
```

Run it. Read the answer carefully.

**Your task.**

1. The model answered confidently. Is that answer trustworthy? How would you know?
2. Now write a new version of `ask()` called `honest_ask()`. Before calling the API, check whether the question contains the phrase `"internal memo"` or `"Q3 2024"`. If it does, return a plain Python string — no API call — that says something like: `"I don't have access to that document."` Otherwise, call the API normally.

```python
def honest_ask(question):
    # your code here
    pass

print(honest_ask("What is the capital of France?"))
print(honest_ask("According to the Q3 2024 memo, what is the travel policy?"))
```

3. This keyword check is brittle. In one sentence, describe *why* it will fail for most real questions.

**Reflect.** You have just felt the core problem: a language model's knowledge is frozen at training time. It cannot know what happened yesterday, or what is in your company's private database. Your keyword check is a crude patch. The real fix requires giving the model the document at the moment it is asked. That is what the next exercises build toward.

**What you invented:** the intuition behind *retrieval-augmented generation* — the idea that knowledge should come from outside the model, not from inside it.

---

### Exercise 1.2 — Stuffing the Prompt

**Difficulty:** ★★☆☆☆

**Setup.** Import the Acme Corp policy documents from the companion dataset file.

```python
from acme_datasets import DOCUMENTS, DOC_A, DOC_B, DOC_C
```

`DOCUMENTS` is a list of six policy documents (travel, remote work, onboarding, IT security, performance reviews, parental leave). `DOC_A`, `DOC_B`, `DOC_C` are the first three — travel, remote work, and onboarding — which are enough for this exercise. The full set of six is there for you to experiment with once you have the basics working.

**Observe.** Try this approach — put all three documents directly into the prompt.

```python
def ask_with_docs(question, docs):
    combined = "\n\n---\n\n".join(docs)
    prompt = f"""You are a helpful assistant. Use only the documents below to answer the question.
If the answer is not in the documents, say "I don't know."

DOCUMENTS:
{combined}

QUESTION: {question}
"""
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=256,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

all_docs = [DOC_A, DOC_B, DOC_C]
print(ask_with_docs("What is the hotel allowance?", all_docs))
print(ask_with_docs("How many days can I work remotely?", all_docs))
```

It works. The model answers correctly from the documents.

**The problem.** Now imagine you have 10,000 documents instead of 3. Each document is 500 words. Write a short calculation:

```python
words_per_doc = 500
num_docs = 10_000
total_words = words_per_doc * num_docs
approx_tokens = total_words / 0.75  # rough conversion

print(f"Total tokens needed: {approx_tokens:,.0f}")
print(f"That is roughly {approx_tokens / 200_000:.1f}x a 200k context window")
```

Run it. What do you get?

**Your task.**

You cannot stuff all 10,000 documents into the prompt. You need a smarter approach: instead of sending *all* documents, send only the *relevant* ones.

Write a function `find_relevant_docs(question, docs)` that uses simple keyword matching to pick the most relevant document. It should:

1. Split the question into individual words (lowercase).
2. For each document, count how many of those words appear in the document text (lowercase).
3. Return only the single document with the highest count.

```python
def find_relevant_docs(question, docs):
    # your code here
    pass

question = "What is the hotel allowance for travel?"
best_doc = find_relevant_docs(question, all_docs)
print(ask_with_docs(question, [best_doc]))
```

Test it with at least two different questions. Does it always pick the right document?

**Reflect.** You have just reinvented keyword-based retrieval. It is fast and requires no ML. But try this question: `"What is the per-night accommodation limit?"` — does it still pick DOC_A? The word "hotel" does not appear in that question, and "accommodation" appears in both the question and DOC_A. But what if a document used the word "lodging" instead? You would miss it entirely.

**What you invented:** the idea of *retrieval as a preprocessing step* — only sending relevant context to the model. This is the skeleton of RAG. The next module fixes the keyword-matching weakness.

---

## Module 2 — The Search Problem

*The central question: how do you find a document that means the same thing, even when it uses different words?*

---

### Exercise 2.1 — When Words Lie

**Difficulty:** ★★☆☆☆

**Observe.** Build a tiny search engine using your keyword matching function from Exercise 1.2.

```python
from acme_datasets import MINI_CORPUS
mini_corpus = MINI_CORPUS  # 8 sentences — 3 synonymous hotel-rate sentences, 1 unrelated decoy, 4 other policy sentences

def keyword_search(query, corpus):
    query_words = set(query.lower().split())
    scores = []
    for doc in corpus:
        doc_words = set(doc.lower().split())
        overlap = len(query_words & doc_words)
        scores.append((overlap, doc))
    scores.sort(reverse=True)
    return scores

results = keyword_search("what is the hotel allowance", mini_corpus)
for score, doc in results:
    print(f"Score {score}: {doc[:60]}...")
```

**The problem.** The first sentence scores highest because it shares the word "hotel." The second and third sentences mean *exactly the same thing* but score zero — they share no words with the query.

**Your task.** You are going to measure meaning using numbers instead of words. Here is the key idea: words that appear in similar contexts tend to mean similar things. We will use a shortcut — a pre-built table of word vectors.

Install the `sentence-transformers` library.

```bash
pip install sentence-transformers
```

Now run this code and study what it produces.

```python
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

sentences = [
    "The hotel rate is capped at $250 per night.",
    "Accommodation costs must not exceed two hundred and fifty dollars.",
    "Python is a programming language.",
]

embeddings = model.encode(sentences)

print(f"Each sentence becomes a vector of {embeddings.shape[1]} numbers.")
print(f"\nFirst 5 numbers for sentence 1: {embeddings[0][:5].round(3)}")
print(f"First 5 numbers for sentence 2: {embeddings[1][:5].round(3)}")
```

Each sentence is now a list of 384 numbers. Two sentences that mean the same thing should produce similar lists of numbers. But how do you measure "similar"?

**Implement dot-product similarity** between two vectors. Given two vectors `a` and `b` of the same length, their dot product is: sum of `a[i] * b[i]` for all `i`.

```python
def dot_product(vec_a, vec_b):
    # implement without numpy (use a loop)
    # hint: zip(vec_a, vec_b) gives you pairs
    pass

# Test it
a = embeddings[0]
b = embeddings[1]
c = embeddings[2]

print(f"Similarity (sentence 1 vs 2): {dot_product(a, b):.3f}")  # should be high
print(f"Similarity (sentence 1 vs 3): {dot_product(a, c):.3f}")  # should be low
```

Now build a `semantic_search` function:

```python
def semantic_search(query, corpus):
    query_vec = model.encode([query])[0]
    corpus_vecs = model.encode(corpus)
    
    scores = []
    for i, doc_vec in enumerate(corpus_vecs):
        score = dot_product(query_vec, doc_vec)
        scores.append((score, corpus[i]))
    
    scores.sort(reverse=True)
    return scores

results = semantic_search("what is the hotel allowance", mini_corpus)
for score, doc in results:
    print(f"Score {score:.3f}: {doc}")
```

Do the accommodation and lodging sentences now rank above the Python sentence?

**Reflect.** You have just used *embeddings* — dense numerical representations of meaning. The dot product between two embedding vectors is a measure of how semantically similar the two pieces of text are. This is the engine inside every modern search system.

**What you invented:** *semantic search using vector embeddings* — the retrieval backbone of production RAG systems.

---

### Exercise 2.2 — Building a Document Index

**Difficulty:** ★★★☆☆

**The goal.** In the real world, you embed documents *once* (when they are added to the system) and store those embeddings. At query time, you only embed the question — not all the documents again. This is what makes semantic search fast.

**Your task.** Build a simple in-memory vector store.

```python
from sentence_transformers import SentenceTransformer
from acme_datasets import STRUCTURED_DOCUMENTS as documents
# 22 policy passages across travel, remote work, IT security, performance, and parental leave

model = SentenceTransformer("all-MiniLM-L6-v2")
print(f"Loaded {len(documents)} documents")
```

Step 1 — Write an `index_documents` function that takes the list of documents and returns a list of `(document, embedding)` pairs. This simulates the "indexing" phase that happens once.

```python
def index_documents(docs):
    # your code here
    # hint: model.encode([d["text"] for d in docs]) gives you all embeddings at once
    pass

index = index_documents(documents)
print(f"Indexed {len(index)} documents.")
print(f"Each embedding has {len(index[0][1])} dimensions.")
```

Step 2 — Write a `retrieve` function that takes a query string and the index, and returns the top-k most relevant documents.

```python
def retrieve(query, index, top_k=2):
    # your code here
    # 1. embed the query
    # 2. compute dot product with every indexed embedding
    # 3. sort and return top_k documents (just the text and source)
    pass

results = retrieve("How much can I spend on food while travelling?", index, top_k=2)
for doc, score in results:
    print(f"[{score:.3f}] ({doc['source']}) {doc['text']}")
```

Step 3 — Think about this: if you had 1 million documents, computing a dot product with each one for every query would be slow. In one or two sentences, describe what you might do to speed this up. (You do not need to implement anything — just reason about it.)

**What you invented:** a *vector index* — the data structure at the heart of systems like Pinecone, Weaviate, and pgvector.

---

## Module 3 — Inventing RAG

*The central question: how do you combine retrieval with generation to get answers that are grounded in your documents?*

---

### Exercise 3.1 — The Grounded Answer

**Difficulty:** ★★★☆☆

**Observe.** You now have two working pieces: a retrieval system and a language model. Try connecting them naively.

```python
import anthropic
from sentence_transformers import SentenceTransformer

client = anthropic.Anthropic()
model = SentenceTransformer("all-MiniLM-L6-v2")

# Use the index from Exercise 2.2
# (paste your index_documents and retrieve functions here)

def naive_rag(question):
    # Step 1: retrieve
    results = retrieve(question, index, top_k=2)
    context = "\n".join([doc["text"] for doc, score in results])
    
    # Step 2: generate
    prompt = f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

print(naive_rag("How much can I spend on a hotel?"))
```

It works. But there is a subtle problem.

**The problem.** Ask a question that is completely outside the documents.

```python
print(naive_rag("What is the boiling point of water?"))
```

What happens? Does the model say "I don't know" or does it answer from general knowledge, ignoring the retrieved context?

**Your task.** Improve `naive_rag` into `grounded_rag` with two changes:

1. Improve the prompt. Add a clear instruction: *"Answer only using the context provided. If the context does not contain the answer, respond with exactly: I cannot answer this from the provided documents."*

2. Add a *confidence gate*: after retrieval, check the top similarity score. If the best-matching document scores below `0.35`, skip the API call entirely and return the fallback string directly. This saves money and is faster.

```python
def grounded_rag(question, confidence_threshold=0.35):
    results = retrieve(question, index, top_k=2)
    
    # your confidence gate here
    top_score = results[0][1]
    if top_score < confidence_threshold:
        return "I cannot answer this from the provided documents."
    
    # your improved prompt here
    context = "\n".join([doc["text"] for doc, score in results])
    prompt = # your prompt here
    
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

# Test both cases
print(grounded_rag("How much can I spend on a hotel?"))
print(grounded_rag("What is the boiling point of water?"))
print(grounded_rag("Who invented the telephone?"))
```

**Reflect.** You have just built a complete RAG pipeline: retrieve relevant chunks, gate on confidence, generate a grounded answer. The confidence gate is a simple but important production pattern — it prevents the model from hallucinating when retrieval fails.

**What you invented:** *Retrieval-Augmented Generation (RAG)* — the dominant architecture for grounding LLMs in private or recent knowledge.

---

### Exercise 3.2 — Chunking and the Goldilocks Problem

**Difficulty:** ★★★★☆

**The problem.** Real documents are long. If you embed an entire 10-page PDF as one vector, you lose precision — the embedding averages out over too many topics. But if you split every sentence into its own chunk, each chunk loses context. There is a Goldilocks size.

**Observe.** Here is a longer fake document.

```python
long_doc = """
ACME CORP TRAVEL POLICY — FULL VERSION

Section 1: Flights
All domestic flights must be booked at economy class. 
Business class is permitted only for flights exceeding 6 hours.
All flights must be booked at least 14 days in advance to qualify for reimbursement.
Last-minute bookings require VP approval and a written justification.

Section 2: Hotels
Employees are entitled to a maximum of $250 per night for hotel accommodation.
The company has preferred rates with Marriott and Hilton chains.
Extended stays of more than 7 nights require manager sign-off.
Airbnb and similar platforms are not approved for reimbursement.

Section 3: Meals
The daily meal allowance is $60. This covers breakfast, lunch, and dinner.
Alcohol is not reimbursable under any circumstances.
Receipts are required for any single meal exceeding $25.
Team dinners with clients may be expensed separately under the entertainment budget.

Section 4: Ground Transport
Taxis and rideshare are reimbursable for airport transfers.
Personal vehicle use is reimbursed at $0.22 per kilometre.
Car rentals require pre-approval and must use the corporate Avis account.
"""
```

**Your task.** Write a `chunk_document` function that splits this document into overlapping chunks.

```python
def chunk_document(text, chunk_size=100, overlap=20):
    """
    Split text into chunks of approximately `chunk_size` words,
    with `overlap` words of overlap between consecutive chunks.
    
    Args:
        text: the full document string
        chunk_size: target number of words per chunk
        overlap: number of words to repeat at the start of each new chunk
    
    Returns:
        list of strings (chunks)
    """
    words = text.split()
    chunks = []
    start = 0
    
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap  # slide forward, but overlap
    
    return chunks

chunks = chunk_document(long_doc, chunk_size=60, overlap=15)
print(f"Created {len(chunks)} chunks")
for i, chunk in enumerate(chunks):
    print(f"\n--- Chunk {i+1} ---\n{chunk}")
```

Now index the chunks and test retrieval:

```python
chunked_docs = [{"id": i, "text": chunk, "source": "travel_policy_full.txt"} 
                for i, chunk in enumerate(chunks)]

chunk_index = index_documents(chunked_docs)

questions = [
    "Can I fly business class?",
    "Can I use Airbnb?",
    "How much per kilometre for my own car?",
    "Is alcohol reimbursable?",
]

for q in questions:
    results = retrieve(q, chunk_index, top_k=1)
    doc, score = results[0]
    print(f"\nQ: {q}")
    print(f"Score {score:.3f}: {doc['text'][:100]}...")
```

**Experiment.** Change `chunk_size` to 20 (very small) and then to 200 (very large). How does retrieval quality change? Write down your observations as a comment in the code.

**What you invented:** *document chunking with overlap* — a standard preprocessing step in all production RAG systems. The overlap prevents relevant sentences from being split across chunk boundaries.

---

## Module 4 — The Single-Step Limit

*The central question: what happens when answering a question requires doing something — not just knowing something?*

---

### Exercise 4.1 — The Model That Cannot Act

**Difficulty:** ★★☆☆☆

**Observe.** Ask the model something that requires a real-time action.

```python
import anthropic
import datetime

client = anthropic.Anthropic()

def ask(question):
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=200,
        messages=[{"role": "user", "content": question}]
    )
    return response.content[0].text

print(ask("What time is it right now?"))
print(ask("What is 10% of 847.33?"))
print(ask(f"Today is {datetime.date.today()}. How many days until Christmas?"))
```

Run these. Notice:
- The time question: the model either guesses or refuses. It cannot actually check a clock.
- The calculator question: it probably gets it right, but could it get a harder one wrong?
- The date question: once you give it the date, it can reason.

**The problem.** The model is stateless and sandboxed. It cannot call your system clock, run a calculator, search the web, or write a file. It can only process text and return text.

**Your task.** Build a small toolkit of Python functions — things the model *cannot* do but you *can*.

```python
import datetime
import math

def get_current_date():
    """Returns today's date as a string."""
    return str(datetime.date.today())

def calculate(expression):
    """
    Safely evaluate a mathematical expression string.
    Only allows numbers and basic operators.
    Returns the result as a string.
    """
    # Safety: only allow digits, spaces, and basic operators
    allowed = set("0123456789+-*/()., ")
    if not all(c in allowed for c in expression):
        return "Error: invalid expression"
    try:
        result = eval(expression)  # safe because we filtered the input
        return str(round(result, 4))
    except Exception as e:
        return f"Error: {e}"

def days_until(target_date_str):
    """
    Returns the number of days from today until a target date.
    target_date_str format: 'YYYY-MM-DD'
    """
    today = datetime.date.today()
    target = datetime.date.fromisoformat(target_date_str)
    return str((target - today).days)

# Test your tools
print(get_current_date())
print(calculate("847.33 * 0.1"))
print(days_until("2024-12-25"))
```

Now the question is: how does the model *call* these tools? It cannot — it only produces text. So you need to make the model produce text that *describes* a tool call, and then you run the tool yourself.

**Invent a simple protocol.** Ask the model to output tool calls in a structured format. Write a prompt that instructs the model to respond in this format when it needs a tool:

```
TOOL: tool_name
INPUT: the input to the tool
```

And to give a final answer in this format when it is done:

```
ANSWER: the final response to the user
```

```python
TOOL_PROMPT = """You are a helpful assistant. You have access to these tools:

- get_current_date(): returns today's date
- calculate(expression): evaluates a math expression, e.g. calculate(2 + 2)
- days_until(YYYY-MM-DD): returns number of days from today until that date

When you need a tool, respond ONLY with:
TOOL: tool_name
INPUT: the input

When you have a final answer, respond ONLY with:
ANSWER: your answer

Do not include any other text.
"""

def ask_with_tools(question):
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=100,
        messages=[
            {"role": "user", "content": TOOL_PROMPT + "\n\nQuestion: " + question}
        ]
    )
    return response.content[0].text

print(ask_with_tools("What is today's date?"))
print(ask_with_tools("What is 15% of 1247?"))
```

Does the model follow the protocol? Does it output `TOOL:` and `INPUT:` correctly?

**Reflect.** The model produces a structured text response that *describes* what tool to call. You have to parse that text and actually run the tool. This is the key insight: the model is a reasoning engine, not an execution engine. You are the executor.

**What you invented:** the concept of *tool use* (also called *function calling*) — the mechanism that allows language models to request external actions.

---

### Exercise 4.2 — Parsing and Executing Tool Calls

**Difficulty:** ★★★☆☆

**Your task.** Complete the loop: parse the model's text output, run the right tool, and feed the result back.

```python
def parse_response(text):
    """
    Parse the model's text output.
    Returns either:
      ("tool", tool_name, tool_input)   — if the model wants a tool
      ("answer", final_answer)          — if the model has a final answer
      ("unknown", raw_text)             — if parsing fails
    """
    text = text.strip()
    lines = text.split("\n")
    
    if lines[0].startswith("TOOL:"):
        tool_name = lines[0].replace("TOOL:", "").strip()
        tool_input = lines[1].replace("INPUT:", "").strip() if len(lines) > 1 else ""
        return ("tool", tool_name, tool_input)
    
    elif lines[0].startswith("ANSWER:"):
        answer = lines[0].replace("ANSWER:", "").strip()
        return ("answer", answer)
    
    else:
        return ("unknown", text)

def run_tool(tool_name, tool_input):
    """Dispatch to the right Python function."""
    if tool_name == "get_current_date":
        return get_current_date()
    elif tool_name == "calculate":
        return calculate(tool_input)
    elif tool_name.startswith("days_until"):
        return days_until(tool_input)
    else:
        return f"Unknown tool: {tool_name}"
```

Now write a `one_step_agent` function that:
1. Asks the model a question.
2. Parses the response.
3. If it is a tool call, runs the tool and prints the result.
4. If it is an answer, returns it.

```python
def one_step_agent(question):
    raw = ask_with_tools(question)
    print(f"Model said: {raw}")
    
    result = parse_response(raw)
    
    if result[0] == "tool":
        _, tool_name, tool_input = result
        tool_result = run_tool(tool_name, tool_input)
        print(f"Tool result: {tool_result}")
        return f"Tool was called. Result: {tool_result}"
    
    elif result[0] == "answer":
        return result[1]
    
    else:
        return f"Could not parse: {result[1]}"

print(one_step_agent("What is today's date?"))
print(one_step_agent("Calculate 18% of 350."))
```

**The limitation.** Try this question:

```python
print(one_step_agent("How many days from today until New Year's Day next year?"))
```

This question requires *two* tool calls: first `get_current_date()` to know today's date, then `days_until()` to compute the gap. Your `one_step_agent` can only do one. What would it take to handle this?

**Reflect.** A single tool call is not enough for complex questions. You need a loop — the model calls a tool, gets a result, decides if it needs another tool, calls again, and so on. That loop is an agent.

**What you invented:** the *tool execution loop* — the bridge between a model's text output and real-world actions.

---

## Module 5 — Inventing Agents

*The central question: how do you give a model the ability to act repeatedly until a task is complete?*

---

### Exercise 5.1 — The Reasoning Loop

**Difficulty:** ★★★★☆

**The key idea.** An agent is not a single API call. It is a *loop* where:
1. The model receives the question and any previous tool results.
2. The model decides: do I have enough information to answer, or do I need a tool?
3. If it needs a tool, run it, add the result to the conversation, go to step 1.
4. If it has an answer, return it.

**Your task.** Build a multi-turn agent using a conversation history list.

```python
def run_agent(question, max_steps=5):
    """
    A simple agent loop that can call tools multiple times before answering.
    """
    
    # The conversation starts with the system prompt and the user's question
    messages = [
        {
            "role": "user", 
            "content": TOOL_PROMPT + "\n\nQuestion: " + question
        }
    ]
    
    for step in range(max_steps):
        print(f"\n--- Step {step + 1} ---")
        
        # Ask the model what to do next
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=150,
            messages=messages
        )
        model_text = response.content[0].text.strip()
        print(f"Model: {model_text}")
        
        # Add model's response to conversation history
        messages.append({"role": "assistant", "content": model_text})
        
        # Parse what the model said
        result = parse_response(model_text)
        
        if result[0] == "answer":
            print(f"\nFinal answer: {result[1]}")
            return result[1]
        
        elif result[0] == "tool":
            _, tool_name, tool_input = result
            tool_result = run_tool(tool_name, tool_input)
            print(f"Tool result: {tool_result}")
            
            # Feed the tool result back into the conversation
            # so the model can use it in the next step
            messages.append({
                "role": "user",
                "content": f"Tool result: {tool_result}\n\nContinue. If you have enough information, provide the ANSWER. Otherwise, call another tool."
            })
        
        else:
            print(f"Parse failed: {result[1]}")
            break
    
    return "Agent exceeded maximum steps without finding an answer."

# Test the multi-step case
run_agent("How many days from today until New Year's Day next year?")
```

Does it now correctly call `get_current_date` first, then `days_until`?

**Experiment.** Try these questions and count how many steps each one takes:

```python
run_agent("What is today's date?")                               # 1 step
run_agent("What is 22% of 4500?")                               # 1 step
run_agent("How many days until July 4th from today?")           # 2 steps
run_agent("What is 15% of the number of days until New Year?")  # 3 steps — chain!
```

**What you invented:** the *agentic loop* — the core architecture of every AI agent, from simple assistants to autonomous research systems.

---

### Exercise 5.2 — Giving the Agent Memory

**Difficulty:** ★★★★☆

**The problem.** Your current agent has no memory between separate `run_agent` calls. Each call starts fresh. Try this:

```python
run_agent("My monthly budget is $3000.")
run_agent("How much is 40% of my budget?")  # it does not know the budget
```

The second call fails because the agent has no memory of the first.

**Your task.** Add a simple external memory store. The agent gets two new tools:

- `remember(key, value)` — store a piece of information
- `recall(key)` — retrieve a stored piece of information

```python
# Simple in-memory key-value store
memory_store = {}

def remember(key_value):
    """
    Store a value. Input format: "key=value"
    Example: "monthly_budget=3000"
    """
    if "=" not in key_value:
        return "Error: format must be key=value"
    key, value = key_value.split("=", 1)
    memory_store[key.strip()] = value.strip()
    return f"Remembered: {key.strip()} = {value.strip()}"

def recall(key):
    """
    Retrieve a stored value by key.
    """
    key = key.strip()
    if key in memory_store:
        return memory_store[key]
    return f"Nothing stored under '{key}'"
```

Update your `TOOL_PROMPT` to include these two new tools, and update `run_tool` to dispatch to them.

```python
TOOL_PROMPT_V2 = """You are a helpful assistant with access to these tools:

- get_current_date(): returns today's date
- calculate(expression): evaluates a math expression
- days_until(YYYY-MM-DD): returns days from today to target date
- remember(key=value): stores information for later, e.g. remember(budget=3000)
- recall(key): retrieves stored information, e.g. recall(budget)

When you need a tool, respond ONLY with:
TOOL: tool_name
INPUT: the input

When you have a final answer, respond ONLY with:
ANSWER: your answer
"""

def run_tool_v2(tool_name, tool_input):
    if tool_name == "get_current_date":
        return get_current_date()
    elif tool_name == "calculate":
        return calculate(tool_input)
    elif tool_name.startswith("days_until"):
        return days_until(tool_input)
    elif tool_name == "remember":
        return remember(tool_input)
    elif tool_name == "recall":
        return recall(tool_input)
    else:
        return f"Unknown tool: {tool_name}"
```

Now update `run_agent` to use `TOOL_PROMPT_V2` and `run_tool_v2`. Then test:

```python
memory_store.clear()
run_agent("Remember that my monthly budget is 3000.", max_steps=3)
run_agent("How much is 40% of my monthly budget?", max_steps=5)
```

The agent should now call `recall(monthly_budget)`, get `3000`, then call `calculate(3000 * 0.4)`.

**Reflect.** You have added persistent state to a stateless model. The model itself still forgets between calls — but the *system* around it remembers. This pattern (external memory + stateless model) is how real production agents are built.

**What you invented:** *external agent memory* — the pattern used in systems like LangChain's memory modules, AutoGPT's file-based memory, and enterprise AI assistants.

---

### Exercise 5.3 — RAG Agent: Combining Everything

**Difficulty:** ★★★★★

**The goal.** Your final exercise is to combine everything you have built:
- The vector index from Module 2
- The grounded generation from Module 3
- The agentic loop from Module 5

You will build an agent that can both *retrieve information from documents* and *use tools* to perform calculations and remember context — and decide which it needs at each step.

**Add one final tool** to your toolkit:

```python
# Rebuild your index from Exercise 2.2 (paste your index and retrieve functions here)
# Then wrap retrieval as a tool the agent can call

def search_docs(query):
    """
    Search the internal document index and return the most relevant passage.
    """
    results = retrieve(query, index, top_k=1)
    if not results:
        return "No relevant documents found."
    doc, score = results[0]
    if score < 0.30:
        return "No sufficiently relevant documents found."
    return f"[Source: {doc['source']}] {doc['text']}"
```

Update your tool prompt to include `search_docs(query)`, and add it to your dispatch function.

```python
TOOL_PROMPT_FINAL = """You are a helpful assistant for Acme Corp employees.
You have access to these tools:

- search_docs(query): searches the internal policy documents
- calculate(expression): evaluates a math expression
- get_current_date(): returns today's date
- days_until(YYYY-MM-DD): returns days from today to a date
- remember(key=value): stores a fact for later
- recall(key): retrieves a stored fact

Use search_docs first when the question is about company policy.
Use calculate for any arithmetic.
Chain tools as needed — you can call multiple tools before giving a final answer.

When you need a tool:
TOOL: tool_name
INPUT: the input

When you have a final answer:
ANSWER: your answer
"""
```

Test your complete RAG agent:

```python
# These questions require document retrieval
run_agent("What is the hotel allowance per night?", max_steps=3)
run_agent("Can I expense alcohol at a client dinner?", max_steps=3)

# This requires retrieval AND calculation
run_agent("I have a 5-day business trip. What is the maximum I can claim for meals?", max_steps=5)

# This requires retrieval, memory, and calculation
memory_store.clear()
run_agent("Remember that my trip has 5 nights and 4 full travel days.", max_steps=3)
run_agent("Based on my trip, what is the total maximum I can claim for hotel and meals combined?", max_steps=7)
```

**Bonus: measure your agent's accuracy.** The companion dataset includes 15 question-answer pairs for evaluating your completed RAG agent.

```python
from acme_datasets import QA_EVAL_SET

correct = 0
for qa in QA_EVAL_SET:
    print(f"\nQ: {qa['question']}")
    print(f"Expected: {qa['expected_answer']}")
    agent_answer = run_agent(qa['question'], max_steps=5)
    print(f"Agent:    {agent_answer}")
    # Manual check — did the agent get the key facts right?
```

Run this after you have completed the full agent. Grade each answer yourself: does it contain the key fact in `expected_answer`? A score of 10/15 or higher means your RAG agent is working well.

**Reflect on what you built.** Walk through the last question step by step and label each action your agent took:
- Which steps used `recall`?
- Which used `search_docs`?
- Which used `calculate`?
- How many total steps did it take?

**What you invented:** a *RAG-powered tool-using agent* — an architecture that appears in production systems like Perplexity, enterprise knowledge assistants, and AI copilots. You built it from scratch, from first principles.

---

## Epilogue — What You Invented, and What It Is Called

| Exercise | What you built | Industry name |
|---|---|---|
| 1.1 | Detected unanswerable questions | Hallucination detection |
| 1.2 | Selected relevant docs before prompting | Context injection / prompt stuffing |
| 2.1 | Measured meaning with dot products | Semantic similarity / cosine similarity |
| 2.2 | Stored embeddings once, queried many times | Vector index |
| 3.1 | Retrieved then generated, with a fallback | Retrieval-Augmented Generation (RAG) |
| 3.2 | Split long docs into overlapping windows | Chunking with overlap |
| 4.1 | Made the model describe actions as text | Tool use / function calling |
| 4.2 | Parsed model text and ran the right function | Tool dispatcher |
| 5.1 | Looped model + tools until task complete | Agentic loop / ReAct pattern |
| 5.2 | Added persistent storage outside the model | External agent memory |
| 5.3 | Combined retrieval, tools, memory, and loop | RAG agent |

---

## Going Further

Once you have completed all exercises, the natural next steps are:

- **Proper vector databases.** Replace your in-memory index with ChromaDB or Qdrant — both have free local modes and Python clients.
- **The ReAct paper.** Read *ReAct: Synergizing Reasoning and Acting in Language Models* (Yao et al., 2022). It formalises the loop you built in Exercise 5.1.
- **Anthropic's native tool use.** The Anthropic API supports tool/function calling natively — the model returns structured JSON instead of the text protocol you invented. Rewrite your agent using it.
- **Evaluation.** How do you know your RAG system gives good answers? Build a tiny evaluation set: 10 questions with known correct answers from the documents, and measure how often your agent gets them right.
- **Multi-agent systems.** What if one agent specialised in retrieval and another in calculation, and a coordinator agent decided which to call? That is a multi-agent system — the current frontier.
