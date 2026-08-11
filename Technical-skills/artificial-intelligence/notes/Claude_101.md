# Source and attribution

These notes are my personal study notes based on Anthropic's Claude 101 course.

- Course: Claude 101
- Provider: Anthropic
- Source: https://anthropic.skilljar.com/
- Copyright: © 2025 Anthropic. All rights reserved.

## These notes are independently written summaries for educational and reference purposes and are not official Anthropic course materials.

# Meet Claude

---

## Lesson 1 : What is Claude

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

## Lesson 2 : Your First Conversation with Claude

### Learning Objectives

- Start a new conversation with Claude and navigate the interface
- Write effective prompts using clear, specific language
- Upload files and images to provide Claude with additional context
- Use follow-up messages to iterate and refine Claude's responses

---

### Getting started with Claude.ai

Claude is an **AI collaborator** that combines its intelligence with your context and expertise to help you work through complex tasks.

---

#### Navigating the Claude interface

The Claude interface provides several features for starting conversations, organizing work, and creating outputs.

- **Chats**
  - Create new conversations.
  - Return to previous conversations.

- **Projects**
  - Organize related conversations in one place.
  - Provide **persistent context** across conversations.
  - Add **custom instructions** to guide Claude's behavior.

- **Artifacts**
  - Turn ideas into shareable:
    - Apps
    - Tools
    - Content

- All interactions with Claude begin with a **prompt**.
- Your prompt, combined with the context you provide, influences Claude's response.
- Claude works best when you communicate naturally, clearly, and conversationally, similar to how you would communicate with a coworker.

---

#### Crafting effective prompts

A good prompt gives Claude enough information to understand **what you're trying to accomplish and how you want it done**.

##### 1. Set the stage

Provide the context Claude needs to understand the situation.

Include:

- Your role
- The project or situation
- Your objectives
- Relevant background information

##### 2. Define the task

Clearly explain **what you want Claude to do**.

For example:

- Write
- Analyze
- Build
- Summarize
- Research
- Transform

##### 3. Specify the rules

Explain how you want Claude to complete the task.

You can specify:

- Style
- Tone
- Format
- Constraints
- Examples to follow
- Sources or research requirements

##### Example of a structured prompt

For an investor pitch deck for a new indie streaming app:

- **Context:** Explain that the work is for an investor pitch deck.
- **Task:** Provide the relevant content and analysis.
- **Rules:** Use current web research with citations and structure the result as a professional report.

> **A strong prompt combines context + task + rules.**

---

#### Adding context to your conversations

Claude becomes more useful when you provide **specific context** related to your task.

You can upload relevant documents and background information directly into a conversation, such as:

- Company documents
- Project files
- Background research
- PDFs
- CSV files
- DOCX files
- Other supported file types

Providing this information helps Claude understand your specific situation rather than relying only on the prompt itself.

> **Context gives Claude the information it needs to tailor its response to your situation.**

---

#### Using search and tools

The **Search and tools** menu allows Claude to access additional sources of information and capabilities.

Examples include:

- **Web search**
  - Allows Claude to research current information.
  - Useful for things such as current market data.

- **Connected data sources**
  - Can provide access to information from services such as Google Drive.
  - Gives Claude additional context for your work.

- Claude can choose the appropriate available tool when solving a request.

---

#### Choosing the right Claude model

Claude offers different models with different capabilities.

##### Claude Opus

- Designed for the **most complex tasks**.
- A large-scale model with hybrid reasoning capabilities.
- Useful for tasks requiring extensive analysis.

**Example:**

- Multi-step financial analysis

##### Claude Sonnet

- Designed for **everyday use**.
- Recommended as the default choice.
- Balances capability, speed, and cost-effectiveness.
- Suitable for most common tasks and conversations.

> **Choose the model based on the complexity of the task.**

---

#### Extended thinking

**Extended thinking** allows Claude to spend more time reasoning through complex problems before responding.

- Particularly useful for:
  - Complex analysis
  - Difficult reasoning
  - Problems requiring careful consideration
- Can increase response latency.
- Usually unnecessary for simple questions and everyday conversations.

For straightforward tasks, start with **Sonnet with thinking mode off**. If the task requires deeper reasoning, you can switch models or enable thinking.

---

#### Research

**Research** allows Claude to conduct systematic, multi-angle investigations.

It can:

- Break complex questions into smaller research tasks.
- Explore many sources.
- Consider multiple perspectives.
- Produce comprehensive reports.
- Include citations in its findings.

Research can take approximately **5–45 minutes**, depending on the complexity of the investigation.

> Research allows Claude to handle detailed investigative work while you focus on other high-value tasks.

---

#### Continuous collaboration with Claude

Claude is most effective when you **continue the conversation** instead of treating each prompt as a one-off interaction.

Through continued communication, you can:

- Refine the result.
- Correct misunderstandings.
- Provide additional context.
- Communicate your preferences.
- Adjust the tone, structure, or level of detail.

The goal is to work collaboratively:

> **Claude brings AI intelligence. You bring the context and expertise that makes the work meaningful.**

---

#### Video

[Delegation Diligence Loop — YouTube](https://www.youtube.com/watch?v=0vZ_UVLhSQQ)

---

#### Key takeaways

- Claude is an **AI collaborator and thinking partner** that combines AI intelligence with your context and expertise.
- Communicate with Claude like you would with a **coworker**: naturally, clearly, concisely, and conversationally.
- Strong prompts generally include three elements:
  - **Setting the stage:** Provide your role, objectives, and relevant context.
  - **Defining the task:** Clearly explain what you want Claude to do.
  - **Specifying rules:** Define the desired style, tone, format, constraints, or examples.
- Providing **relevant files and background information** gives Claude the context it needs to produce more tailored responses.
- **Projects** help organize work by providing persistent context and custom instructions.
- **Artifacts** can turn ideas into shareable apps, tools, and content.
- Choose the appropriate **Claude model** for the task:
  - **Sonnet** for everyday tasks and a balance of capability, speed, and cost.
  - **Opus** for more complex tasks requiring greater reasoning capabilities.
  - **Extended thinking** for problems that benefit from deeper analysis.
- **Research** allows Claude to conduct systematic investigations across multiple sources and produce comprehensive, cited reports.
- Claude becomes more useful through **continued interaction** rather than one-off prompts, allowing you to refine results, provide feedback, and collaborate toward better outcomes.

---

### Starting your first conversation

When you open Claude.ai, you'll see a clean interface with a **text input area** at the bottom of the screen.

Your prompts can range from:

- Simple questions
- Brainstorming ideas
- Writing and editing
- Coding tasks
- Complex requests to create files

All interactions with Claude begin with a **prompt**, and the prompt combined with additional context influences Claude's response.

---

#### Writing effective prompts

The best way to communicate with Claude is similar to how you would communicate with a **coworker**:

- Naturally
- Clearly
- Concisely
- Conversationally

A strong prompt should give Claude enough information to understand both **what you need** and **how you want the task completed**.

##### 1. Setting the stage

Provide the context Claude needs to understand your situation.

Consider:

- What is your role?
- What are your objectives?
- What background information does Claude need to know?

##### 2. Defining the task

Clearly describe **what you want Claude to do**.

For example:

- Write
- Analyze
- Build
- Research
- Summarize

Be specific about the outcome you want.

##### 3. Specifying rules

Explain how you want Claude to approach and present the work.

You can specify:

- Style
- Tone
- Format
- Constraints
- Examples to follow
- Research or citation requirements

---

##### Putting it together

A strong prompt can combine all three elements:

> "I'm the marketing lead at an indie streaming startup, and we're preparing an investor pitch deck for Series A investors. Can you research the current state of the independent film streaming market and identify key trends, competitor positioning, and growth opportunities? Use current web research with citations and structure it as a professional report of up to 5 pages, with an executive summary, market analysis, competitive landscape, and growth opportunities."

**Breaking down the prompt:**

- **Setting the stage:** Establishes the user's role, the company context, and the objective.
- **Defining the task:** Specifies the research to perform and the areas to investigate.
- **Specifying rules:** Defines the research requirements, citation requirements, length, and report structure.

> **A strong prompt gives Claude the context, task, and rules it needs to produce a useful result.**

---

#### The 4D Framework for AI Fluency

The prompt framework is adapted from the **4D Framework for AI Fluency**, developed through research collaboration between Professor Rick Dakan of Ringling College of Art and Design and Professor Joseph Feller of University College Cork.

The framework identifies four core competencies for effective collaboration with AI:

- **Delegation**
- **Description**
- **Discernment**
- **Diligence**

These competencies support **efficient, effective, ethical, and safe** use of AI.

---

### Adding context

You can give Claude additional context about your work through **file uploads, connectors, and custom preferences**.

Providing relevant context helps Claude produce responses that are more specific and useful for your situation.

#### File uploads

Claude can analyze both **text and visual elements** in documents, including:

- Text
- Images
- Charts
- Graphics

Supported file types include:

- PDF
- DOCX
- CSV
- TXT
- PNG
- JPEG

#### Practical uses for file uploads

- Upload a document and ask Claude to **summarize the key points**.
- Share an image and ask Claude to **describe or analyze it**.
- Attach a spreadsheet and ask Claude to **identify trends or patterns** in the data.
- Upload code and ask Claude to **explain how it works or identify bugs**.

Once a file is uploaded, Claude automatically attempts to **parse its contents**. The file appears as an attachment in the conversation, allowing you to ask Claude questions about it.

#### Custom preferences

If you want Claude to consider specific preferences in **every conversation**, you can configure them in:

**Settings → General → "What personal preferences should Claude consider?"**

This allows you to provide persistent preferences that Claude can use across conversations.

---

### Iterating on Claude's responses

Conversations with Claude are designed to be **iterative**. Instead of trying to create the perfect prompt in one message, you can use a series of smaller prompts to guide Claude based on its responses.

#### Ask follow-up questions

Build on Claude's previous response by asking for:

- More detail
- A different perspective
- Clarification
- Expansion of a specific point

**Examples:**

> "Can you expand on the second point?"

> "That's helpful, but can you make it more concise?"

#### Provide feedback

Tell Claude what worked and what needs to change.

**Example:**

> "This is good, but the tone is too formal. Can you make it more conversational?"

This allows Claude to adjust its response based on your feedback.

#### Redirect or restart

If Claude misunderstands your request or goes in the wrong direction, **redirect the conversation** by clarifying what you actually meant.

**Example:**

> "Actually, I was asking about X, not Y. Let me clarify..."

If the conversation has accumulated too much irrelevant context, you can also **start a new chat** to refresh the context and approach the task from scratch.

#### Edit and resubmit prompts

You can click the **pencil icon** on one of your previous messages to edit and resubmit the prompt.

This is useful when you want to **refine the original request** rather than add another message to the conversation.

> **Key idea:** Don't treat Claude's first response as the final answer. Guide, correct, and refine the conversation until the result meets your needs.

---

### Personalizing Claude

Claude provides features that help it work more effectively for you over time by reducing the need to repeat your preferences and context.

#### Memory

**Memory** automatically saves useful context from your conversations, such as:

- Your role
- Preferences
- Past decisions
- Working style

This means you don't have to repeat the same information every time you start a new conversation.

**Example:**

> If you tell Claude that you work in marketing at a B2B company, Claude can remember that context for future conversations.

You can manage your memory at any time through **Settings**, including:

- Reviewing what Claude remembers
- Editing saved memories
- Deleting memories

Memory also **syncs across your devices**.

#### Styles

**Styles** allow you to customize how Claude communicates with you.

You can:

- Choose from preset styles, such as:
  - Concise
  - Formal
  - Explanatory
- Create a **custom style** by describing how you want Claude to write.

Once configured, your selected style applies automatically across your conversations.

> **Memory** helps Claude remember your context, while **Styles** control how Claude communicates with you.

---

## Lesson 3 : Getting Better Results

### Learning Objective

- Recognize common challenges when starting out with AI and use troubleshooting techniques to overcome them
- Define AI Fluency and know where to go to learn more about working with AI in a fluent way
- Explain how you might set up evals to better understand how Claude might perform with your unique workflows

---

### Common challenges and how to fix them

When working with Claude, the response may not always match your expectations. This is normal and provides an opportunity to **refine your prompt and approach**.

| Challenge                                   | What's happening                                                                                                    | How to fix it                                                                                                                     |
| ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| **Claude's response is too generic**        | The prompt doesn't provide enough context about your specific situation.                                            | Add details about your **audience, role, objectives, and constraints**.                                                           |
| **The response is too long or too short**   | Claude is guessing the appropriate level of detail.                                                                 | Specify the desired **length or level of detail**, such as "Keep this under 100 words" or "Give me a comprehensive analysis."     |
| **Claude didn't follow my format**          | Claude understood what you wanted but not how you wanted it presented.                                              | **Show rather than just tell**. Provide an example or explicitly describe the required structure.                                 |
| **Information sounds correct but is wrong** | Claude can sometimes generate plausible but incorrect information, particularly for specific facts or niche topics. | **Verify important information independently**. Ask Claude for sources or confidence levels, and use web search when appropriate. |
| **The tone isn't right**                    | Claude's default helpful and professional tone may not match your needs.                                            | Describe the desired tone in plain language and provide an **example** of the style you want.                                     |

#### Example: Adding context

Instead of:

> "Write an email about the project delay."

Provide more context:

> "Write an email to our enterprise client explaining that the software integration will be delayed by two weeks. They've been patient so far, but this is the second delay. Keep it professional but apologetic."

**Key idea:** The more relevant context and clear constraints you provide, the more tailored Claude's response can be.

---

### The iteration mindset

One of the most important habits when working with Claude is understanding that the **first prompt rarely produces a perfect result**.

Treat the initial prompt as the **start of a conversation**, not a one-shot request.

#### Treat first drafts as starting points

- Review Claude's response.
- Identify what is working and what needs improvement.
- Refine the response through additional prompts and feedback.
- Use each iteration to move closer to the desired result.

#### Give specific feedback

Specific feedback is more useful than vague instructions.

Instead of:

> "Make it shorter."

Try:

> "Cut the first two paragraphs and make the conclusion more action-oriented."

Specific feedback gives Claude a clearer direction for the next iteration.

#### Know when to start fresh

If a conversation has gone significantly off track, it may be more efficient to **start a new chat** with a clearer prompt.

Rather than spending multiple messages trying to redirect an increasingly confused conversation, reset the context and explain the task again.

> **Key idea:** Treat Claude's first response as a draft. Review, give specific feedback, iterate, and start fresh when necessary.

---

### What is AI Fluency?

**AI Fluency** is the ability to collaborate effectively with AI tools. It goes beyond knowing how to use AI features and involves developing the **judgment and skills to use AI effectively across different situations**.

### The 4D Framework for AI Fluency

The **4D Framework for AI Fluency** was developed through research collaboration between Professor Rick Dakan of Ringling College of Art and Design and Professor Joseph Feller of University College Cork.

It identifies four core competencies:

#### Delegation

Deciding **what work should be done by humans, what should be done by AI, and how to divide tasks between them**.

This involves:

- Understanding your goals.
- Understanding AI capabilities and limitations.
- Making strategic decisions about how humans and AI should collaborate.

#### Description

Effectively **communicating with AI systems**.

This includes:

- Clearly defining desired outputs.
- Guiding AI through a task.
- Specifying desired behaviors and interactions.

#### Discernment

**Critically evaluating AI outputs and processes**.

This involves assessing:

- Quality
- Accuracy
- Appropriateness
- Areas that need improvement

#### Diligence

Using AI **responsibly and ethically**.

This includes:

- Making thoughtful choices about AI systems and interactions.
- Maintaining transparency about AI-assisted work.
- Taking accountability for the final result.

### Applying the 4D Framework

The course has already introduced several of these competencies:

- The **prompt framework** from Lesson 2 — setting the stage, defining the task, and specifying rules — is rooted in **Description**.
- The troubleshooting techniques from this lesson draw on **Discernment** and **Diligence**.
- Deciding when Claude should act as a thinking partner versus when a search box is sufficient involves **Delegation**.

> **AI Fluency is not just knowing how to use AI. It's knowing how to collaborate with AI effectively, critically, and responsibly.**

---

### Evaluating Claude for Your Workflows

As you start using Claude for recurring tasks, **evaluations (evals)** help you determine how well Claude actually performs for your specific workflow. Evals are a systematic way to test Claude's outputs and build better judgment about when and how to use it.

#### Why Evals Matter

Every workflow is different. Claude may perform extremely well on one type of task but require more context, examples, or human review for another.

Evals can help you:

- Identify where Claude provides the most value
- Find tasks where Claude needs additional context or examples
- Build confidence in Claude's outputs for recurring workflows
- Determine where human review is still necessary

#### A Simple Eval Process

You don't need a complex evaluation system to get started. A basic eval can be done in four steps:

1. **Gather examples** — Collect 5–10 examples of a task you regularly perform, such as emails, reports, analyses, or other work.
2. **Create test prompts** — Write prompts that ask Claude to perform the same type of task using the context you would normally provide.
3. **Compare outputs** — Evaluate Claude's responses against your existing examples and ask:
   - Did Claude capture the important information?
   - Is the tone and style appropriate?
   - What is missing or could be improved?
4. **Refine your approach** — Use the results to improve your prompts, provide better examples, or identify situations where human review is essential.

Evals turn your experience with Claude from **"it seems good"** into a more systematic understanding of where Claude performs reliably and where it needs additional guidance.

---

### Delegation diligence loop

The **delegation diligence loop** is a systematic way to determine whether AI can reliably perform a specific analytical task. Instead of blindly trusting AI-generated results, test its performance against data and analyses you already understand.

#### Why it matters

- AI can be useful for data analysis, but its outputs should not automatically be treated as correct.
- Testing AI on known data helps identify:
  - Where AI performs reliably
  - Where additional context or instructions are needed
  - Where AI has capability gaps
  - Which tasks should or should not be delegated
- The goal is to build **validated confidence**, rather than relying on assumptions about what AI can do.

#### The delegation diligence loop

1. **Identify a task to delegate**
   - Choose a specific analytical task that you perform regularly.
   - Be clear about what you want AI to handle and what you want to retain responsibility for.

2. **Use known data**
   - Find historical data where the analysis has already been completed.
   - Make sure you know what the correct results should be so you can evaluate AI's output.

3. **Reproduce the analysis with AI**
   - Provide the necessary data, context, and instructions.
   - Ask AI to perform the same analysis.

4. **Evaluate the output**
   - Compare AI's results against the known results.
   - Check both the final conclusions and how AI arrived at them.
   - Look for missing information, incorrect assumptions, or gaps in reasoning.

5. **Refine the delegation**
   - If AI makes mistakes, determine whether additional context or clearer instructions can fix the issue.
   - Add the necessary information to future prompts.

6. **Test again**
   - Repeat the process after refining the approach.
   - If AI consistently produces reliable results, you have a validated workflow.
   - If repeated refinement does not resolve the problems, the task may not be suitable for delegation.

#### Validation builds confidence, not responsibility

- Validating AI's performance does **not** remove human responsibility.
- Continue checking whether results make sense when working with new data.
- Remain accountable for the final analysis and decisions.
- Be transparent about AI's involvement when appropriate.

#### Using AI when you're not a data expert

AI can also help users who are less comfortable with data analysis by:

- Writing or explaining spreadsheet formulas
- Cleaning and reformatting messy data
- Brainstorming analytical approaches
- Explaining possible solutions step by step
- Helping implement analytical workflows

When using AI this way, continue asking for explanations and clarifications so that you understand the process rather than blindly accepting the output.

#### General principle

> **Test first → Validate → Refine → Test again → Delegate with confidence**

The same approach can be applied to many recurring analytical tasks, including forecasting, survey analysis, reporting, budgeting, and data-driven decision-making.

#### Video

[Delegation Diligence Loop — YouTube](https://www.youtube.com/watch?v=Zzn-g8lvLMA)

---

#### Applying the evaluation approach

To evaluate how Claude performs on a recurring data task:

1. Find a dataset you have already analyzed manually.
2. Create prompts asking Claude to perform the same analysis.
3. Compare Claude's results with your original analysis.
4. Identify patterns in what Claude gets right or wrong.
5. Refine your prompts and repeat the evaluation.

This lightweight evaluation builds intuition about where Claude works well, where it needs additional guidance, and where human review should be focused.

---

## Lesson 4 : How you'll work with Claude on your desktop

### Learning Objectives

- Distinguish the ways you work with Claude on the desktop — working with Claude turn by turn, handing whole tasks off for Claude to run, and building software in your codebase
- Recognize which shape of work a task calls for before you start it
- Find where each way of working lives in the desktop app today

---

### Working with Claude on your desktop

Claude's desktop app supports three main ways of working, each suited to a different type of task.

#### Three ways of working with Claude

- **Working with Claude, turn by turn**
  - You and Claude collaborate through an ongoing conversation.
  - You provide a request, review the response, give feedback, and guide subsequent revisions.
  - The work develops through the back-and-forth interaction.

- **Handing work off to Claude**
  - You describe the desired outcome rather than manually directing every step.
  - Claude can plan and execute the work, then return the completed result for you to review.
  - Useful for tasks where you care more about the final outcome than managing each individual step.

- **Building software with Claude Code**
  - Claude works directly within a codebase.
  - It can read and modify code, run commands, and test changes.
  - Primarily designed for developers and software development workflows.

#### Where each workflow happens

| Workflow | Claude desktop location |
|---|---|
| Turn-by-turn collaboration | **Chat** |
| Handing work off to Claude | **Cowork** |
| Building software | **Code** |

The key distinction is **how much of the work you are directly coordinating**: Chat is collaborative and iterative, Cowork allows Claude to take ownership of a larger task, and Claude Code works directly with software projects.

---

