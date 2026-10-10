# Cloud GPUs, ROCm, and Cloud Security

## 1. What is ROCm?

ROCm (Radeon Open Compute) is AMD's software platform that allows programs to use AMD GPUs for tasks such as running AI models.

A GPU is a processor particularly good at performing many calculations simultaneously. These calculations are useful for AI because AI models perform enormous numbers of mathematical operations.

ROCm provides the software components needed for programs and AI frameworks to communicate with and use AMD GPUs.

### How ROCm fits into the process

1. **Python code:** The instructions written by the developer.
2. **AI framework (e.g., PyTorch):** A collection of tools that makes building and running AI models easier.
3. **ROCm:** The software layer that enables compatible programs and frameworks to use AMD GPUs.
4. **AMD GPU:** Performs the calculations required to run or train AI models.

ROCm is software, not a physical GPU.

For a cloud-based hackathon, the AMD GPU and ROCm environment are provided remotely, so a powerful local computer or local AMD GPU is not necessarily required.

---

## 2. What is a Cloud GPU?

A cloud GPU is a GPU that you access remotely over the internet instead of owning and using it directly on your computer.

The physical GPU is installed in a remote computer, usually inside a data centre. The data centre contains computers called servers that provide computing resources to users.

The user sends instructions or a program to the remote environment. The server runs the program using its available computing resources and returns the results.

### Example

Suppose you want to summarise a 500-page document using an AI model.

1. You send the document and instructions to a remote server.
2. The server processes the document using an AI model.
3. Its GPU performs the necessary calculations.
4. The server returns the summary to your computer.

The calculations happen remotely. Your computer mainly acts as the interface through which you submit work and receive results.

### The basic mental model

**Your computer = the remote control.**

**Cloud computer = the machine doing the heavy work.**

You don't need to download the entire AI model or perform all its calculations locally if the cloud environment handles those tasks for you.

---

## 3. How Could You Turn Your Own Computer into a Cloud Service?

Imagine owning the most powerful computer in the world, with the best CPU, GPU, maximum RAM, and other high-end hardware.

You could potentially make that computer available to other people over the internet.

The general process would be:

1. Keep the computer running and connected to the internet.
2. Set up software that accepts requests from users.
3. Give users a way to submit programs or computing jobs.
4. Run their jobs using your computer's resources.
5. Return their results.
6. Track their resource usage and charge them.

This is the basic concept behind providing computing resources as a service.

### Two different business models

**A. Owning the hardware and renting it out**

You own the computer and let customers use its computing resources.

- Customers submit jobs.
- Your computer performs the calculations.
- You charge for access or usage.
- You cover electricity, internet, cooling, maintenance, and hardware costs.

Your profit is the revenue remaining after expenses.

**B. Renting someone else's cloud GPU**

A cloud provider owns and maintains the physical servers. You rent access to their computing resources.

- You submit your code or computing job.
- Their servers execute it.
- You retrieve the results.
- You pay the provider for the service.

The second model is the one most relevant to a hackathon that provides cloud-based AMD GPUs.

---

## 4. How Does Cloud Computing Security Work?

Allowing other people to run programs on your computer introduces a serious problem: their programs could potentially damage the machine, access private information, or consume all available resources.

Cloud providers use several security measures to reduce these risks.

### 4.1 Isolation and Sandboxing

**Sandboxing** means running a program inside a restricted environment that limits what it can access or modify.

Imagine a building containing separate locked rooms. A customer can use their assigned room but should not be able to enter other rooms or access the building's control systems.

Similarly, a cloud provider tries to isolate each customer's workload from the underlying host machine and other customers.

Containers and virtual machines are two technologies that can help provide this isolation.

### 4.2 Permissions

Programs should receive only the permissions they need.

For example, a program that performs an AI calculation generally should not automatically have administrator-level access to the entire server.

Restricting permissions reduces the damage a program can cause if it behaves maliciously or contains a bug.

### 4.3 Resource Limits

A program could consume excessive RAM, CPU time, GPU memory, or storage.

Cloud environments can impose resource limits and execution timeouts to prevent one workload from consuming all available resources.

These limits help protect the service and other users.

### 4.4 Network Restrictions

A program may attempt to communicate with other computers or access sensitive internal services.

Network restrictions can limit which systems the program is allowed to contact, reducing the risk of unauthorised access.

### 4.5 Monitoring and Cleanup

Providers can monitor workloads, terminate jobs that violate their rules, and remove temporary environments after use.

However, deleting an environment does not automatically undo damage that has already occurred outside it.

### 4.6 Why Security Is Never Perfect

Isolation mechanisms can contain vulnerabilities. A malicious program might exploit a weakness to escape its restricted environment and affect the underlying system.

Cloud providers therefore combine multiple security measures, keep software updated, and carefully control access to sensitive resources.

**Important principle:** Cloud providers do not necessarily inspect every command and determine whether it is dangerous before execution. A major part of their security strategy is restricting what a program can access and do, even if the program behaves unexpectedly.

---

## 5. Key Takeaways

- **GPU:** A processor particularly suited to performing many calculations simultaneously.
- **ROCm:** AMD's software platform for enabling compatible programs to use AMD GPUs.
- **Cloud GPU:** A physical GPU in a remote computer that you access over the internet.
- **Server:** A computer that provides resources or services to other computers.
- **Cloud provider:** A company that operates computing infrastructure and makes it available to customers.
- **Sandboxing:** Running programs in restricted environments to limit their access and potential damage.
- **Isolation:** Separating workloads so that one customer's program cannot freely interfere with other workloads or the underlying system.

For the AMD hackathon, the essential mental model is that your code can run on a remote machine equipped with an AMD GPU. ROCm helps compatible software use that GPU, while the cloud provider manages the underlying infrastructure and its security.

---

## Intelligent Industry — Safety Measures, Machinery, and Where AI Fits

### 1. Existing Industrial Safety Measures

Factories already use several safety measures to protect workers and machinery. AI is not always necessary to implement these measures.

- **Physical barriers and guards:** Fences, covers, and enclosures prevent workers from reaching dangerous moving parts.
- **Emergency stops:** Buttons that allow workers to stop dangerous machinery quickly.
- **Interlocks:** Mechanisms that prevent a machine from operating when a safety condition is not met, such as a protective door being open.
- **Sensors and automatic shutdowns:** Sensors detect conditions such as a person entering a restricted area or a machine exceeding a safe temperature. A predefined rule can trigger an alarm or stop the machine.
- **Protective equipment and training:** Helmets, goggles, gloves, hearing protection, and procedures that reduce the risk of injury.
- **Inspections and maintenance:** Workers inspect equipment, follow operating procedures, and isolate dangerous energy sources before servicing machinery. This isolation process is commonly called lockout/tagout.

#### Where AI fits into industrial safety

AI can supplement existing safety systems by identifying patterns or combinations of conditions that conventional rules might miss.

However, AI can also produce false alarms or miss hazards. Critical safety functions should use appropriate, dependable safety mechanisms rather than relying solely on AI predictions.

**Key distinction:** Conventional automation follows predefined rules. AI can help identify patterns in data or recognise situations that are difficult to describe using simple rules. Not every industrial problem requires AI.

---

### 2. Industries and What Their Machinery Does

Different industries use machinery to perform a range of operations. Understanding what the machinery accomplishes is often more useful than memorising individual machine names.

| Industry                           | What its machinery does                                                                                                   |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Automotive manufacturing           | Joins, welds, paints, assembles, moves, and inspects vehicle components.                                                  |
| Food and beverage                  | Cleans, cuts, mixes, cooks, cools, fills containers, seals packaging, and inspects products.                              |
| Pharmaceutical manufacturing       | Measures ingredients, mixes compounds, produces medicines, fills containers, and maintains controlled conditions.         |
| Electronics manufacturing          | Places tiny components, solders connections, assembles circuit boards, tests electrical functions, and inspects products. |
| Metal and steel production         | Melts, shapes, rolls, cuts, transports, and inspects metal.                                                               |
| Oil, gas, and chemical processing  | Moves fluids and gases, separates substances, controls pressure and temperature, and manages chemical reactions.          |
| Textile and clothing manufacturing | Spins fibres, weaves fabric, dyes materials, cuts patterns, stitches pieces, and finishes garments.                       |
| Cement and construction materials  | Crushes, grinds, mixes, heats, packages, and transports materials.                                                        |
| Agriculture                        | Prepares soil, plants seeds, harvests crops, irrigates fields, and sorts produce.                                         |
| Warehousing and logistics          | Moves, lifts, sorts, stores, scans, and packs goods.                                                                      |

Across these industries, machinery generally performs five broad functions:

1. **Transform:** Cut, shape, heat, mix, or assemble materials.
2. **Move:** Transport, lift, sort, and position materials.
3. **Control:** Maintain temperature, pressure, speed, and flow.
4. **Inspect:** Check whether products meet specifications.
5. **Monitor:** Detect unusual operating conditions, wear, and potential hazards.

---

### 3. Initial Analysis: Where AI Is Actually Useful

The main question is not whether AI _can_ be used in a process, but whether it provides a meaningful advantage over a simpler solution.

#### Machine failure prediction

AI can analyse historical and real-time data, such as temperature, vibration, and power consumption, to identify patterns associated with potential machine failures.

The goal is to detect warning signs early enough to allow maintenance before a breakdown occurs.

#### Defect detection

AI can analyse images, measurements, or other production data to identify products that may not meet the required specifications.

For example, it could identify a crack, an incorrectly positioned component, or an unusual product dimension.

#### Worker safety

Many safety problems can be handled using conventional engineering solutions, such as physical guards, sensors, interlocks, and predefined control rules.

AI may be useful when a situation requires more complex recognition or interpretation, but it is not automatically the best solution.

#### Initial conclusion

The current working hypothesis is that machine failure prediction and product defect detection are relatively clear applications of AI in industrial settings.

For other problems, conventional automation may be sufficient. The value of AI depends on whether it can solve a problem more effectively than the alternatives.

This is an initial assessment, not a universal conclusion. Some safety, monitoring, and waste-reduction problems may benefit from AI, while others may not need it at all.

---

## Health and Wellbeing — Understanding Where AI Is Useful

### 1. What Is Health and Wellbeing?

The goal is to make some part of the patient's journey safer, clearer, or more efficient.

The patient journey includes everything from describing symptoms and receiving an assessment to understanding treatment and attending follow-up appointments.

AI can potentially help patients communicate their problems, help healthcare professionals interpret information, and identify patterns that may warrant medical attention.

The brief explicitly states:

- No autonomous diagnosis.
- Uncertainty must be communicated.
- Human review must remain part of the process.

### 2. AI for Patient Interviews Before Seeing a Doctor

One potential application is an AI system that interviews patients remotely before their appointment.

The patient describes their symptoms in their own words. The AI asks relevant follow-up questions, collects additional details, and organises the information into a structured summary for a healthcare professional.

#### Why this could be useful

- Patients sometimes struggle to explain their symptoms clearly.
- Patients may forget important details during appointments.
- Follow-up questions can uncover relevant information that the patient did not initially mention.
- Doctors can review an organised medical history before speaking to the patient.
- Remote interviews may help healthcare facilities handle some consultations more efficiently.

The purpose would be to improve communication between patients and healthcare professionals, not to replace the doctor.

#### Potential problems and limitations

- AI can misunderstand a patient's description.
- It may overlook important symptoms or ask inappropriate follow-up questions.
- Patients may trust the AI's interpretation too much.
- A well-organised summary does not guarantee that the information is medically accurate or complete.
- Remote interviews cannot replace physical examinations, laboratory tests, or other procedures when these are necessary.
- Reducing hospital visits is not guaranteed. The system would need appropriate clinical oversight and safe referral procedures.

### 3. Does a Patient Interview Actually Need AI?

This is an important question when evaluating whether AI is justified.

A conventional questionnaire can already collect symptoms, medical history, and other information. If the questions are predictable and the answers fit predefined categories, ordinary software may be sufficient.

AI becomes more potentially useful when:

- Patients describe symptoms in their own words rather than selecting predefined answers.
- Their answers are ambiguous or incomplete.
- Follow-up questions need to adapt to what they have said.
- Relevant details emerge gradually throughout the conversation.

The key question is whether adaptive AI questioning produces a meaningful improvement over a well-designed conventional questionnaire.

That improvement would need to be tested rather than assumed.

### 4. Predicting Patient Deterioration

AI can analyse historical patient records and current observations to identify patterns associated with worsening medical conditions.

For example, changes in recorded vital signs might indicate that a patient needs a clinical review.

**Potential benefits:**

- Earlier identification of patients who may be deteriorating.
- Faster clinical review and intervention.
- Better prioritisation of patients who need attention.

**Potential problems:**

- False alarms can overwhelm healthcare staff.
- Missed warnings can create a false sense of security.
- Predictions may be unreliable when training data is inadequate or differs from the patients being assessed.
- Clinical validation and appropriate human oversight are necessary.

The system should flag concerning patterns for healthcare professionals to review rather than independently decide what treatment a patient needs.

### 5. Helping Healthcare Professionals Find Information

AI may help healthcare workers retrieve and interpret information spread across medical records, clinical documents, and guidelines.

However, not every information-retrieval problem requires AI.

- **Finding a known document:** Conventional search software is usually sufficient.
- **Retrieving information from structured records:** Ordinary database queries may be sufficient.
- **Interpreting complicated information across lengthy documents:** AI may be useful when the task requires understanding natural language and connecting relevant details.

AI can also produce incorrect answers or misinterpret medical information. Important claims should therefore be traceable to reliable source documents and verified by qualified professionals.

The important distinction is between retrieving information and interpreting it.

### 6. AI Versus Conventional Software

A recurring principle across healthcare applications is that using AI does not automatically make a solution better.

| Task                                                     | Is AI necessarily required? |
| -------------------------------------------------------- | --------------------------- |
| Appointment reminders                                    | No                          |
| Collecting answers to fixed questions                    | Usually no                  |
| Conducting adaptive patient interviews                   | Potentially useful          |
| Predicting patient deterioration                         | Potentially useful          |
| Searching for a known document                           | Usually no                  |
| Interpreting complex information across multiple records | Potentially useful          |

The decision should depend on whether AI offers a meaningful advantage over a simpler alternative.

### 7. A Broader Observation About AI's Current Limitations

AI can already help interpret information, identify patterns, and communicate with people. However, these capabilities do not automatically make it reliable enough to perform every task independently.

Healthcare is particularly demanding because incorrect conclusions can have serious consequences.

More advanced diagnostic technologies, including specialised imaging and optical sensing systems, can provide information that ordinary conversations and text-based analysis cannot. AI may help interpret the resulting measurements or images, but the quality of the sensors, available data, validation, and clinical workflow all matter.

The combination of AI with advanced diagnostic hardware is a separate area from using AI to organise information or conduct patient interviews.

### 8. Key Takeaway

The central question is not whether AI can perform a task, but whether it solves the underlying problem better than conventional software or existing methods.

For the patient-interview concept, the main assumption to investigate is whether adaptive questioning can gather more relevant and accurate information than a well-designed questionnaire.

For deterioration prediction, the main challenges are reliable data, false alarms, missed warnings, and clinical validation.

For information retrieval, the question is whether the task requires interpretation or merely searching and retrieving documents.

**The general principle:** Identify the problem first, understand the existing solutions, examine their limitations, and only then determine whether AI offers a meaningful improvement.

---

## 4. Reinvent Commerce — Customer Behaviour, Business Decisions, and Where AI Fits

### 4.1 Three Different Problems Hidden Inside Commerce

Commerce problems can be divided into three broad categories:

**A. Helping customers make decisions**

Example: A customer wants to buy a laptop but doesn't know which one suits their needs.

A useful system would understand the customer's budget, intended use, and constraints, then compare suitable products using reliable specifications.

However, general-purpose AI assistants such as ChatGPT and Claude can already research products and make recommendations. A separate AI product needs a compelling advantage, such as access to specialised data, integration with a retailer's inventory, or a workflow that general-purpose assistants cannot easily provide.

**B. Helping businesses understand customer behaviour**

Businesses may already collect information such as:

- Products or services customers view.
- Items they add to their carts.
- Purchases they complete.
- Transactions they abandon.
- Products they return.
- Steps at which customers abandon registration or onboarding.
- Questions and complaints submitted to customer support.

These observations can reveal patterns without requiring customers to complete surveys.

However, observed behaviour does not reveal intention with certainty. A person viewing a product might be interested, comparing alternatives, researching for somebody else, or simply curious.

**C. Helping businesses make decisions**

Examples include:

- How much inventory should a retailer order?
- Why are customers abandoning account verification?
- Which recurring customer-support problems should be fixed first?
- What changes could reduce customer churn?
- How should a company allocate limited staff or resources?

These problems concern business decisions rather than simply providing a chatbot.

### 4.2 Behaviour Is Not the Same as Intention

Consider a customer who repeatedly views a product but never purchases it.

Possible explanations include:

- The price is too high.
- Shipping costs are unattractive.
- The customer is comparing alternatives.
- The specifications or product description are confusing.
- The customer does not trust the seller.
- The customer is interested but is waiting for a better time.
- The customer never intended to buy it.

The observed behaviour alone cannot establish which explanation is correct.

Analysing many customers can reveal statistical patterns, but it does not automatically prove why those patterns occur.

**Important distinction:** Data can show what happened without establishing why it happened.

### 4.3 Recommendation Systems: Scripts Versus Machine Learning

A recommendation system might keep suggesting products similar to something a customer viewed, even if the customer never purchased it.

There are two different problems to investigate.

**Problem A: Poor rules**

The system may treat a product view as a strong signal of interest.

A conventional script could improve this by assigning different weights to different actions:

- Viewing a product.
- Viewing it repeatedly.
- Adding it to a cart.
- Purchasing it.
- Returning it.

The weights and rules would need to be tested rather than assumed correct.

**Problem B: Complex behaviour that rules cannot adequately capture**

A statistical or machine-learning model could learn patterns from historical examples and estimate which products or outcomes are more likely.

The model might identify relationships that would be difficult to express through manually written rules.

However, it can still make mistakes. More data may improve predictions without revealing every customer's true intentions.

**Conclusion:** Use explicit rules when they solve the problem adequately. Consider machine learning when patterns are too complex for practical hand-written rules. An LLM is not automatically the right model for recommendations or predictions.

### 4.4 The Roles of Conventional Software, Statistics, Machine Learning, and LLMs

A business system can have several layers.

1. **Data collection and organisation:** Record and organise relevant events. This is mostly conventional software and database work.
2. **Analysis and prediction:** Identify patterns, estimate probabilities, or forecast future outcomes. Statistics and machine learning may be useful here.
3. **Interpretation and communication:** Summarise complicated records, interpret customer messages, or let a manager investigate evidence using natural language. An LLM may help here.
4. **Action:** Change a process, improve a product, contact a customer, or adjust a business decision. This requires a suitable workflow and an appropriate response to the evidence.

Not every system needs every layer, and not every layer needs AI.

The objective is to solve the problem reliably, not to maximise the amount of AI used.

### 4.5 Important Statistical Problems

**Observation versus intention**

A click is an observable action, not proof of what the person wanted.

**Correlation versus causation**

Two events occurring together does not prove that one caused the other.

For example, customers who read a particular article might be more likely to purchase a product. That does not prove the article caused the purchase; those customers might already have been more interested.

**Feedback loops**

A recommendation system changes what customers see, then uses their subsequent behaviour to improve future recommendations.

If a system stops showing a customer certain products, it loses opportunities to observe whether that customer would have liked them. Its own decisions can therefore influence the data used to evaluate it.

**Selection bias**

The customers who purchase, leave reviews, complete surveys, or remain active may differ from those who do not. Analysing only the visible or participating group can produce misleading conclusions.

These problems mean that finding a pattern is only the beginning. The pattern must be interpreted and evaluated carefully before using it to make decisions.

### 4.6 Privacy and Trust as Product Constraints

Personalisation can benefit customers by helping them find relevant products or services. However, customers may dislike discovering that a company collects or infers information about their behaviour.

It is useful to distinguish between:

- **Collecting data:** Recording that a customer viewed a product.
- **Inferring information:** Estimating the customer's preferences from their behaviour.
- **Using an inference:** Changing recommendations, offers, prices, or other treatment.
- **Retaining or sharing data:** Keeping information or making it available to other parties.

These are different activities with different risks and legal implications.

Collecting less data, limiting retention, explaining how data is used, and giving customers appropriate control over optional personalisation can help protect trust. Aggregation and anonymisation can reduce certain risks, but do not automatically eliminate them.

In a financial-services context, behavioural data may reveal sensitive financial interests or habits, making careful handling particularly important.

Privacy is not merely an obstacle to technical development. It affects whether customers trust and accept a product.

### 4.7 Prediction Is Not the Same as a Useful Decision

Suppose a brokerage predicts that a customer is likely to stop using its platform.

That prediction alone does not solve the problem.

The business still needs to determine:

- Why the customer might leave.
- Whether the prediction is sufficiently reliable.
- Whether the business can take an effective action.
- Whether that action would improve the outcome.
- Whether the intervention creates costs or harms elsewhere.

A model can predict an outcome accurately while providing little business value if nobody can act on its prediction effectively.

This distinction is important in quantitative finance, forecasting, and business analytics: predicting what may happen is different from determining which action is likely to improve the outcome.

### 4.8 A Framework for Investigating Business Problems

Before proposing an AI solution, ask:

1. **Who makes the decision?** A customer, manager, support team, or another party?
2. **What specific decision are they making?**
3. **What information do they currently use?**
4. **What do they get wrong, and why?** Missing information, poor tools, weak analysis, conflicting incentives, or something else?
5. **What does the mistake cost?** Lost revenue, wasted time, customer frustration, excess inventory, or lost trust?
6. **Could better information realistically change the decision?**
7. **How can the improvement be measured against a reasonable baseline?**

A vague goal such as "understand customers better" should be converted into a specific, testable problem.

For example: "Identify why customers abandon account verification and test whether addressing the main causes increases successful completion."

Even then, the solution might be better instructions, a simpler interface, conventional analytics, machine learning, or a combination.

### 4.9 Overall Conclusion

The most important question is not "Where can we add AI?"

It is:

**Which important decision is currently being made poorly, why is it difficult to make well, and what evidence would show that a solution actually improves the outcome?**

A business may have plenty of data but lack a reliable way to turn it into useful decisions. AI may help, but the underlying problem could instead be poor processes, inadequate software, missing information, or organisational incentives.

Start with the problem, understand the existing approach, identify its limitations, and then choose the simplest approach that can demonstrably improve the result.

---
