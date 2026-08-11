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