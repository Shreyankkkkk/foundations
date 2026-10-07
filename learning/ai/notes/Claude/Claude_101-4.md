# Source and attribution

These notes are my personal study notes based on Anthropic's Claude 101 course.

- Course: Claude 101
- Provider: Anthropic
- Source: https://anthropic.skilljar.com/
- Copyright: © 2025 Anthropic. All rights reserved.

## These notes are independently written summaries for educational and reference purposes and are not official Anthropic course materials.

# Putting it all Together

---

## Lesson 1 : Claude in Action - use case by role

### Learning Objectives

- Describe 2-3 use-cases for claude.ai that you can try right away
- Know where to go to find additional use-case inspiration

---

### General Professional Use

Claude can streamline work across many roles and industries. The **Use Case Gallery** provides practical, role-relevant examples with detailed, step-by-step guides for applying Claude to common tasks.

#### Common Use Cases

- **[Generate project status reports](https://claude.com/resources/use-cases/generate-project-status-reports)** — Create clear, consistent project updates that keep stakeholders informed about progress and key developments.
- **[Analyze patterns in user feedback](https://claude.com/resources/use-cases/analyze-patterns-in-user-feedback)** — Analyze customer comments and survey responses to identify recurring patterns, themes, and useful insights.
- **[Package your brand guidelines in a Skill](https://claude.com/resources/use-cases/package-your-brand-guidelines-in-a-skill)** — Turn your brand standards into a reusable Claude Skill so they can be applied consistently across relevant work.

---

#### Sales

Claude can help sales teams prepare for deals, organize competitive intelligence, and turn pipeline data into useful reports.

- [Build a battle card library](https://claude.com/resources/use-cases/build-a-battle-card-library) – Create reusable competitive intelligence resources to help the sales team handle competitors and win deals.
- [Prepare for sales deals](https://claude.com/resources/use-cases/prepare-for-sales-deals) – Research prospects before meetings and organize relevant talking points.
- [Create sales reports](https://claude.com/resources/use-cases/create-sales-reports) – Turn pipeline and sales data into clear, actionable reports.

#### Marketing

Claude can help marketers analyze campaign results and adapt existing content for different audiences and channels.

- [Analyze campaign performance](https://claude.com/resources/use-cases/analyze-campaign-performance) – Analyze campaign metrics and identify insights that can inform future strategy.
- [Adapt content across platforms](https://claude.com/resources/use-cases/adapt-content-across-platforms) – Repurpose existing content for different platforms, formats, and audiences without starting from scratch.

#### Finance

Claude can work with financial data and spreadsheets to help build models, write analyses, and understand complicated existing files.

- [Build financial models](https://claude.com/resources/use-cases/build-financial-models) – Create and refine financial projections and models with Claude's help.
- [Draft investment memos](https://claude.com/resources/use-cases/draft-investment-memos) – Structure research and financial analysis into clear investment memos.
- [Understand and extend an inherited spreadsheet](https://claude.com/resources/use-cases/understand-and-extend-an-inherited-spreadsheet) – Analyze an unfamiliar spreadsheet, understand how it works, and add new functionality.

#### HR

Claude can help HR teams create structured documentation and improve the onboarding experience.

- [Create new hire onboarding guides](https://claude.com/resources/use-cases/create-new-hire-onboarding-guides) – Create comprehensive onboarding materials tailored to different roles and new employees.

#### Legal

Claude can help legal teams organize large amounts of information and identify patterns across complex documents.

- [Track discovery timelines and analyze patterns](https://claude.com/resources/use-cases/track-discovery-timelines-and-analyze-patterns) – Organize case timelines and analyze legal documents to identify important patterns.

#### Research

Claude can support researchers with planning, analysis, and verification of research work.

- [Plan your literature review](https://claude.com/resources/use-cases/plan-your-literature-review) – Structure a systematic approach to finding and reviewing relevant academic sources.
- [Verify statistics from raw data](https://claude.com/resources/use-cases/verify-statistics-from-raw-data) – Use Claude to double-check calculations and statistical analyses against the underlying data.

---

## Lesson 2 : Other ways to work with Claude

### Learning Objectives

- Understand when to use additional Claude products including Claude Code, @Claude, Claude Design, Claude for Microsoft 365, and Claude in Chrome

---

### Other ways to work with Claude

Claude is an intelligence, while Claude.ai is just one interface for working with it.

Claude is also available through specialized tools designed around different workflows and environments. These give you ways to use Claude where you already work, rather than always going back to the main Claude.ai interface.

This lesson covers the additional ways Claude can be used and when each option is most useful.

---

### Claude Code

Claude Code is an agentic coding tool that works directly in your development environment — including the terminal, IDE, browser, and Slack. It can understand a codebase, execute commands, modify files, run tests, and handle larger development workflows through natural language.

#### When to use Claude Code

- **Build features:** Describe what you want in plain English and Claude can write the code, run tests, and create commits.
- **Debug problems:** Give Claude an error message and it can inspect the codebase, identify the cause, and make fixes.
- **Understand unfamiliar codebases:** Ask Claude how different parts of a project work together instead of manually tracing everything.
- **Automate repetitive development tasks:** Useful for fixing lint errors, resolving merge conflicts, generating release notes, and similar work.
- **Work in your existing environment:** Claude Code is useful if you prefer staying in your terminal and IDE rather than switching to a separate interface.

---

### AI Core Overview

**#Anthropic #Claude #AIProductivity #TeamCollaboration #SoftwareDevelopment #Security #WorkflowAutomation**

Anthropic presents Claude Tag, a new way for Claude to collaborate directly with teams inside shared channels. The demo shows Claude following live product discussions, opening pull requests, making code changes, and keeping different teams aligned while respecting strict per-channel permissions, memory boundaries, and access controls.

### Key takeaways

- **Claude can collaborate directly inside team channels.** Teams can tag Claude into ongoing conversations, allowing it to follow discussions and act on decisions as they happen.
- **Claude can take action, not just answer questions.** In the demo, Claude understands the requested feature, finds the relevant part of the codebase, opens a pull request, and lands the change.
- **Claude uses the context of each channel.** It understands what the team is working on and can build memory over time as work happens.
- **Permissions are scoped by team and channel.** Claude only has access to the systems and information that have been explicitly made available in that context.
- **Claude cannot act outside its permissions.** For example, Claude in a legal channel can access contract information, while Claude in an engineering channel can edit the codebase. If Claude is asked to edit code from a legal channel where it has no code access, it cannot do so.
- **Memory follows the same boundaries.** Information Claude learns in a private channel or DM stays within that context rather than becoming available everywhere.
- **Claude has its own account and credentials.** Actions are performed through Claude's own permissions rather than pretending to be a human team member.

### Permissions and safety

- Claude can make edits itself using its own accounts and permissions.
- Access is granted per team and per channel, keeping sensitive systems separated.
- Claude cannot access systems that aren't available to the channel where it is being used.
- Memory boundaries match permission boundaries, so private information remains contained.
- The overall idea is to let Claude become part of the team's workflow while maintaining strict access controls.

### Main idea

Claude Tag is an example of moving Claude from a separate assistant that you ask for help into an **active team collaborator** that can follow conversations, understand context, take actions, and continue work across connected systems.

The important principle is that this only works safely when **context, permissions, and memory are properly scoped**.

---

#### Video

[Delegation Diligence Loop — YouTube](https://www.youtube.com/watch?v=GJ5jTgcbRHA)

---

### @Claude in Slack

@Claude brings Claude directly into Slack, allowing you to work with Claude inside channels and threads or bring Slack context into your Claude conversations. You can tag **@Claude** in a thread to bring it into the discussion.

#### When to use @Claude

- **Draft and summarize messages:** Draft replies, summarize long threads, or break down complex discussions without leaving Slack.
- **Prepare for meetings:** Have Claude pull together relevant Slack conversations and shared documents from your workspace.
- **Get up to speed:** When joining a new team, use Claude to review channel history and understand ongoing projects and discussions.
- **Hand off coding tasks:** Tag @Claude from a bug report or feature discussion and it can use the surrounding context to start a Claude Code session.
- **Get quick answers:** Ask about industry trends, technical concepts, or company information while staying inside the conversation.

---

### Claude for Excel

**#Claude #Excel #SpreadsheetAutomation #DataAnalysis #FinancialModeling #ScenarioPlanning #PivotTable #AIProductivity**

Claude for Excel works directly inside Excel workbooks as an AI assistant. It can help users understand unfamiliar spreadsheet models, trace and fix formula errors, run scenarios, create pivot tables and charts, and add new calculations while maintaining references to existing assumptions.

The example uses an HR headcount planning model to demonstrate how Claude can understand the relationships between multiple tabs, diagnose errors, update assumptions, create visualizations, and extend the model.

### Understanding an unfamiliar workbook

- Claude can **walk through the structure of a workbook** and explain what each tab contains and how the tabs connect.
- Rather than simply listing the sheets, it can explain the **data flow** between them.
- In the example, Claude identifies the flow from:
  - **Assumptions** → central model inputs
  - **Headcount** → uses those assumptions
  - **Compensation** → builds on the headcount information
  - **Summary** → rolls the results up
- This can help someone who inherited a complex model understand it without manually tracing every sheet and formula.

### Diagnosing and fixing errors

- Claude can identify errors while analyzing the workbook.
- In the example, it finds a `#REF!` error in the Headcount tab and identifies the specific cell containing the problem.
- The user asks Claude to diagnose and fix the error.
- Claude traces the broken reference and recommends a correction.
- When given permission to use its best judgment, Claude sets the planned hires value to `0`.
- The correction then **cascades through the rest of the workbook**, removing the resulting reference errors and updating dependent calculations.

### Running scenario analysis

- Claude can modify assumptions and explain the resulting changes throughout the model.
- Example: the original attrition assumption is **10%**, and leadership wants to see what happens if attrition increases to **15%**.
- Instead of manually changing cells and checking the workbook, the user tells Claude what scenario to model.
- Claude updates the assumption and explains the resulting impact across the workbook.
- Headcount projections, compensation costs, and other dependent calculations are recalculated through the existing Excel formulas.
- The important point is that Claude can help with both the **edit and the interpretation of the resulting changes**.

### Creating pivot tables and charts

- Claude can turn spreadsheet data into visual summaries.
- Example request: create a visual breakdown of **headcount by department and level**.
- Claude plans and creates:
  - A pivot table based on the headcount data
  - A stacked bar chart to visualize the results
- Users can then ask Claude to adjust the formatting or visualization instead of manually working through Excel's menus.

### Adding new calculations

- Claude can extend an existing model by creating calculations that don't already exist.
- In the example, the Headcount tab already contains **base salary**, but the user wants a new **fully loaded cost** calculation.
- Claude adds a new column for fully loaded cost per employee.
- Instead of hard-coding the assumptions, Claude creates formulas that **reference the rates on the Assumptions tab**.
- This keeps the calculation connected to the model and makes it maintainable if the assumptions change later.
- The calculation can then be applied across employees and used to determine the team's overall fully loaded cost.

### Main takeaway

Claude for Excel is useful when you want Claude to **work inside the spreadsheet rather than simply analyze it from outside**.

It can help with:

- Understanding unfamiliar models
- Tracing and fixing formula errors
- Running what-if scenarios
- Explaining how changes affect the model
- Creating pivot tables and charts
- Adding new calculations
- Building formulas that reference existing assumptions

The key idea is that Claude works alongside the existing Excel model and its relationships, reducing the need to manually copy information between Claude and Excel.

---

#### Video

[Claude for Excel — YouTube](https://www.youtube.com/watch?v=8ZRTSIRWLu4&t)

---

### Claude for Excel

Claude for Excel brings Claude directly into Microsoft Excel through a sidebar. It lets you analyze, understand, and modify spreadsheets through conversation while working inside the workbook.

#### When to use Claude for Excel

- **Understand complex workbooks:** Use Claude to understand multi-tab spreadsheets and trace how formulas and calculations flow between sheets.
- **Update assumptions:** Change model inputs while preserving the existing formula dependencies and relationships throughout the workbook.
- **Debug spreadsheet errors:** Investigate errors such as `#REF!`, `#VALUE!`, or circular references by tracing them back to their source and getting suggested fixes.
- **Create or populate spreadsheets:** Build new spreadsheets or populate existing templates while maintaining appropriate formulas and structure.
- **Create visualizations:** Quickly generate pivot tables and charts to help analyze and present spreadsheet data.

---

### Claude for PowerPoint

Claude for PowerPoint brings Claude directly into Microsoft PowerPoint through a sidebar. You can draft, edit, and restructure presentations through conversation while keeping your existing template and brand styling.

#### When to use Claude for PowerPoint

- **Create a first-draft deck:** Turn an outline, document, or notes into a presentation without manually building every slide.
- **Improve slide copy:** Rewrite and tighten bullets, add speaker notes, or adjust the tone for a specific audience.
- **Restructure presentations:** Reorder sections, split overly dense slides, or combine slides that cover overlapping information.
- **Keep formatting consistent:** Apply consistent titles, bullet styles, layouts, and other formatting across the deck without manually fixing each slide.
- **Get visual suggestions:** Ask Claude for recommendations on layouts, charts, or other visual approaches that best communicate the point of a slide.

---

### Claude for Word

Claude for Word brings Claude directly into Microsoft Word through a sidebar. You can draft, revise, and restructure documents while staying inside the document you're working on.

It can also work with tracked changes and comments, and use context from connected sources to help ground the content you write.

#### When to use Claude for Word

- **Create first drafts:** Turn an outline or rough notes into a structured draft using your team's existing Word template.
- **Revise documents:** Tighten writing, adjust the tone for a particular reader, or restructure sections without leaving Word.
- **Work through feedback:** Use Claude to help address reviewer comments and tracked changes directly in the document.
- **Ground your writing in sources:** Connect relevant source material so Claude can use it when drafting and help ensure claims are based on the underlying information.

---

### Claude for Outlook

Claude for Outlook brings Claude directly into Microsoft Outlook through a sidebar. It can help you manage your inbox, draft replies, and understand long email conversations without leaving Outlook.

Claude can also use context from related email threads and your calendar to make its responses more relevant.

#### What you can use it for

- **Triage emails:** Quickly review incoming mail and identify what needs your attention.
- **Draft replies:** Create replies using context from related email threads and your calendar.
- **Summarize long threads:** Turn lengthy email chains into a concise summary.
- **Identify next steps:** Extract action items and next steps from an email conversation.

#### Availability

Claude for Outlook is currently in **beta** and is installed separately from the other Microsoft 365 add-ins.

[Claude for Outlook setup](https://support.claude.com/en/articles/14855664-use-claude-for-outlook)

---

### Claude in Chrome

---

#### AI Core Overview

**#Claude #AI #BrowserAutomation #Productivity #SafetySecurity #HomeRenovation**

Claude for Chrome brings Claude's computer-use capabilities directly into the browser. It can navigate websites, gather information, work with spreadsheets, and draft content while using the context it finds across different websites and applications.

The demo uses a home renovation scenario where information is spread across planning documents, contractor emails, receipts, and a budget spreadsheet.

#### Intro and use case

- Claude can work directly in the browser rather than only responding to information manually provided in chat.
- The example involves organizing a **home renovation budget** where relevant information is scattered across different sources.
- Claude gathers the required context and then uses it to complete the requested work.

#### Budget workflow

- Claude searches for relevant **emails and receipts** to find the information needed for the renovation budget.
- It gathers the requested records and uses the information it finds as context.
- Claude works directly with the **budget spreadsheet**, filling in missing numbers and updating it in real time.
- After updating the budget, Claude drafts an email that summarizes the renovation plans for the user's partner.
- The user still reviews and makes any final edits before sending the email.

#### Safety and user control

Claude for Chrome is designed around keeping the user in control of actions taken in the browser.

- **Granular permissions:** Users can control which actions Claude is allowed to take.
- **Prompt-injection protection:** The system includes defenses against malicious instructions that may appear on websites Claude visits.
- **Website restrictions:** Users can restrict which websites Claude is allowed to access.
- **Confirmation for sensitive actions:** Claude asks for confirmation before taking sensitive actions, such as making purchases.
- **User review:** For actions like sending an email, Claude can prepare the work while the user retains control over the final action.

#### Main takeaway

Claude in Chrome extends Claude from a chatbot into an **agent that can operate websites and complete browser-based tasks**.

The useful pattern is:

**Find information → use the information → update another tool → prepare the next action**

The important limitation is that browser automation involves real-world actions, so permissions, website restrictions, prompt-injection protection, and confirmation for sensitive actions are important parts of the workflow.

---

#### Video

[Claude in Chrome — YouTube](https://www.youtube.com/watch?v=IypXvHej9eY)

---

### Claude in Chrome

Claude in Chrome is a browser extension that adds Claude as a sidebar in Google Chrome. It can observe what you're working on, maintain context across tabs, and take actions directly within your browser.

**When to use Claude in Chrome:**

- **Summarize web content:** Articles, research papers, documentation, and web pages while browsing
- **Work with email:** Draft responses, summarize conversations, and help manage your inbox
- **Automate repetitive tasks:** Fill out forms and handle repetitive browser workflows
- **Navigate websites:** Test website features or work through multi-step processes without manually clicking through everything
- **Work across multiple tabs:** Maintain context as you move between pages and tasks
- **Work with web-based tools:** Pull context from niche internal tools, CRMs, dashboards, and other websites

**Best use case:** Claude in Chrome is most useful when the information or task is inside a website and would otherwise require you to manually browse, copy information, and move it between tools.

**Important note:** Claude in Chrome is currently in public beta. Anthropic recommends using it for low-risk tasks on trusted websites. Claude asks for permission before taking high-risk actions such as making purchases or sharing personal data. Certain website categories, including financial services and adult content, are blocked by default.

**Key takeaway:** Claude in Chrome gives Claude the ability to **see and interact with the browser**, rather than only answering questions based on information you provide.

---

### Summary

Each of these tools extends Claude's capabilities into the specific environments where you work:

| **Tool** | **Best for** | **Where it runs** |
| --- | --- | --- |
| Claude.ai | General tasks, research, writing, analysis, file creation | Web, desktop, and mobile apps |
| Claude Code | Software development, codebase navigation, git workflows | Terminal/command line, IDE, or your browser |
| Claude Cowork | Complex, multi-step tasks: research briefs, document creation, file organization, data analysis | Desktop (plus web and mobile, in beta, on eligible plans) |
| @Claude | Team collaboration, meeting prep, quick answers in context | Slack workspace |
| Claude Design | UI prototypes, design exploration, design-system-aware mockups | Web |
| Claude for Microsoft 365 | Editing in place and carrying context across documents | Excel, PowerPoint, Word, and Outlook sidebars |
| Claude in Chrome | Web research, email management, browser automation | Chrome browser sidebar |

---

## Lesson 3 : What's Next?

---

### Course Summary

---
#### Getting started with Claude

- Claude is an AI assistant built to be **helpful, harmless, and honest**. It can act as a thinking partner for complex work, not just a chatbot.
- Claude is available through **web, desktop, and mobile apps**, with conversations syncing across devices.
- Effective prompts set the stage by providing **context**, defining the **task/action**, and specifying **rules such as format and style**.

#### Getting better results

- **Iteration is key:** Treat Claude's first response as a starting point and refine it through conversation.
- Generic responses or incorrect tone can usually be improved by providing **more specific context and instructions**.
- **AI Fluency** consists of four competencies:
  - **Delegation** — deciding what to give to AI
  - **Description** — clearly communicating what you want
  - **Discernment** — evaluating and judging AI outputs
  - **Diligence** — checking and refining the work

#### Organizing your work

- **Projects** create dedicated workspaces with persistent knowledge, custom instructions, chat history, and team collaboration.
- **Artifacts** are standalone outputs such as documents, code, diagrams, and interactive tools that Claude creates alongside the conversation.
- **Skills** are instruction packages that teach Claude specialized workflows, including built-in document creation capabilities and custom skills you can create yourself.

#### Expanding Claude's reach

- **Connectors** link Claude to external tools such as Google Workspace, Slack, Notion, and other services, allowing it to work with your actual data.
- **Enterprise Search** provides a dedicated way to search and synthesize information across an organization's connected knowledge sources.
- **Research** performs systematic, multi-source investigations, allowing Claude to gather and synthesize information that would otherwise take hours or days to research manually.

#### Putting it all together

- Claude can support many different roles and workflows, including **sales, marketing, finance, HR, legal, research, and more**.
- Claude is not limited to claude.ai. You can work with it through specialized tools such as **Claude Code, Slack, Excel, PowerPoint, Word, Outlook, and Chrome**.

---

## A word of encouragement

The most important thing now is to **get started**. The skills from this course will improve with practice, and you'll gradually develop intuition for when and how Claude can help.

**Start simple:**
- Pick one recurring task from your work and try it with Claude.
- Examples: drafting an email, summarizing meeting notes, or analyzing a spreadsheet.
- See what happens, then iterate and adjust your approach.
- Over time, learn which workflows and prompting styles work best for your specific needs.

Remember: **Claude is designed to be a collaborator, not a replacement.** The best results come from combining Claude's capabilities with your own expertise, context, and judgment.

You now have the foundation. **The rest comes from doing the work.**

---