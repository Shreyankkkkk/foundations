# Claude 101

---

## Source and attribution

These notes are my personal study notes based on Anthropic's Claude 101 course.

- Course: Claude 101
- Provider: Anthropic
- Source: https://anthropic.skilljar.com/
- Copyright: © 2025 Anthropic. All rights reserved.

These notes are independently written summaries for educational and reference purposes and are not official Anthropic course materials.

---

## Lesson 1

### Learning Objectives

- Explain what Claude is and the principles that guide its design
- Describe Claude's core capabilities and how it differs from a simple chatbot
- Identify the different ways to access Claude (web, desktop, and mobile)

---

### Course Roadmap

**1. Meet Claude**

> What is Claude, how do you talk to it, and how do you get great results?
> ↓
> **2. Organizing your work**
> Projects → Artifacts → Skills
> ↓
> **3. Expanding Claude's reach**
> Connectors → Enterprise Search → Research
> ↓
> **4. Putting it all together**
> Claude across roles → Where else can you work with Claude?
> ↓
> **5. Conclusion & certificate**
> Where do you go from here? → How do you earn your certificate?

---

### What is Claude?

- **Claude is an AI assistant and thinking partner**, not just a chatbot.
- Designed to help with a wide range of work tasks and complex problems.

---

#### Key characteristics

- **Helpful, harmless, and honest**
  - Guided by principles intended to avoid toxic/discriminatory outputs and assistance with illegal or unethical activities.
  - Uses **Constitutional AI** to align behavior with human values and promote transparent, reliable behavior.

- **More than a chatbot**
  - Can perform tasks such as:
    - Summarization
    - Search
    - Creative and collaborative writing
    - Q&A
    - Coding
    - Complex problem-solving
  - Designed to act as a **thinking partner** rather than simply provide answers.

- **Steerable and collaborative**
  - Can be directed on:
    - Personality
    - Tone
    - Behavior
  - Designed to be easier to converse with and more steerable, allowing users to get their desired output with less effort.

- **Available across devices**
  - Available on **web, desktop, and mobile**.
  - Available across **Free, Pro, Max, Team, and Enterprise** plans.
  - When signed in, **conversations, projects, memory, and preferences sync across devices**.

---

### Understanding Claude's capabilities

Claude can help with tasks that go beyond simple question-and-answer interactions. It can act as a **thinking partner** that both **automates** and **augments** your work.

---

#### Thinking partner vs. search box

The key difference is whether the request needs **your situation, context, judgment, or existing work**.

- A **search box** is best for:
  - Simple facts
  - Definitions
  - Calculations
  - Current information
  - Questions with one straightforward answer

- A **thinking partner** is best when:
  - Your own work or context is involved
  - The task requires judgment or reasoning
  - You want to transform or improve something you've created
  - You need to explore a problem collaboratively
  - You may need to provide feedback and refine the result

> **A search box takes a question. Claude takes the situation.**

---

#### Which requests need a thinking partner?

##### 1. Exchange rate

> "What's the exchange rate from US dollars to euros today?"

**Search-box territory**

- This requires one current fact from an authoritative source.
- Nothing about the user's specific situation changes the answer.
- A search engine or simple lookup is sufficient.

---

##### 2. Rewriting an update

> "Rewrite my update below so the delay reads as a decision, not an apology."

**Thinking-partner work**

- Claude needs to work with the user's existing draft.
- It must preserve the facts while making a judgment about tone and framing.
- The user can provide feedback and ask Claude to adjust the result.

**Key idea:** The task becomes collaborative because the user's content and judgment are part of the work.

---

##### 3. Structuring a quarterly business review

> "best structure for a quarterly business review presentation"

**Thinking-partner work — when context is provided**

- As written, this looks like a search query.
- A search engine can provide generic presentation templates.
- Claude becomes more useful when given the user's specific context.

**Better version:**

> "Here's last quarter's review and the two slides leadership pushed back on. Restructure the story for this quarter."

**Key idea:** The value comes from giving Claude the situation, not just asking for a generic answer.

---

##### 4. Understanding a customer's complaint

> "I've pasted a customer's complaint thread below. Help me work out what they're actually asking for before I reply."

**Thinking-partner work**

- There may be no external page or fact to look up.
- Claude needs to read and interpret the conversation.
- The user can correct Claude's interpretation and refine the understanding.

**Example:**

> "No, they're not after a refund. They want a firm date."

**Key idea:** The back-and-forth between the user and Claude is part of the task.

---

##### 5. Purchase order vs. invoice

> "What's the difference between a purchase order and an invoice?"

**Search-box territory**

- This is a straightforward definition.
- A search engine or Claude can provide the same basic explanation.
- The question does not require knowledge of the user's specific situation.

**It becomes thinking-partner work when context is added:**

> "A vendor sent us an invoice with no PO attached. Given how our team handles approvals, what should we do next?"

**Key idea:** Adding your real situation turns a general question into a problem that requires reasoning.

---

##### 6. Calculating working days

> "How many working days are there between March 3 and March 24?"

**Search-box territory**

- This can be answered directly with a calculation or calendar.
- There is no personal context for Claude to reason about.
- Not every request needs a thinking partner.

---

#### The six, side by side

The topic itself does **not** determine whether you need a search box or a thinking partner.

For example, reviews, invoices, and exchange rates can all be typed into a search box. The important question is whether the answer needs **you** and your context.

##### Search-box territory

- "What's the exchange rate from US dollars to euros today?"
- "What's the difference between a purchase order and an invoice?"
- "How many working days are there between March 3 and March 24?"

##### Thinking-partner work

- "Rewrite my update below so the delay reads as a decision, not an apology."
- "Here's last quarter's review and the two slides leadership pushed back on. Restructure the story for this quarter."
- "I've pasted a customer's complaint thread below. Help me work out what they're actually asking for before I reply."

---

#### Key takeaway

**Use a search box when you need an answer.**

**Use Claude as a thinking partner when you need to work through a situation.**

The biggest difference is **context**:

- A search box takes a **question**.
- Claude can take the **situation**, work with your materials, reason through the problem, and collaborate with you toward an outcome.

---

#### Here's a few things Claude excels at

- **Writing and content creation**
  - Collaborates on:
    - Social media posts
    - Professional emails
    - Complex reports
  - Can take direction on **personality and tone**.
  - Allows you to iterate on:
    - Structure
    - Clarity
    - Tone
  - Helps ensure your **own voice** comes through clearly.

- **Research and analysis**
  - Helps you:
    - Explore research angles
    - Compile findings
    - Analyze data
    - Surface meaningful insights
  - You can upload documents and have Claude analyze complex information.
  - Claude's large context window allows it to work with extensive amounts of information in a single conversation.
  - Supports **200K+ tokens** (about 500 pages of text or more).
  - Up to **1M tokens** are available on Pro, Max, Team, and Enterprise plans when using supported models.

- **Coding assistance**
  - Coding is one of Claude's greatest strengths.
  - Claude can help you:
    - Write code
    - Debug code
    - Explain code
  - Supports real-world coding tasks across multiple programming languages.

- **Problem-solving and reasoning**
  - Can handle:
    - Complex cognitive tasks
    - Mathematical problems
    - Strategic thinking
    - Analysis
    - Research
  - Claude can respond near-instantly or take additional time to reason before answering.
  - This deeper reasoning capability is called **Thinking**.
  - When a problem requires careful analysis, Claude can work through it step by step before providing an answer.

- **Learning new things**
  - Can adapt to your:
    - Learning style
    - Pace
    - Level of knowledge
  - Useful for learning new skills, exploring unfamiliar domains, and working through complex challenges.
  - **Learning mode** guides your reasoning process instead of simply providing answers.
  - This can help develop **critical thinking skills**.

#### Further ways to explore Claude

- Explore Claude's **use-case gallery** to find ideas for applying Claude to your specific function.
- Take the **AI Capabilities** course for a deeper understanding of what AI can and cannot do.

---

### Ways to access Claude

Claude is the **intelligence—the AI assistant** you're learning to work with throughout this course. The same intelligence is available across multiple interfaces, each suited to different types of tasks.

- **Claude.ai**
  - Available through the web, mobile, and desktop apps.
  - The primary way most people interact with Claude.
  - Useful for:
    - Asking questions
    - Brainstorming ideas
    - Creating and editing documents
    - Writing assistance
    - Research
    - Analysis
    - Creating files
  - This is the **primary focus of this course**.

- **Claude Code**
  - An **agentic coding tool** designed primarily for developers.
  - Can also be used for file manipulation on your desktop.
  - Can:
    - Directly edit files
    - Run commands
    - Create commits

- **@Claude for Slack**
  - Brings Claude directly into **Slack**.
  - You can interact with Claude:
    - From the AI assistant header
    - By tagging `@Claude` in threads
  - When Slack is connected to Claude, it can search:
    - Workspace channels
    - Direct messages
    - Shared files
  - This allows Claude to find relevant context for better responses and research.

- **Claude Design**
  - A dedicated space for turning ideas into **working interfaces**.
  - You can:
    - Describe what you want
    - Start from a sketch
    - Start from a screenshot
  - Claude creates an interactive prototype that you can refine and hand off to your team.

- **Claude for Microsoft 365**
  - Brings Claude into:
    - Excel
    - PowerPoint
    - Word
    - Outlook
  - Works as a sidebar within these applications.
  - Allows you to:
    - Analyze content
    - Draft content
    - Edit documents
    - Carry context from one application to another

#### Course focus

- This course focuses primarily on **Claude.ai**.
- For development workflows, you can explore **Claude Code in Action** for more information on using Claude in coding and development.

---
