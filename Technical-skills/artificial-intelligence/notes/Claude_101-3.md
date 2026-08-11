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

