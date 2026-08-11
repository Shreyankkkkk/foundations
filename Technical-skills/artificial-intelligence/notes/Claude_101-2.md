# Source and attribution

These notes are my personal study notes based on Anthropic's Claude 101 course.

- Course: Claude 101
- Provider: Anthropic
- Source: https://anthropic.skilljar.com/
- Copyright: © 2025 Anthropic. All rights reserved.

## These notes are independently written summaries for educational and reference purposes and are not official Anthropic course materials.

# Organizing Your Work and Knowledge

---

## Lesson 1 : Introduction to Projects

### Learning Objectives

- Explain what projects are and when to use them
- Create a new project with a name, description, and visibility settings
- Add documents and files to your project's knowledge base
- Write effective project instructions to guide Claude's behavior
- Share projects with teammates (for Claude for Work (Team and Enterprise plan) users)

---

### Claude Projects

- **Projects** are self-contained environments with:
  - Their own chat histories
  - A project knowledge base
  - Custom project instructions/settings
- Project knowledge is automatically considered in chats within that project, providing Claude with relevant context.
- Projects can handle large amounts of information using **Retrieval-Augmented Generation (RAG)** when the project knowledge approaches the context-window limit.

### Creating a Project

1. Create a **New Project** and give it a name.
2. Describe the project's purpose and desired outcome.
3. Create the project.

Project options include:
- Star a project for quicker access
- Edit project details
- Archive or delete a project
- Set visibility to **private** or **public/team-accessible**

### Project Instructions

- Instructions apply to **every chat within the project**.
- They can specify:
  - Tone
  - Expertise level
  - Response style
  - Desired outcomes
  - Additional project context
- Project instructions work alongside user preferences and selected styles.

### Project Knowledge

- Files added to the project's knowledge base are available across **all chats within the project**.
- Supported sources include:
  - PDFs
  - Documents
  - CSVs
  - Text files
  - Google Drive
- Claude processes these files and uses them as context in project conversations.
- **Important:** Context from one chat is not automatically shared with other chats unless the information is added to the project knowledge base.
- Content can also be uploaded directly into an individual conversation without adding it to project knowledge. This is useful for temporary context or examples.

### Sharing & Permissions

Projects can be shared with other members for collaboration.

Permission levels:
- **Can view:** Can view project contents, access knowledge, and chat, but cannot make changes.
- **Can edit:** Can modify instructions, update knowledge, manage members, and contribute to the project.
- **Project creator:** Has full control over the project and its sharing/access settings.

Other collaboration features:
- **Shared with me** tab for finding projects shared with you
- Email notifications when a project is shared
- Multiple members can contribute documents and create chats

### Example Uses

Projects can be used for:
- **Product development:** Organize product information, generate ideas, track design evolution, and plan launches.
- **Content creation:** Generate ideas, assist with writing, and maintain consistency across platforms.
- **Education:** Organize course materials, explain complex concepts, and improve course content.
- **Personal finance:** Track financial goals, analyze spending, and plan budgets.
- **Home renovation:** Centralize project information, develop design ideas, manage budgets, and track decisions.

---

#### Video

[Delegation Diligence Loop — YouTube](https://www.youtube.com/watch?v=GJ5jTgcbRHA)

---

#### Key Takeaways

- **Projects are self-contained workspaces** with their own memory, chat histories, knowledge bases, and customized instructions. They are dedicated environments for specific work streams.
- **Project knowledge enhances Claude's understanding** by allowing relevant documents to be uploaded and referenced across all chats within the project.
- **Project instructions guide Claude's behavior** by defining tone, expertise level, response style, and other preferences. They apply to every conversation within the project.
- **Projects scale automatically.** When the knowledge base approaches context limits, Claude uses retrieval to search the project knowledge and pull in relevant information.
- **Projects enable collaboration** for Claude for Work users by allowing teammates to share the same context, instructions, and accumulated knowledge.

---

### What are Projects?

Projects are useful for:
- Storing knowledge Claude should reference
- Organizing related chats around a specific topic or work area
- Collaborating with team members who need access to the same shared context

### When to Use Projects

Projects are particularly useful for **ongoing work**, rather than one-off questions.

Create a project when you have:

- **Reference materials you'll use repeatedly**
  - Meeting notes
  - Survey results
  - Reports
  - Historical data
- **Consistent requirements** for how Claude should respond
  - Always use formal language
  - Always cite sources
  - Always follow a specific template
- **Team collaboration needs** where multiple people need to work from the same foundation

---

### Creating Your First Project

Setting up a project involves three main steps:

#### Step 1: Set Up Your Project

1. Open **Projects** from the left sidebar or go to `claude.ai/projects`.
2. Click **+ New Project**.
3. Give the project a descriptive name.
4. Add a brief description of the project's purpose.
   - This helps you and teammates understand the project but is not directly visible to Claude.
5. Choose the visibility:
   - **Private**
   - **Shared with your organization** (Claude for Work)

#### Step 2: Add Project Instructions

Project instructions tell Claude how to behave across **all conversations within the project**.

Useful instructions can include:

- **Context:** What the project is about.
- **Process:** How Claude should approach tasks.
- **Tone and style:** How Claude should communicate.
- **Specific requirements:** Rules Claude should consistently follow.

Example:
> "When I upload a meeting transcript, create a structured summary using this template."

Project instructions:
- Apply to every chat in the project.
- Work alongside user preferences and selected styles.
- Can be used to automate recurring workflows.

Think of project instructions as **programming Claude's behavior for that project**.

#### Step 3: Build Your Knowledge Base

The project knowledge base stores documents Claude should reference across project chats.

You can add content through the **Files** menu, including:
- PDF
- DOCX
- CSV
- TXT
- HTML
- Other supported file types
- Google Drive documents

Useful things to upload:
- Reference documents
- Brand/style guides
- Templates
- Research reports
- Meeting notes
- Requirements documents
- Examples of work you want Claude to emulate
- Technical documentation and specifications

**Pro tip:** Use descriptive file names so Claude can better identify and retrieve the relevant information.

Example:
- `Q4-2024-Brand-Guidelines.pdf` → useful
- `document1.pdf` → less useful

---

### How Projects Handle Large Knowledge Bases

Projects use **Retrieval-Augmented Generation (RAG)** to handle large amounts of content.

- Claude can automatically find and use the **most relevant parts** of uploaded documents without being told which file to use.
- When project knowledge approaches the **context window limit**, Claude stops loading everything at once and instead searches the project's files for relevant information.
- RAG can expand project capacity by **up to 10x** while maintaining response quality.
- A visual indicator shows when a project is **RAG-enabled**.
- The user experience remains the same: upload documents, chat with Claude, and receive context-aware responses.

---

### Working Within a Project

- Each conversation within a project automatically has access to the project's **knowledge base** and follows its **project instructions**.

#### Collaboration Features

Available on **Claude for Work (Team and Enterprise)** plans.

##### Permission Levels

1. **Can view:** Members can view project contents, access knowledge, and chat, but cannot make changes.
2. **Can edit:** Members can modify instructions, update knowledge, manage members, and contribute to the project.
3. **Owner:** Project creators have full control, including managing who can access the project and its visibility.

##### Sharing a Project

- Open the project and click **Share project**.
- Add individual members by name or email.
- Bulk-share by pasting a list of email addresses.
- Share with **Everyone at [your organization]** to make the project discoverable within the Team tab.
- Team members receive an **email notification** when a project is shared.
- Shared projects appear in the **Shared with me** section.

---

### Example Projects to Inspire You

- **Q4 product launch:** Upload product specs, competitive analysis, and messaging notes so Claude has the relevant context for drafts and questions.
- **Research support:** Centralize competitive reviews, user research, and customer feedback so Claude can synthesize sources and draft reports.
- **Client account hub:** Store brand guidelines, past deliverables, and communication history so Claude can match the client's tone and context.
- **Event planning workspace:** Upload venue contracts, speaker bios, and attendee data to help Claude create event documents and communications.
- **Job description generator:** Add past job descriptions, team charters, and headcount documents so Claude can draft roles that reflect your team's work and culture.

---

### Best Practices for Projects

- **Start focused, then expand:** Begin with a specific use case instead of creating one project for everything.
- **Keep the knowledge base current:** Regularly review and update documents to avoid outdated responses.
- **Write clear instructions:** Be specific about what you want to get more consistent results.
- **Name documents descriptively:** Use clear filenames (e.g., `Q4-2025-Sales-Report.pdf` instead of `report.pdf`) and group related files together.
- **Reference documents by name:** Mention specific documents in prompts to help Claude focus on the relevant information.

---

## Lesson 2 : Creating with Artifacts

### Learning Objectives

- Explain what artifacts are and when Claude creates them
- Share artifacts with colleagues and publish them publicly
- Troubleshoot common artifact issues

---

### What Are Artifacts?

- **Artifacts** are standalone, interactive outputs that Claude creates in a dedicated window alongside the conversation.
- They display content in a usable format instead of leaving long code or text buried in the chat.
- Examples include **working websites, interactive charts, and downloadable documents**.

#### When Claude Creates an Artifact

Claude automatically creates an artifact when the content:

- Is **significant and self-contained**, typically 15+ lines.
- Is likely to be **edited, iterated on, or reused**.
- Is **complex enough to stand on its own** without the surrounding conversation.
- Is something you'll likely want to **reference or use later**.

---

### Common Artifact Types

- **Documents:** Markdown and plain text for meeting notes, reports, project plans, blog posts, and other text-heavy content.
- **Code snippets:** Working code in languages such as Python, JavaScript, and C++. You can view, copy, or download the code.
- **HTML pages:** Complete web pages using HTML, CSS, and JavaScript in a single file. Useful for landing pages, forms, interactive demos, and prototypes.
- **SVG images:** Scalable vector graphics for logos, icons, illustrations, and other visual elements.
- **Mermaid diagrams:** Flowcharts, sequence diagrams, Gantt charts, org charts, and other diagrams that can be refined.
- **React components:** Interactive UI elements such as calculators, dashboards, games, and data visualizations with actual functionality.

> **Note:** Word documents, Excel spreadsheets, PowerPoint presentations, and PDFs are created through Claude's separate file creation capability, not as artifacts. They are returned as downloadable files.

---

### Creating Your First Artifact

- Create an artifact simply by **describing what you want**. Claude determines whether the output should be presented as an artifact.
- Examples:
  - Create a flowchart showing a customer onboarding process.
  - Build an interactive dashboard for monthly expenses.
  - Design a landing page for a productivity app.
  - Write a reusable project brief template.
- If Claude doesn't automatically create an artifact, explicitly ask:
  - "Create this as an artifact."
  - "Show me this in an artifact."

#### Using an Artifact

Artifacts appear in a **dedicated window** to the right of the conversation. You can:

- **Preview:** See how the artifact looks.
- **View code:** Inspect the underlying code.
- **Copy:** Copy the content for use elsewhere.
- **Download:** Save the artifact as a file to your computer.

---

### Sharing and Publishing Artifacts

- **Copy or download:** Use the copy or download buttons to save an artifact or share it through other channels.
- **Share within your organization:** Claude for Work (Team and Enterprise) users can share artifacts internally with colleagues. Shared artifacts require team authentication.
- **Publish publicly:** Free, Pro, and Max users can publish artifacts so anyone with the link can access them.
  - Only the selected artifact version becomes public; the conversation remains private.
  - Anyone can view and interact with the artifact without a Claude account.
  - Others can **remix** the artifact in their own Claude conversation and modify it.
  - Published artifacts are publicly accessible through their link.
  - Published artifacts are **not indexed by search engines**.
  - You can unpublish an artifact at any time by removing public access.

#### How to Publish

- Click **Share** or **Publish** in the upper-right corner of the artifact.

---

### Tips for Getting the Most from Artifacts

- **Be specific:** Clearly describe what you want the artifact to do and include important features or requirements.
- **Describe the end user:** Tell Claude who will use the artifact so it can make appropriate design choices.
- **Iterate incrementally:** Ask for one feature or change at a time to make it easier to identify issues and refine the result.
- **Request artifacts when needed:** If Claude responds in chat instead of creating an artifact, ask: "Please create that as an artifact."

---

## Lesson 3 : Working with skills

### Learning Objectives

- Explain what Skills are and how Claude uses them
- Identify Anthropic's built-in Skills for document creation
- Enable and manage Skills in your settings

---

### What Are Skills?

- **Skills** are folders containing instructions, scripts, and resources that Claude loads dynamically to improve performance on specialized tasks.
- Think of Skills as **expertise packages** that teach Claude how to complete specific tasks consistently and repeatedly.
- Skills already power capabilities such as creating:
  - Excel spreadsheets
  - PowerPoint presentations
  - Word documents
  - PDFs
- **Custom Skills** can also encode entire repeatable workflows, such as:
  - Quarterly variance analysis
  - Brand voice reviews
  - Compliance checklists
- The goal is to make Claude follow the **same rigorous process every time** for a specialized task.

---

#### Types of Skills

There are two main categories of Skills:

- **Anthropic Skills:** Created and maintained by Anthropic.
  - Enhance document creation for **Excel, Word, PowerPoint, and PDF** files.
  - Available to all paid users.
  - Claude automatically invokes them when relevant.

- **Custom Skills:** Created by you or your organization for **specialized workflows and domain-specific tasks**.
  - Apply company brand guidelines to presentations.
  - Structure meeting notes in a specific format.
  - Execute organization-specific data analysis workflows.

---

### Enabling Skills

- Skills are currently a **feature preview** for **Pro, Max, Team, and Enterprise** users.
- Skills require **Code execution and file creation** to be enabled because they use Claude's secure sandboxed computing environment.

#### How to Enable Skills

1. Go to **Settings > Capabilities**.
2. Turn on **Code execution and file creation**.
3. Scroll to the **Skills** section.
4. Toggle individual Skills on or off as needed.

#### Plan-Specific Settings

- **Enterprise:** Organization Owners must enable both Code execution and Skills in Admin settings before members can use them.
- **Team:** Skills are enabled by default at the organization level.

Once enabled, available Skills appear in Settings, including **Anthropic's built-in Skills** and any **custom Skills** you've uploaded.

---

### Using Skills in Practice

- You usually **don't need to select Skills manually**. Claude automatically chooses the relevant Skill based on your request.
- Examples of prompts that can invoke Skills:
  - Create an Excel spreadsheet with formulas.
  - Turn meeting notes into a PowerPoint presentation.
  - Generate a PDF report from data.
  - Build a financial model in Excel with scenario analysis.
- When Claude uses a Skill, it will indicate the Skill being used while working.
- The result can be a **downloadable file** that you can save to your computer or directly to **Google Drive**.

---

### Working with Your Actual Files

- Claude can work with your **actual files** in a contained environment to create updated versions.
- In **Chat**, Claude creates a **new version** of the document rather than editing the original in place.
- Supported file types include:
  - `.xlsx`
  - `.pptx`
  - `.docx`
  - `.pdf`
- Claude can:
  - Create and update slides
  - Analyze spreadsheets and data
  - Add suggested edits to documents
- Finished files can be **downloaded** or opened directly in **Google Drive**.
- To use these capabilities, Claude may require access to external data sources. When prompted, enable **Allow limited network access**.

---

### Security Considerations

- **Only install custom Skills from trusted sources.**
- **Anthropic's built-in Skills** are tested and maintained by Anthropic.
- **Custom Skills you upload** are private to your individual account.
- If installing a custom Skill from an external source, **review its contents before using it** so you understand what it does.
- Skills can include **executable code**, so treat them carefully.

---

### Creating Custom Skills

Custom Skills let you teach Claude your **specific workflows, brand guidelines, and ways of working** so Claude can automatically apply them whenever they're relevant.

The easiest way to create a custom Skill is through **conversation with Claude**. You don't need to write code or manually build the Skill's technical structure.

### How to Create a Custom Skill

1. **Start a new chat**
   - Tell Claude what Skill you want to create.
   - Example: "I want to create a Skill for writing quarterly business reviews."
   - Or: "I need a Skill that applies our brand guidelines to presentations."

2. **Answer Claude's questions**
   - Claude will ask about your workflow and what the Skill should accomplish.
   - It may ask:
     - What should the Skill do?
     - What makes a good output for this type of work?
     - When would you use this Skill?
     - Can you provide examples?

3. **Upload reference materials**
   - Provide materials that help Claude understand the workflow, such as:
     - Templates
     - Style guides
     - Brand assets
     - Examples of high-quality work

4. **Save the Skill**
   - Claude generates the properly structured Skill file.
   - Save the generated file and the Skill is ready to use.

### Managing and Improving Skills

- Find your available Skills in the **Customize** tab in the left sidebar.
- You can view and edit Skills **manually or through conversation with Claude**.
- Custom Skills appear alongside Anthropic's built-in Skills.
- Claude automatically invokes a relevant custom Skill when you work on a task it applies to; **you don't need to trigger it manually**.
- Skills can be improved iteratively:
  - Ask Claude to edit an existing Skill.
  - Claude updates the Skill files based on your instructions.

---

### Skills vs. Projects

Think of it simply:

- **Projects store knowledge.**
- **Skills perform tasks.**

#### Projects

- Act as **knowledge hubs** for information Claude needs to understand your work.
- Store reference materials such as:
  - Project specifications
  - Meeting notes
  - Research documents
- Uploaded knowledge is available across conversations within the project.
- Best for **long-term context, reference materials, and team collaboration**.

#### Skills

- Act as **procedural machines** that define how Claude should perform a task.
- Encode:
  - Specific steps
  - Order of operations
  - Methodology
- Best for **repeatable workflows, multi-step tasks, and consistent processes**.
- Examples:
  - Brand or legal guidelines
  - Blog drafting workflows
  - PDF creation

#### How They Work Together

Projects provide the **"what" (information)**, while Skills provide the **"how" (process)**.

A Skill can reference knowledge stored in a Project. For example, a customer call-prep Skill could use customer profiles stored in a Project's knowledge base.

| | Projects | Skills |
|---|---|---|
| **Purpose** | Store knowledge Claude references | Define processes Claude executes |
| **Best for** | Long-term context, reference materials, collaboration | Repeatable workflows, multi-step tasks, consistent methodology |
| **Persistence** | Knowledge available across all chats in the project | Instructions applied when the Skill is invoked |

#### Key Distinction

> **Project = what Claude needs to know**  
> **Skill = how Claude should do the work**

---