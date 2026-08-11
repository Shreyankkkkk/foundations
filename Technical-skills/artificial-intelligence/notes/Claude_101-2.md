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

