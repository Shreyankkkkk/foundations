# Source and attribution

These notes are my personal study notes based on Anthropic's Claude 101 course.

- Course: Claude 101
- Provider: Anthropic
- Source: https://anthropic.skilljar.com/
- Copyright: © 2025 Anthropic. All rights reserved.

## These notes are independently written summaries for educational and reference purposes and are not official Anthropic course materials.

# Expanding Claude's reach

---

## Lesson 1 : Connecting your Tools

### Learning Objectives

- Explain what connectors are and why they matter for your work with Claude
- Navigate the connectors directory and set up your first connection
- Use connected tools effectively in your conversations with Claude

---

### What Are Connectors?

- **Connectors turn Claude into an informed collaborator** by giving it access to the tools, data, and context you already use.
- They allow Claude to work with your **actual information** instead of starting each conversation from scratch.

#### What Connectors Can Do

Depending on the connector and permissions, Claude can:

- Search files and retrieve documents
- Analyze data
- Create content
- Update records
- Execute tasks across connected applications

#### Model Context Protocol (MCP)

- **MCP (Model Context Protocol)** powers connectors.
- Think of MCP as **"USB-C for AI"** — a universal standard for connecting Claude to different applications through a consistent interface.
- Developers can build connectors for different tools using this open standard.

#### Types of Connectors

- **Web connectors:** Connect Claude to cloud services such as Google Drive, Notion, Slack, and Asana.
- **Desktop extensions:** Run locally through the Claude Desktop app, giving Claude access to local files and native applications.

---

#### Connector Directory

- Anthropic maintains a directory of recommended connectors at `claude.ai/directory`.
- The directory has two categories:
  - **Web:** Cloud services and applications such as Gmail, Notion, Slack, Asana, Linear, and Stripe.
  - **Desktop extensions:** Local tools that run through the Claude Desktop app.
- You can also browse connectors directly in Claude by clicking **+** in the lower-left of the chat window and selecting **Connectors**.

---

### Setting Up a Web Connector

1. **Find the connector:** Go to `claude.ai/directory`, or click **+ > Connectors** in a chat.
2. **Connect:** Select the cloud service you want to add.
3. **Authenticate:** Sign in through the service's login page using your existing credentials.
4. **Grant permissions:** Review the permissions Claude is requesting and authorize access.
5. **Test the connection:** Return to Claude and make a simple request to confirm the connection works.

Once connected, Claude can **search, read, and sometimes take actions** within the service, depending on the permissions granted.

---

### Desktop Extensions

- **Desktop extensions** work through the Claude Desktop app rather than the web interface.
- They let Claude interact with **local applications, your file system, and native features** on macOS or Windows.
- Examples include:
  - **Local file access** — read and organize documents.
  - **Browser control** — automate web-based tasks.
  - **Native app integrations** — such as Figma for design work.

#### Installing a Desktop Extension

1. Download and install the [Claude Desktop app](https://claude.ai/download).
2. Open Claude Desktop and go to **Settings > Extensions**.
3. Browse the available extensions and click **Install**.
4. Complete any additional setup required by the specific extension.

---

### Using Connectors in Your Work

Once your tools are connected, Claude can use them when responding to your requests.

#### Common Uses

- **Project management (Asana, Linear, Jira)**
  - Find high-priority tasks and deadlines.
  - Create new tasks.
  - Summarize project status.

- **Communication (Slack, Gmail)**
  - Find relevant email threads.
  - Draft replies to messages.
  - Recall decisions from team discussions.

- **Documentation (Notion, Google Drive, Confluence)**
  - Search internal documentation and guidelines.
  - Summarize meeting notes and other documents.
  - Answer questions using your organization's reference material.

- **Business tools (Stripe, PayPal, Salesforce)**
  - Analyze revenue and transaction trends.
  - Check customer or sales opportunity status.
  - Find transactions matching specific criteria.

**Key idea:** Connectors let Claude work with information and tools you already use, so you can ask questions or perform tasks across those services from within Claude.

---

### Security and Permissions

- **Scoped access:** Connector permissions are limited to what the connector needs. You can enable or disable individual permissions within the application's settings.
- **Claude sees what you see:** Claude can only access information that your own account has permission to access. Connecting your work email, for example, does not give Claude access to someone else's inbox.
- **Revocable access:** You can disconnect a connector through Claude's settings or through the connected service's security settings.
- **Trusted sources:** Custom connectors can be built or installed, so only use connectors from sources you trust.

---

## Lesson 2 : Enterprise Search

### Learning Objective

- Explain what Enterprise Search is and the types of questions Enterprise Search can answer
- Understand how the setup process works for both admins and users
- Recognize how security and permissions protect organizational data

---

### What is Enterprise Search?

- **Enterprise Search** adds an **"Ask {Your Org Name}"** option to the Claude sidebar.
- It is designed to **find and synthesize knowledge across your company's tools and data sources**.
- Think of it as a **pre-built project for the entire organization**, with the company's knowledge already connected.
- It provides **context-aware answers** based on organizational information.
- Unlike regular chats with connectors, **Enterprise Search is specifically focused on information gathering** and uses custom instructions configured by Anthropic.

---

### What Can You Ask?

Enterprise Search is useful for questions that **span multiple sources** or require Claude to **synthesize information across your organization**.

#### Common Use Cases

- **Getting up to speed**
  - Summarize what happened while you were away.
  - Get key updates from across the business.
  - Identify current project blockers.

- **Policy and process questions**
  - Find company policies and procedures.
  - Learn how to submit expenses or request time off.
  - Get answers from internal documentation.

- **Research and analysis**
  - Identify customer feedback and competitor-related insights.
  - Summarize discussions around product roadmaps.
  - Find and synthesize information about internal processes.

- **Onboarding**
  - Learn how internal systems work.
  - Find the right people to contact about specific systems.
  - Understand the tools and processes used by different teams.

- **Performance and project tracking**
  - Find discussions and documents related to a project or campaign.
  - Summarize decisions from meetings.
  - Track team contributions to an initiative.

#### How It Works

- Claude searches across connected sources such as **SharePoint, Slack, Gmail, and Google Drive**.
- It **combines and synthesizes information** from multiple sources into one response.
- Claude **cites its sources**, allowing you to verify the information and explore the original context.

---

### Setting Up Enterprise Search

Enterprise Search has a **two-step setup**: an admin configures it for the organization, then individual users authenticate their own accounts.

#### For Admins (Owners)

- Enterprise Search is enabled by default for **Team and Enterprise** organizations, but an Owner must complete the initial setup.
- Setup steps:
  1. Click **"Ask Your Org"** in the left sidebar.
  2. Click **"Set up for your org"** to continue, or **"Disable"** to turn it off.
  3. Connect the organization's tools:
     - **Documents:** Google Drive, SharePoint, etc.
     - **Chat:** Slack, Microsoft Teams, etc.
     - **Email:** Recommended but optional.
  4. Click **"+ Add more"** to connect additional tools.
  5. Customize the project name, which appears as **"Ask [Name]"** in everyone's sidebar.
  6. Add a description and click **"Finish set up."**
- Once setup is complete, Enterprise Search becomes available to everyone in the organization.

#### For Users

- After setup, the **"Ask {Org Name}"** project appears starred in the sidebar.
- To get started:
  1. Open the project.
  2. Follow the guided onboarding flow.
  3. Authenticate with the services you want Claude to search, such as Slack, Google, or Microsoft 365.
  4. Start asking questions about your organization's knowledge.
- **More connectors = more comprehensive search results.**
- Additional connectors can be added later through **Connect** in the project's Instructions section.

---

### Is Enterprise Search Safe?

- Enterprise Search only shows information you already have permission to access in the original connected tools.
- Your conversations remain private.
- Connected data is **not separately indexed or stored** by Enterprise Search.

### Lesson Reflection

- What questions do you regularly ask colleagues that could instead be answered by searching company documents and communications?
- Could Enterprise Search help with onboarding or training new team members?
- Which data sources would be most valuable to connect for your role?

---

## Lesson 3 : Research for deep dives

### Learning Objectives

- Explain what Research does: systematic, multi-source investigation
- Identify when to use Research for comprehensive information gathering
- Understand how Research uses Thinking to plan its approach before it gathers information
- Write effective Research prompts for complex investigations

---

### Researching with Claude

- **Research is more than a single search.** Claude searches agentically, conducting multiple searches that build on each other and exploring different angles of a question.
- **Research takes longer than a normal search.** Complex questions may take several minutes because Claude can run many searches across hundreds of sources and synthesize the findings.
- **Research works with Thinking.** Claude can plan how to approach a complex question, break it into smaller parts, and then research each part.
- **Citations make verification easier.** Research provides citations so you can check the sources and verify Claude's findings.

---

### What is Research?

- **Research turns Claude into a systematic investigator**, rather than just a conversational assistant.
- When enabled, Claude:
  - Explores a question from **multiple angles**.
  - Searches across the **web and connected integrations**.
  - Cross-references information from different sources.
  - Synthesizes findings into a **comprehensive response**.
- Think of it as a **research assistant** that gathers and compares information while you work on something else.
- Research is most useful when a question requires:
  - **Multiple sources**
  - **Different perspectives**
  - **Cross-referencing**
  - **Synthesis into actionable insights**
- It is better suited to **thorough research** than quick, straightforward questions.

---

### When to Use Research

The main pattern to remember:

> **Multi-source synthesis → Research**  
> **Single facts → Web search**  
> **Pure reasoning → Thinking**  
> **Company-specific questions → Enterprise Search**

#### Use Research When You Need

- Comprehensive reports that synthesize information from **multiple sources**.
- In-depth analysis across the **web and connected integrations** such as Google Workspace.
- Thorough investigations that would normally take **hours of manual work**.
- **Comparative analysis**, such as evaluating competitors or vendors.
- Reports with **citations** that you can verify.

#### Good Use Cases

- Market analysis and competitive research.
- Planning complex projects such as team offsites or product launches.
- Synthesizing information from email, calendars, and documents.
- Creating technical documentation using multiple sources.
- Preparing briefings that require **current, verified information**.

#### Use Web Search Instead When

- You need a **quick, specific fact**.
- The answer only requires **one or two sources**.
- **Speed matters more than comprehensiveness**.

#### Use Thinking Instead When

- You need deep reasoning on a complex problem that **doesn't require external information**.
- You're working on mathematics, code debugging, or logical analysis.
- The answer comes primarily from **reasoning through the problem**, rather than gathering information.

#### Use Enterprise Search Instead When

- You need answers from your **organization's internal knowledge**, such as documents, Slack, emails, or meeting notes.
- You're onboarding and need to find company-specific **policies, processes, or past decisions**.
- The question is specific to **your company**, rather than information available on the public web.

---

### How Research Works

Research uses an **agentic, multi-step process** that goes beyond a simple web search. Claude decides what to investigate next based on what it has already found, pursuing leads and filling gaps automatically.

1. **Plan the approach**
   - Claude breaks down your request.
   - Identifies what information it needs.
   - Plans how to investigate the different aspects of the question.

2. **Conduct multiple searches**
   - Claude performs many searches instead of a single lookup.
   - Searches build on one another.
   - Claude uses previous findings to decide what to investigate next.
   - It pursues useful leads and fills information gaps.

3. **Synthesize findings**
   - Claude combines information from multiple sources.
   - Sources can include the **web and connected integrations** such as Gmail, Google Calendar, and Google Drive.
   - Findings are compiled into a **comprehensive, organized report**.

4. **Provide citations**
   - Research reports link claims back to their sources.
   - This makes it easy to **verify information and investigate sources further**.

---

### Using Research in Practice

1. Click the **+** button in the bottom-left of the chat interface.
2. Select **Research** from the menu. It will appear highlighted when active.
3. Enter your prompt and submit it.
4. Claude will work in the background while searching and analyzing. Progress indicators show its activity.

> **Important:** Web search must be enabled for Research to work. You can enable it from the same **+** menu.

---

### Tips for Effective Research Prompts

Since Research can take **minutes rather than seconds**, spending time on the prompt helps improve the quality and relevance of the results.

- **Be specific about your goal**
  - Clearly state what you want to learn, analyze, or decide.
  - Avoid broad prompts when you need a focused investigation.

- **Specify the structure you want**
  - Tell Claude which sections, categories, or comparisons to include.
  - Claude will organize its research around the structure you provide.

- **Include relevant constraints**
  - Provide important limits such as:
    - Budget
    - Timeline
    - Geographic requirements
    - Other criteria or parameters
  - Constraints help Claude focus on relevant information.

- **Ask Claude to refine your prompt**
  - If you're unsure how to frame the research question, ask Claude to help improve the prompt **before enabling Research**.

---

### Working with Connected Integrations

- Research becomes more powerful when **Google Workspace or other integrations** are connected.
- Claude can combine information from your:
  - Emails
  - Calendar
  - Documents
  - Other connected tools
  - The web
- This allows Claude to **combine internal context with external research** in one investigation.

#### Examples

- Combine discussions from emails and Slack with research on industry best practices.
- Review upcoming calendar meetings and research the companies you'll be meeting with.
- Find internal documents about a topic and compare them with external competitor information.

#### Steering Research with Integrations

You can explicitly tell Claude where to look, for example:

- "Pull relevant context from my Google Drive."
- "Include insights from my recent emails on this topic."

### Lesson Reflection

- What tasks in your work require gathering information from multiple sources?
- How could combining Research with connected integrations change your workflow?
- What's a complex research question you've been avoiding because it would take too much time to investigate manually?

---