**Be clear, direct, and detailed**

Copy page  
While these tips apply broadly to all Claude models, you can find prompting tips specific to extended thinking models [here](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/extended-thinking-tips).

When interacting with Claude, think of it as a brilliant but very new employee (with amnesia) who needs explicit instructions. Like any new employee, Claude does not have context on your norms, styles, guidelines, or preferred ways of working. The more precisely you explain what you want, the better Claude’s response will be.

The golden rule of clear prompting  
Show your prompt to a colleague, ideally someone who has minimal context on the task, and ask them to follow the instructions. If they’re confused, Claude will likely be too.

## [**​**](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/be-clear-and-direct#how-to-be-clear%2C-contextual%2C-and-specific)

## **How to be clear, contextual, and specific**

* Give Claude contextual information: Just like you might be able to better perform on a task if you knew more context, Claude will perform better if it has more contextual information. Some examples of contextual information:  
  * What the task results will be used for  
  * What audience the output is meant for  
  * What workflow the task is a part of, and where this task belongs in that workflow  
  * The end goal of the task, or what a successful task completion looks like  
* Be specific about what you want Claude to do: For example, if you want Claude to output only code and nothing else, say so.  
* Provide instructions as sequential steps: Use numbered lists or bullet points to better ensure that Claude carries out the task the exact way you want it to.

### [**​**](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/be-clear-and-direct#examples)

### **Examples**

Notice that Claude still makes mistakes in the unclear prompting example, such as leaving in a customer’s name.

| Role | Unclear Prompt | Clear Prompt |
| ----- | ----- | ----- |
| User | Please remove all personally identifiable information from these customer feedback messages: {{FEEDBACK\_DATA}} | Your task is to anonymize customer feedback for our quarterly review. Instructions: 1\. Replace all customer names with “CUSTOMER\_\[ID\]” (e.g., “Jane Doe” → “CUSTOMER\_001”). 2\. Replace email addresses with “EMAIL\_\[ID\]@example.com”. 3\. Redact phone numbers as “PHONE\_\[ID\]“. 4\. If a message mentions a specific product (e.g., “AcmeCloud”), leave it intact. 5\. If no PII is found, copy the message verbatim. 6\. Output only the processed messages, separated by ”---”. Data to process: {{FEEDBACK\_DATA}} |
| Assistant (Claude’s response) | Here are the anonymized customer feedback messages: 1\. I’ve been using your software for years, and it’s been great. But lately, AcmeCloud has been crashing a lot. Fix it\! 2\. XXX, your customer support rep, was incredibly helpful. He guided me through the whole process. My email is XXX if you want to send a survey. 3\. I’m John Smith, and I’m not happy. I’ve been on hold for 2 hours trying to reach someone at XXX. This is unacceptable\! | CUSTOMER\_001: I’ve been using your software for years, and it’s been great. But lately, AcmeCloud has been crashing a lot. Fix it\! \--- CUSTOMER\_002: CUSTOMER\_SERVICE\_001, your customer support rep, was incredibly helpful. He guided me through the whole process. My email is EMAIL\_002@example.com if you want to send a survey. \--- CUSTOMER\_003: I’m CUSTOMER\_003, and I’m not happy. I’ve been on hold for 2 hours trying to reach someone at PHONE\_001. This is unacceptable\! |

Notice that Claude makes up details to fill in the gaps where it lacks context with the vague prompt.

| Role | Vague Prompt | Specific Prompt |
| ----- | ----- | ----- |
| User | Write a marketing email for our new AcmeCloud features. | Your task is to craft a targeted marketing email for our Q3 AcmeCloud feature release. Instructions: 1\. Write for this target audience: Mid-size tech companies (100-500 employees) upgrading from on-prem to cloud. 2\. Highlight 3 key new features: advanced data encryption, cross-platform sync, and real-time collaboration. 3\. Tone: Professional yet approachable. Emphasize security, efficiency, and teamwork. 4\. Include a clear CTA: Free 30-day trial with priority onboarding. 5\. Subject line: Under 50 chars, mention “security” and “collaboration”. 6\. Personalization: Use {{COMPANY\_NAME}} and {{CONTACT\_NAME}} variables. Structure: 1\. Subject line 2\. Email body (150-200 words) 3\. CTA button text |
| Assistant (Claude’s response) | Here’s a draft marketing email for our new features: Subject: Boost Your Business with AcmeCloud’s Latest Features Dear Valued Customer, We’re excited to introduce three powerful features to AcmeCloud that will revolutionize your workflow: 1\. Real-Time Collaboration: Work on documents simultaneously with your team. No more version control issues\! 2\. AI-Powered Insights: Make data-driven decisions with AI that analyzes trends and automates tasks. 3\. Advanced Security Suite: End-to-end encryption, multi-factor auth, and threat detection keep your data safe. Limited Offer: Upgrade now for a 20% first-year discount. Plus, refer a friend for an extra 10% off\! Best, The AcmeCloud Team | Subject line: AcmeCloud: Enterprise security meets real-time teamwork Email body: Dear {{CONTACT\_NAME}}, At {{COMPANY\_NAME}}, you’re scaling fast and eyeing the cloud. But with growth comes the challenge of keeping data secure while fostering collaboration. That’s where AcmeCloud’s Q3 release comes in, tailor-made for tech innovators like you. 1\. Fort Knox for Your Files: Military-grade encryption now safeguards your data, both in motion and at rest. Your intellectual property stays yours, period. 2\. Sync Without Borders: Windows, Mac, or Linux—AcmeCloud speaks all languages. Unified version control means no more “final\_v2\_REALLY\_FINAL.doc”. 3\. Collaborate at Light Speed: Ditch the attachment ping-pong. Now your devs, designers, and data scientists co-create in real-time, slashing time-to-market. Don’t just take our word for it. Experience the AcmeCloud difference with our 30-day trial. And because we know time is your most precious asset, we’re throwing in priority onboarding. Elevate Your Team Now \- Free 30-Day Trial |

Notice that Claude outputs superfluous text and different formating with the vague prompt.

| Role | Vague Prompt | Detailed Prompt |
| ----- | ----- | ----- |
| User | Analyze this AcmeCloud outage report and summarize the key points. {{REPORT}} | Analyze this AcmeCloud outage report. Skip the preamble. Keep your response terse and write only the bare bones necessary information. List only: 1\) Cause 2\) Duration 3\) Impacted services 4\) Number of affected users 5\) Estimated revenue loss. Here’s the report: {{REPORT}} |
| Assistant (Claude’s response) | Here’s a summary of the key points from the AcmeCloud outage report: On May 15th, a misconfigured load balancer update caused significant traffic routing issues, resulting in a service outage from 09:15 to 13:52 UTC. The 4-hour 37-minute disruption impacted our core file syncing service and admin dashboard, rendering them inaccessible. Additionally, the mobile app experienced partial functionality loss. Approximately 68% of our user base, totaling 1.3 million users, were affected. Based on our Service Level Agreements (SLAs) and average revenue per user, we estimate a financial impact of $420,000 in service credits and potential customer churn. | 1\) Cause: Misconfigured load balancer update 2\) Duration: 4h 37m (09:15-13:52 UTC, May 15\) 3\) Impacted: Core sync, admin dashboard (down); mobile app (partial) 4\) Affected users: 1.3M (68% of base) 5\) Est. revenue loss: $420,000 |

**Use examples (multishot prompting) to guide Claude's behavior**

Copy page  
While these tips apply broadly to all Claude models, you can find prompting tips specific to extended thinking models [here](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/extended-thinking-tips).

Examples are your secret weapon shortcut for getting Claude to generate exactly what you need. By providing a few well-crafted examples in your prompt, you can dramatically improve the accuracy, consistency, and quality of Claude’s outputs. This technique, known as few-shot or multishot prompting, is particularly effective for tasks that require structured outputs or adherence to specific formats.

Power up your prompts: Include 3-5 diverse, relevant examples to show Claude exactly what you want. More examples \= better performance, especially for complex tasks.

## [**​**](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/multishot-prompting#why-use-examples%3F)

## **Why use examples?**

* Accuracy: Examples reduce misinterpretation of instructions.  
* Consistency: Examples enforce uniform structure and style.  
* Performance: Well-chosen examples boost Claude’s ability to handle complex tasks.

## [**​**](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/multishot-prompting#crafting-effective-examples)

## **Crafting effective examples**

For maximum effectiveness, make sure that your examples are:

* Relevant: Your examples mirror your actual use case.  
* Diverse: Your examples cover edge cases and potential challenges, and vary enough that Claude doesn’t inadvertently pick up on unintended patterns.  
* Clear: Your examples are wrapped in \<example\> tags (if multiple, nested within \<examples\> tags) for structure.

Ask Claude to evaluate your examples for relevance, diversity, or clarity. Or have Claude generate more examples based on your initial set.  
Notice that in the “no examples” version, Claude does not list multiple options for each category, despite its written analysis indicating that there are multiple categories for certain feedback. It also includes a long explanation when we may not want it to.

| Role | No Examples | With Examples |
| ----- | ----- | ----- |
| User | Analyze this customer feedback and categorize the issues. Use these categories: UI/UX, Performance, Feature Request, Integration, Pricing, and Other. Also rate the sentiment (Positive/Neutral/Negative) and priority (High/Medium/Low). Here is the feedback: {{FEEDBACK}} | Our CS team is overwhelmed with unstructured feedback. Your task is to analyze feedback and categorize issues for our product and engineering teams. Use these categories: UI/UX, Performance, Feature Request, Integration, Pricing, and Other. Also rate the sentiment (Positive/Neutral/Negative) and priority (High/Medium/Low). Here is an example: \<example\> Input: The new dashboard is a mess\! It takes forever to load, and I can’t find the export button. Fix this ASAP\! Category: UI/UX, Performance Sentiment: Negative Priority: High\</example\> Now, analyze this feedback: {{FEEDBACK}} |
| Assistant (Claude’s response) | Here’s the analysis of the customer feedback: Issue: UI/UX Sentiment: Negative Priority: High The customer is frustrated with the new dashboard design, which they find cluttered and slow to load. They specifically call out the missing “export” button, which is likely a critical feature. This issue needs to be addressed as a high priority. Issue: Integration Sentiment: Positive Priority: Medium The customer is pleased with the existing Salesforce integration but would like to see support for Hubspot as well. This is a feature request that could be considered for a future product update. Issue: Pricing Sentiment: Negative Priority: High The customer finds the pricing to be unreasonable, especially for the basic features. They are threatening to switch to a competitor, so this is a high-priority issue that needs to be reviewed. Issue: Performance Sentiment Negative Priority: High The customer is experiencing critical issues with the mobile app, where large file uploads consistently result in crashes. This is a significant problem that impacts the customer’s ability to use the product effectively and should be addressed as a high priority. Issue: UI/UX Sentiment: Positive Priority: Low The customer is overall satisfied with the product, specifically calling out the intuitive UI and excellent customer support. This is a positive piece of feedback that does not require any immediate action. | Here’s the analysis of the customer feedback: 1\. The new dashboard is a mess\! It takes forever to load, and I can’t find the export button. Fix this ASAP\! Category: UI/UX, Performance Sentiment: Negative Priority: High 2\. Love the Salesforce integration\! But it’d be great if you could add Hubspot too. Category: Integration, Feature Request Sentiment: Positive Priority: Medium 3\. Your pricing is ridiculous\! $99/mo for basic features? I’m switching to Competitor X. Category: Pricing Sentiment: Negative Priority: High 4\. The mobile app keeps crashing when I try to upload large files (\>50MB). This is critical for our field agents. Category: Performance Sentiment: Negative Priority: High 5\. Overall, I’m happy with the product. The UI is intuitive, and the customer support is top-notch. Keep it up\! Category: UI/UX, Other (Customer Support) Sentiment: Positive Priority: Low |

**Let Claude think (chain of thought prompting) to increase performance**

Copy page  
While these tips apply broadly to all Claude models, you can find prompting tips specific to extended thinking models [here](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/extended-thinking-tips).

When faced with complex tasks like research, analysis, or problem-solving, giving Claude space to think can dramatically improve its performance. This technique, known as chain of thought (CoT) prompting, encourages Claude to break down problems step-by-step, leading to more accurate and nuanced outputs.

## [**​**](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/chain-of-thought#before-implementing-cot)

## **Before implementing CoT**

### [**​**](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/chain-of-thought#why-let-claude-think%3F)

### **Why let Claude think?**

* Accuracy: Stepping through problems reduces errors, especially in math, logic, analysis, or generally complex tasks.  
* Coherence: Structured thinking leads to more cohesive, well-organized responses.  
* Debugging: Seeing Claude’s thought process helps you pinpoint where prompts may be unclear.

### [**​**](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/chain-of-thought#why-not-let-claude-think%3F)

### **Why not let Claude think?**

* Increased output length may impact latency.  
* Not all tasks require in-depth thinking. Use CoT judiciously to ensure the right balance of performance and latency.

Use CoT for tasks that a human would need to think through, like complex math, multi-step analysis, writing complex documents, or decisions with many factors.  
---

## [**​**](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/chain-of-thought#how-to-prompt-for-thinking)

## **How to prompt for thinking**

The chain of thought techniques below are ordered from least to most complex. Less complex methods take up less space in the context window, but are also generally less powerful.

CoT tip: Always have Claude output its thinking. Without outputting its thought process, no thinking occurs\!

* Basic prompt: Include “Think step-by-step” in your prompt.  
  * Lacks guidance on *how* to think (which is especially not ideal if a task is very specific to your app, use case, or organization)  
* Example: Writing donor emails (basic CoT)  
* 

|  |  |
| ----- | ----- |
|  |   |

*   
* Guided prompt: Outline specific steps for Claude to follow in its thinking process.  
  * Lacks structuring to make it easy to strip out and separate the answer from the thinking.  
* Example: Writing donor emails (guided CoT)  
* 

|  |  |
| ----- | ----- |
|  |   |

*   
* Structured prompt: Use XML tags like \<thinking\> and \<answer\> to separate reasoning from the final answer.  
* Example: Writing donor emails (structured guided CoT)  
* 

|  |  |
| ----- | ----- |
|  |   |

* 

### [**​**](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/chain-of-thought#examples)

### **Examples**

Without step-by-step thinking, Claude gives a recommendation that seems reasonable but lacks depth. It doesn’t quantify the potential outcomes or consider historical market performance, which are crucial for making an informed decision.

| Role | Content |
| ----- | ----- |
| User | You’re a financial advisor. A client wants to invest $10,000. They can choose between two options: A) A stock that historically returns 12% annually but is volatile, or B) A bond that guarantees 6% annually. The client needs the money in 5 years for a down payment on a house. Which option do you recommend? |
| Assistant | Based on the information provided, I would recommend option B, the bond that guarantees a 6% annual return. Here’s why: 1\. Certainty: The bond offers a guaranteed 6% annual return, which provides certainty in financial planning. This is crucial when the client has a specific financial goal (down payment) with a fixed timeline (5 years). 2\. Risk aversion: Since the client needs this money for an important life event (buying a house), they likely have a low risk tolerance. The volatility of the stock market could jeopardize their plans if there’s a downturn close to when they need the funds. 3\. Time horizon: With only 5 years, there’s less time to recover from potential stock market downturns. Longer investment horizons (10+ years) are generally better suited for weathering stock market volatility. While the stock’s historical 12% return is attractive, past performance doesn’t guarantee future results. The guaranteed 6% from the bond ensures the client will have the funds they need when it’s time to make the down payment. |

With step-by-step thinking, the advisor provides a much richer analysis. It calculates exact figures for both scenarios, considers historical market volatility, and deeply analyzes the client’s risk tolerance. This thorough reasoning leads to a more confident and justifiable recommendation.

| Role | Content |
| ----- | ----- |
| User | You’re a financial advisor. A client wants to invest $10,000. They can choose between two options: A) A stock that historically returns 12% annually but is volatile, or B) A bond that guarantees 6% annually. The client needs the money in 5 years for a down payment on a house. Which option do you recommend? Think step-by-step. |
| Assistant | To determine the best investment option for our client, I’ll consider several factors step-by-step: \<thinking\> 1\. Understand the client’s goal and timeline: \- Goal: Down payment for a house \- Timeline: 5 years \- Implication: This is a short-term, high-priority financial goal. The client likely cannot afford significant risk or volatility. 2\. Analyze Option A (Stock): \- Pro: Higher historical return (12% annually) \- Con: Volatile (implying potential for significant gains or losses) \- Calculate potential 5-year return: \- Best case (12% annually): $10,000 \* (1.12)^5 ≈ $17,623.42 \- Worst case (market crash): Could lose a substantial portion, e.g., 50% crash \= $5,000 3\. Analyze Option B (Bond): \- Pro: Guaranteed return (6% annually) \- Con: Lower return compared to historical stock performance \- Calculate 5-year return: \- Guaranteed: $10,000 \* (1.06)^5 ≈ $13,382.25 4\. Consider risk tolerance: \- Goal is a house down payment (essential, not discretionary) \- Short timeline (5 years) limits ability to recover from market downturns \- Conclusion: Client likely has low risk tolerance 5\. Historical perspective: \- Stock’s 12% is historical, not guaranteed \- In 5-year periods, stock market can vary wildly: \- 2003-2007 (pre-financial crisis): S\&P 500 up \~82% \- 2007-2011 (during crisis): S\&P 500 down \~2% \- Conclusion: Past performance doesn’t guarantee future results, especially short-term 6\. Final analysis: \- Option A (Stock): Higher potential return but unacceptable risk of not meeting the down payment goal \- Option B (Bond): Guaranteed to meet \~80% of best-case stock scenario, 100% certainty of having funds \</thinking\> \<answer\> I recommend Option B, the bond with a guaranteed 6% annual return. While the stock’s historical 12% return is tempting, the bond ensures you’ll have $13,382.25 in 5 years for your house down payment. Given the importance and short timeline of your goal, the stock’s volatility poses an unacceptable risk. The bond provides certainty, which is invaluable for such a crucial financial milestone. \</answer\>  |

**Use XML tags to structure your prompts**

Copy page  
While these tips apply broadly to all Claude models, you can find prompting tips specific to extended thinking models [here](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/extended-thinking-tips).

When your prompts involve multiple components like context, instructions, and examples, XML tags can be a game-changer. They help Claude parse your prompts more accurately, leading to higher-quality outputs.

XML tip: Use tags like \<instructions\>, \<example\>, and \<formatting\> to clearly separate different parts of your prompt. This prevents Claude from mixing up instructions with examples or context.

## [**​**](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags#why-use-xml-tags%3F)

## **Why use XML tags?**

* Clarity: Clearly separate different parts of your prompt and ensure your prompt is well structured.  
* Accuracy: Reduce errors caused by Claude misinterpreting parts of your prompt.  
* Flexibility: Easily find, add, remove, or modify parts of your prompt without rewriting everything.  
* Parseability: Having Claude use XML tags in its output makes it easier to extract specific parts of its response by post-processing.

There are no canonical “best” XML tags that Claude has been trained with in particular, although we recommend that your tag names make sense with the information they surround.  
---

## [**​**](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags#tagging-best-practices)

## **Tagging best practices**

1. Be consistent: Use the same tag names throughout your prompts, and refer to those tag names when talking about the content (e.g, Using the contract in \<contract\> tags...).  
2. Nest tags: You should nest tags \<outer\>\<inner\>\</inner\>\</outer\> for hierarchical content.

Power user tip: Combine XML tags with other techniques like multishot prompting (\<examples\>) or chain of thought (\<thinking\>, \<answer\>). This creates super-structured, high-performance prompts.

### [**​**](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags#examples)

### **Examples**

Without XML tags, Claude misunderstands the task and generates a report that doesn’t match the required structure or tone. After substitution, there is also a chance that Claude misunderstands where one section (like the the Q1 report example) stops and another begins.

| Role | No XML Tags | With XML Tags |
| ----- | ----- | ----- |
| User | You’re a financial analyst at AcmeCorp. Generate a Q2 financial report for our investors. Include sections on Revenue Growth, Profit Margins, and Cash Flow, like with this example from last year: {{Q1\_REPORT}}. Use data points from this spreadsheet: {{SPREADSHEET\_DATA}}. The report should be extremely concise, to the point, professional, and in list format. It should and highlight both strengths and areas for improvement. | You’re a financial analyst at AcmeCorp. Generate a Q2 financial report for our investors. AcmeCorp is a B2B SaaS company. Our investors value transparency and actionable insights. Use this data for your report:\<data\>{{SPREADSHEET\_DATA}}\</data\> \<instructions\> 1\. Include sections: Revenue Growth, Profit Margins, Cash Flow. 2\. Highlight strengths and areas for improvement. \</instructions\> Make your tone concise and professional. Follow this structure: \<formatting\_example\>{{Q1\_REPORT}}\</formatting\_example\> |
| Assistant | Q2 Financial Report for AcmeCorp Investors Dear Valued Investors, I am pleased to present our Q2 financial report, showcasing AcmeCorp’s continued growth and resilience in the B2B SaaS market. 1\. Revenue Growth: Our Q2 revenue reached $15.2M, a 22% YoY increase. This growth is primarily driven by a 30% expansion in our enterprise client base. However, our SMB segment saw a slight decline of 5%, which we aim to address through targeted marketing initiatives in Q3. 2\. Profit Margins: Gross margin improved to 72% (up 3% from Q1) due to infrastructure optimizations. EBITDA margin, however, dipped to 18% (down 2%) as we invested heavily in R\&D for our upcoming AI-driven features. 3\. Cash Flow: Operating cash flow remains strong at $4.1M. Our cash reserves stand at $28M, providing a 15-month runway at current burn rate. We did see a 20% increase in customer acquisition costs, which we’re addressing through more efficient sales strategies. In summary, AcmeCorp’s core financials remain robust. We’re balancing growth investments with prudent cash management. Our focus for Q3 will be revitalizing SMB growth and optimizing sales efficiency. Thank you for your continued trust. Sincerely, CFO, AcmeCorp | Q2 Financial Report for AcmeCorp Investors\</output\> Revenue Growth: \- Q2 revenue: $15.2M (22% YoY ↑) \- Enterprise clients: 30% ↑ \- SMB segment: 5% ↓ Action: Targeted Q3 marketing Profit Margins: \- Gross margin: 72% (3% ↑ from Q1) Reason: Infrastructure optimizations \- EBITDA margin: 18% (2% ↓) Reason: R\&D investment in AI features Cash Flow: \- Operating cash flow: $4.1M (strong) \- Cash reserves: $28M (15-month runway) \- Customer acquisition cost: 20% ↑ Action: Optimize sales strategies Outlook: \- Core financials: Robust \- Q3 focus: Revitalize SMB, optimize sales Management remains committed to balancing growth investments with financial discipline |

Without XML tags, Claude’s analysis is disorganized and misses key points. With tags, it provides a structured, thorough analysis that a legal team can act on.

| Role | No XML Tags | With XML Tags |
| ----- | ----- | ----- |
| User | Analyze this software licensing agreement for potential risks and liabilities: {{CONTRACT}}. Focus on indemnification, limitation of liability, and IP ownership clauses. Also, note any unusual or concerning terms. Here’s our standard contract for reference: {{STANDARD\_CONTRACT}}. Give a summary of findings and recommendations for our legal team. | Analyze this software licensing agreement for legal risks and liabilities. We’re a multinational enterprise considering this agreement for our core data infrastructure. \<agreement\> {{CONTRACT}}\</agreement\> This is our standard contract for reference: \<standard\_contract\>{{STANDARD\_CONTRACT}}\</standard\_contract\> \<instructions\> 1\. Analyze these clauses: \- Indemnification \- Limitation of liability \- IP ownership 2\. Note unusual or concerning terms. 3\. Compare to our standard contract. 4\. Summarize findings in \<findings\> tags. 5\. List actionable recommendations in \<recommendations\> tags.\</instructions\> |
| Assistant | The provided software licensing agreement presents several concerning aspects. The indemnification clause is overly broad, potentially exposing us to significant liabilities. The limitation of liability section caps damages at a mere $500, which is inadequate for our enterprise-level usage. Regarding IP, the agreement grants the vendor joint ownership of any modifications or integrations we create. In summary, this agreement is not in our best interest. It exposes us to undue risk, limits our recourse in case of failures, and compromises our intellectual property rights. I recommend renegotiating these terms or seeking alternative vendors. | \<findings\> 1\. Indemnification (Clause 8): \- Issue: Overly broad. We indemnify vendor against “any and all claims” arising from our use. \- Risk: Could hold us liable even for vendor’s negligence or product defects. \- Deviation: Our standard limits indemnity to claims arising from our violation of agreement. 2\. Limitation of Liability (Clause 9): \- Issue: Caps all damages at $500, including direct damages. \- Risk: Grossly inadequate for enterprise use. A critical failure could cost millions. \- Deviation: Our standard allows for direct damages up to 12 months of fees paid. 3\. IP Ownership (Clause 12): \- Issue: Grants vendor joint ownership of our modifications/integrations. \- Risk: Vendor could use or sell our proprietary algorithms or data insights. \- Deviation: Our standard retains full ownership of our work. 4\. Unusual Terms: \- Clause 5.3: Vendor can use our usage data for “any purpose.” \- Clause 7.2: Vendor can terminate for “convenience” with only 7 days’ notice. \- Clause 11: No warranties of any kind, even for basic merchantability. \</findings\> \<recommendations\> 1\. Reject this agreement. Risks far outweigh benefits for an enterprise. 2\. Counter-propose: \- Indemnification: Limit to claims arising from our violation of agreement. \- Liability: Cap at 12 months’ fees for direct damages; negotiate for indirect. \- IP: Full ownership of our modifications/integrations. \- Data Use: Restrict to service improvement only. \- Termination: Minimum 90 days’ notice; only for cause. \- Warranties: Demand basic merchantability and fitness for purpose. 3\. If vendor refuses, explore alternative providers or in-house solutions. 4\. Engage legal counsel for contract negotiation given high stakes. \</recommendations\> |

**Giving Claude a role with a system prompt**

Copy page  
While these tips apply broadly to all Claude models, you can find prompting tips specific to extended thinking models [here](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/extended-thinking-tips).

When using Claude, you can dramatically improve its performance by using the system parameter to give it a role. This technique, known as role prompting, is the most powerful way to use system prompts with Claude.

The right role can turn Claude from a general assistant into your virtual domain expert\!

System prompt tips: Use the system parameter to set Claude’s role. Put everything else, like task-specific instructions, in the user turn instead.

## [**​**](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/system-prompts#why-use-role-prompting%3F)

## **Why use role prompting?**

* Enhanced accuracy: In complex scenarios like legal analysis or financial modeling, role prompting can significantly boost Claude’s performance.  
* Tailored tone: Whether you need a CFO’s brevity or a copywriter’s flair, role prompting adjusts Claude’s communication style.  
* Improved focus: By setting the role context, Claude stays more within the bounds of your task’s specific requirements.

---

## [**​**](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/system-prompts#how-to-give-claude-a-role)

## **How to give Claude a role**

Use the system parameter in the [Messages API](https://docs.claude.com/en/api/messages) to set Claude’s role:

Copy  
import anthropic

client \= anthropic.Anthropic()

response \= client.messages.create(  
    model\="claude-3-7-sonnet-20250219",  
    max\_tokens\=2048,  
    system\="You are a seasoned data scientist at a Fortune 500 company.", \# \<-- role prompt  
    messages\=\[  
        {"role": "user", "content": "Analyze this dataset for anomalies: \<dataset\>{{DATASET}}\</dataset\>"}  
    \]  
)

print(response.content)

Role prompting tip: Experiment with roles\! A data scientist might see different insights than a marketing strategist for the same data. A data scientist specializing in customer insight analysis for Fortune 500 companies might yield different results still\!  
---

## [**​**](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/system-prompts#examples)

## **Examples**

### [**​**](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/system-prompts#example-1%3A-legal-contract-analysis)

### **Example 1: Legal contract analysis**

Without a role, Claude might miss critical issues:

| Role | Content |
| ----- | ----- |
| User | Analyze this software licensing agreement for potential risks: \<contract\> {{CONTRACT}} \</contract\> Focus on indemnification, liability, and IP ownership. |
| Assistant | Here’s a summary of the key points in the software licensing agreement: 1\. Indemnification (Section 8): \- We indemnify the vendor against claims arising from our use. 2\. Limitation of Liability (Section 9): \- Damages capped at $500. 3\. IP Ownership (Section 12): \- We retain ownership of our modifications. Overall, the agreement seems standard. The indemnification and liability clauses are typical, and we maintain our IP rights. |

With a role, Claude catches critical issues that could cost millions:

| Role | Content |
| ----- | ----- |
| User | You are the General Counsel of a Fortune 500 tech company. We’re considering this software licensing agreement for our core data infrastructure: \<contract\> {{CONTRACT}} \</contract\> Analyze it for potential risks, focusing on indemnification, liability, and IP ownership. Give your professional opinion. |
| Assistant | I’ve reviewed the software licensing agreement, and I have serious concerns that could expose our company to significant risks: 1\. Indemnification (Section 8): \- Critical Issue: We indemnify the vendor against “any and all claims” arising from our use. \- Risk: This could hold us liable even for the vendor’s negligence or product defects. \- Recommendation: Reject. Limit our indemnity to claims arising from our violation of the agreement. 2\. Limitation of Liability (Section 9): \- Critical Issue: Damages capped at $500, including direct damages. \- Risk: Grossly inadequate. A critical failure in our data infrastructure could cost us millions in lost revenue and reputational damage. \- Recommendation: Reject. Negotiate for cap at 12 months of fees for direct damages, and carve-outs for data breaches. 3\. IP Ownership (Section 12): \- Critical Issue: Vendor gains joint ownership of our modifications and integrations. \- Risk: They could use or sell our proprietary algorithms or data insights to competitors. \- Recommendation: Reject. We must retain full ownership of our work. Professional Opinion: Do not sign this agreement. It is grossly unfavorable and exposes us to unacceptable levels of risk. If the vendor refuses to renegotiate these terms, I strongly advise exploring alternative providers or accelerating our in-house solution. The potential costs of proceeding with this agreement far outweigh any short-term gains. |

### **Example 2: Financial analysis**

Without a role, Claude’s analysis lacks depth:

| Role | Content |
| ----- | ----- |
| User | Analyze this dataset of our Q2 financials: \<data\> {{FINANCIALS}} \</data\> Highlight key trends and recommend actions. |
| Assistant | Here’s a summary of your Q2 financials: 1\. Revenue: $15.2M, up 22% YoY. Enterprise client base grew 30%. 2\. Gross Margin: 72%, up 3% from Q1. 3\. EBITDA Margin: 18%, down 2% due to R\&D investments. 4\. Cash Flow: $4.1M operating, $28M in reserves. Overall, financials look strong with revenue growth and healthy margins. Increased R\&D spending is impacting profitability but could pay off long-term. Maintain current course. |

With a role, Claude delivers actionable insights:

| Role | Content |
| ----- | ----- |
| User | You are the CFO of a high-growth B2B SaaS company. We’re in a board meeting discussing our Q2 financials: \<data\> {{FINANCIALS}} \</data\> Analyze key trends, flag concerns, and recommend strategic actions. Our investors want aggressive growth but are wary of our burn rate. |
| Assistant | Board members, here’s my analysis of our Q2 financials: 1\. Revenue ($15.2M, \+22% YoY): \- Insight: Enterprise growth (+30%) is outpacing overall growth. \- Flag: SMB segment declined 5%. \- Action: Reallocate 20% of SMB marketing budget to enterprise sales. Task product to simplify SMB onboarding. 2\. Margins (Gross: 72%, \+3% QoQ; EBITDA: 18%, \-2% QoQ): \- Insight: Infrastructure optimizations boosted gross margins. \- Flag: R\&D spend on AI features dented EBITDA. \- Action: No change. Our AI roadmap is critical for enterprise stickiness. 3\. Cash ($4.1M OCF, $28M reserves): \- Insight: 15-month runway at current burn. \- Flag: CAC up 20%, eroding LTV/CAC. \- Action: Freeze non-essential hires. Implement sales funnel analytics to cut CAC by 15% in Q3. Strategic Stance: We’re threading the needle between growth and burn. Enterprise focus is our growth engine—invest there. But watch SMB churn; it could bleed into enterprise. Our AI bet is sound, but we must convert it to ARR by Q4, or we cut R\&D by 30%. In sum: Double down on enterprise, streamline SMB, optimize sales, and monetize AI. Questions? |

**Prefill Claude's response for greater output control**

Copy page  
While these tips apply broadly to all Claude models, you can find prompting tips specific to extended thinking models [here](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/extended-thinking-tips).  
Prefilling is only available for non-extended thinking modes. It’s not currently supported with extended thinking.

When using Claude, you have the unique ability to guide its responses by prefilling the Assistant message. This powerful technique allows you to direct Claude’s actions, skip preambles, enforce specific formats like JSON or XML, and even help Claude maintain character consistency in role-play scenarios.

In some cases where Claude is not performing as expected, a few prefilled sentences can vastly improve Claude’s performance. A little prefilling goes a long way\!

## [**​**](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/prefill-claudes-response#how-to-prefill-claude%E2%80%99s-response)

## **How to prefill Claude’s response**

To prefill, include the desired initial text in the Assistant message (Claude’s response will continue from where the Assistant message leaves off):

Copy  
import anthropic

client \= anthropic.Anthropic()  
response \= client.messages.create(  
    model\="claude-sonnet-4-5",  
    max\_tokens\=1024,  
    messages\=\[  
        {"role": "user", "content": "What is your favorite color?"},  
        {"role": "assistant", "content": "As an AI assistant, I don't have a favorite color, But if I had to pick, it would be green because"}  \# Prefill here  
    \]  
)

The prefill content cannot end with trailing whitespace. A prefill like "As an AI assistant, I " (with a space at the end) will result in an error.

### [**​**](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/prefill-claudes-response#examples)

### **Examples**

#### [**​**](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/prefill-claudes-response#example-1%3A-controlling-output-formatting-and-skipping-the-preamble)

#### **Example 1: Controlling output formatting and skipping the preamble**

Power user tip: Prefilling { forces Claude to skip the preamble and directly output the JSON object. This is cleaner, more concise, and easier for programs to parse without additional processing.

| Role | Content |
| ----- | ----- |
| User | Extract the name, size, price, and color from this product description as a JSON object: \<description\> The SmartHome Mini is a compact smart home assistant available in black or white for only $49.99. At just 5 inches wide, it lets you control lights, thermostats, and other connected devices via voice or app—no matter where you place it in your home. This affordable little hub brings convenient hands-free control to your smart devices. \</description\> |
| Assistant | Here’s the extracted information in JSON format: \`\`\`json { “name”: “SmartHome Mini”, “size”: “5 inches wide”, “price”: “$49.99”, “colors”: \[“black”, “white”\] } \`\`\` I’ve extracted the following details from the product description: \- Name: SmartHome Mini \- Size: 5 inches wide \- Price: $49.99 \- Colors: Available in black and white The JSON object provides a structured format that’s easy for programs to parse and use. Let me know if you need any modifications or have any other questions\! |

| Role | Content |
| ----- | ----- |
| User | Extract the name, size, price, and color from this product description as a JSON object: \<description\> The SmartHome Mini is a compact smart home assistant available in black or white for only $49.99. At just 5 inches wide, it lets you control lights, thermostats, and other connected devices via voice or app—no matter where you place it in your home. This affordable little hub brings convenient hands-free control to your smart devices. \</description\> |
| Assistant (prefill) | { |
| Assistant (Claude’s response) | “name”: “SmartHome Mini”, “size”: “5 inches wide”, “price”: “$49.99”, “colors”: \[ “black”, “white” \] } |

#### [**​**](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/prefill-claudes-response#example-2%3A-maintaining-character-in-roleplay-scenarios)

#### **Example 2: Maintaining character in roleplay scenarios**

Role-play tip: Prefilling a bracketed \[ROLE\_NAME\] can remind Claude stay in character, even for longer and more complex conversations. This is especially powerful when combined with role prompting in the system parameter.

| Role | Content |
| ----- | ----- |
| User (50 conversation turns in with “Sherlock Holmes” Claude) | What do you deduce about the owner of this shoe? \<image\>muddy\_shoe.jpg\</image\> |
| Assistant | As an AI assistant, I would be happy to analyze the image of a muddy shoe as if you had provided it. Here’s my deduction… |

| Role | Content |
| ----- | ----- |
| User (50 conversation turns in with “Sherlock Holmes” Claude) | What do you deduce about the owner of this shoe? \<image\>muddy\_shoe.jpg\</image\> |
| Assistant (prefill) | \[Sherlock Holmes\] |
| Assistant (Claude’s response) | Ah, what have we here? A most curious specimen, Watson\! Let us examine this shoe with a discerning eye. The mud, you see, is not your common London clay, but rather the distinctive reddish hue of the iron-rich soil found only in the environs of Hampstead Heath. And yet, the wear on the sole suggests a gait more suited to the cobblestones of Whitechapel than the gentle slopes of the Heath. Now, observe the laces\! They are tied with a particular knot favored by those in the medical profession—doubtless a habit acquired during years of tying surgical gowns. But the scuff marks on the toe box tell a different tale: they are consistent with the kicking motion one might employ in the martial arts, specifically Baritsu. We may conclude, then, that our absent shoe owner is a doctor, possibly a surgeon, who resides in Whitechapel but frequents Hampstead Heath—perhaps for a secret Baritsu practice, away from prying eyes. A most intriguing case, Watson\! We must make haste; the game is afoot\! |

**Chain complex prompts for stronger performance**

Copy page  
While these tips apply broadly to all Claude models, you can find prompting tips specific to extended thinking models [here](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/extended-thinking-tips).

When working with complex tasks, Claude can sometimes drop the ball if you try to handle everything in a single prompt. Chain of thought (CoT) prompting is great, but what if your task has multiple distinct steps that each require in-depth thought?

Enter prompt chaining: breaking down complex tasks into smaller, manageable subtasks.

## [**​**](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/chain-prompts#why-chain-prompts%3F)

## **Why chain prompts?**

1. Accuracy: Each subtask gets Claude’s full attention, reducing errors.  
2. Clarity: Simpler subtasks mean clearer instructions and outputs.  
3. Traceability: Easily pinpoint and fix issues in your prompt chain.

---

## [**​**](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/chain-prompts#when-to-chain-prompts)

## **When to chain prompts**

Use prompt chaining for multi-step tasks like research synthesis, document analysis, or iterative content creation. When a task involves multiple transformations, citations, or instructions, chaining prevents Claude from dropping or mishandling steps.

Remember: Each link in the chain gets Claude’s full attention\!

Debugging tip: If Claude misses a step or performs poorly, isolate that step in its own prompt. This lets you fine-tune problematic steps without redoing the entire task.  
---

## [**​**](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/chain-prompts#how-to-chain-prompts)

## **How to chain prompts**

1. Identify subtasks: Break your task into distinct, sequential steps.  
2. Structure with XML for clear handoffs: Use XML tags to pass outputs between prompts.  
3. Have a single-task goal: Each subtask should have a single, clear objective.  
4. Iterate: Refine subtasks based on Claude’s performance.

### [**​**](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/chain-prompts#example-chained-workflows%3A)

### **Example chained workflows:**

* Multi-step analysis: See the legal and business examples below.  
* Content creation pipelines: Research → Outline → Draft → Edit → Format.  
* Data processing: Extract → Transform → Analyze → Visualize.  
* Decision-making: Gather info → List options → Analyze each → Recommend.  
* Verification loops: Generate content → Review → Refine → Re-review.

Optimization tip: For tasks with independent subtasks (like analyzing multiple docs), create separate prompts and run them in parallel for speed.

### [**​**](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/chain-prompts#advanced%3A-self-correction-chains)

### **Advanced: Self-correction chains**

You can chain prompts to have Claude review its own work\! This catches errors and refines outputs, especially for high-stakes tasks.

#### **Prompt 1**

| Role | Content |
| ----- | ----- |
| User | Summarize this medical research paper. \<paper\>{{RESEARCH\_PAPER}}\</paper\> Focus on methodology, findings, and clinical implications. |
| Assistant {{SUMMARY}} | Methodology: Double-blind RCT with 500 Type 2 diabetes patients. Group A (n=250) received novel GLP-1/GIP dual agonist; Group B (n=250) received standard GLP-1 agonist. 24-week trial, primary endpoint: HbA1c reduction. Findings: \- Group A: 1.8% mean HbA1c reduction \- Group B: 1.1% mean HbA1c reduction \- 68% of Group A vs. 52% of Group B achieved HbA1c \<7% \- Group A: 5.2kg mean weight loss \- Group B: 3.1kg mean weight loss Safety: Similar adverse event profiles, no serious events attributed to treatment. Clinical Implications: Dual agonist shows superior glycemic control and weight loss compared to standard therapy. Could be a game-changer, especially for obese diabetics. |

#### [**​**](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/chain-prompts#prompt-2)

#### **Prompt 2**

| Role | Content |
| ----- | ----- |
| User | Your task is to provide feedback on a research paper summary. Here is a summary of a medical research paper: \<summary\> {{SUMMARY}} \</summary\> Here is the research paper: \<paper\> {{RESEARCH\_PAPER}} \</paper\> Review this summary for accuracy, clarity, and completeness on a graded A-F scale. |
| Assistant {{FEEDBACK}} | 1\. Accuracy: A \- Correctly reported key stats: HbA1c reductions, weight loss. \- Accurately noted safety profile and lack of serious adverse events. \- Assertion of “game-changer” is justified by significantly better outcomes. 2\. Clarity: A- \- Concise and well-structured with clear sections. \- Good use of comparative language (e.g., “up 3% from Q1”) for context. \- Minor issue: Acronyms like “RCT,” “GLP-1,” and “GIP” not defined. Consider spelling out first use. 3\. Completeness: B+ \- Covers all requested areas: methodology, findings, clinical implications. \- Missing: Baseline characteristics of groups (were they well-matched?). \- Missing: Any secondary endpoints (e.g., blood pressure, lipids). \- Consider: Long-term implications or need for further research. Overall, the summary is accurate and clear, providing key insights for a quick grasp of the study. To elevate to A+, define acronyms, mention group baseline stats, note any secondary outcomes, and briefly touch on the need for long-term studies. |

#### [**​**](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/chain-prompts#prompt-3)

#### **Prompt 3**

| Role | Content |
| ----- | ----- |
| User | Your task is to improve a paper summary given feedback. Here is the first draft of a medical research paper: \<summary\> {{SUMMARY}} \</summary\> Here is the research paper: \<paper\> {{RESEARCH\_PAPER}} \</paper\> Here is the feedback: \<feedback\> {{FEEDBACK}} \</feedback\> Update the summary based on the feedback. |
| Assistant | Methodology: Double-blind randomized controlled trial (RCT) with 500 Type 2 diabetes patients. Group A (n=250) received a novel glucagon-like peptide-1/glucose-dependent insulinotropic polypeptide (GLP-1/GIP) dual agonist; Group B (n=250) received a standard GLP-1 agonist. The 24-week trial’s primary endpoint was HbA1c reduction. Groups were well-matched for age, BMI, and baseline HbA1c. Findings: \- Group A: 1.8% mean HbA1c reduction \- Group B: 1.1% mean HbA1c reduction \- 68% of Group A vs. 52% of Group B achieved HbA1c \<7% \- Group A: 5.2kg mean weight loss \- Group B: 3.1kg mean weight loss Secondary endpoints showed improvements in blood pressure and lipid profiles for both groups, with Group A showing slightly better results. Safety: Similar adverse event profiles, with no serious events attributed to either treatment. Clinical Implications: The dual GLP-1/GIP agonist demonstrates superior glycemic control and weight loss compared to standard GLP-1 therapy. These results suggest it could be a significant advancement, particularly for obese diabetics. However, longer-term studies are needed to confirm sustained efficacy and safety, as well as to investigate potential benefits on cardiovascular outcomes. |

**Long context prompting tips**

Copy page  
While these tips apply broadly to all Claude models, you can find prompting tips specific to extended thinking models [here](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/extended-thinking-tips).

Claude’s extended context window (200K tokens for Claude 3 models) enables handling complex, data-rich tasks. This guide will help you leverage this power effectively.

## [**​**](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/long-context-tips#essential-tips-for-long-context-prompts)

## **Essential tips for long context prompts**

* Put longform data at the top: Place your long documents and inputs (\~20K+ tokens) near the top of your prompt, above your query, instructions, and examples. This can significantly improve Claude’s performance across all models.  
* Queries at the end can improve response quality by up to 30% in tests, especially with complex, multi-document inputs.  
* Structure document content and metadata with XML tags: When using multiple documents, wrap each document in \<document\> tags with \<document\_content\> and \<source\> (and other metadata) subtags for clarity.

## **Essential tips for long context prompts**

* Put longform data at the top: Place your long documents and inputs (\~20K+ tokens) near the top of your prompt, above your query, instructions, and examples. This can significantly improve Claude’s performance across all models.  
* Queries at the end can improve response quality by up to 30% in tests, especially with complex, multi-document inputs.  
* Structure document content and metadata with XML tags: When using multiple documents, wrap each document in \<document\> tags with \<document\_content\> and \<source\> (and other metadata) subtags for clarity.  
* Example multi-document structure  
* Copy

\<documents\>  
  \<document index\="1"\>  
    \<source\>annual\_report\_2023.pdf\</source\>  
    \<document\_content\>  
      {{ANNUAL\_REPORT}}  
    \</document\_content\>  
  \</document\>  
  \<document index\="2"\>  
    \<source\>competitor\_analysis\_q2.xlsx\</source\>  
    \<document\_content\>  
      {{COMPETITOR\_ANALYSIS}}  
    \</document\_content\>  
  \</document\>  
\</documents\>

Analyze the annual report and competitor analysis. Identify strategic advantages and recommend Q3 focus areas.

*   
*   
* Ground responses in quotes: For long document tasks, ask Claude to quote relevant parts of the documents first before carrying out its task. This helps Claude cut through the “noise” of the rest of the document’s contents.

Example quote extraction  
You are an AI physician's assistant. Your task is to help doctors diagnose possible patient illnesses.

\<documents\>  
  \<document index\="1"\>  
    \<source\>patient\_symptoms.txt\</source\>  
    \<document\_content\>  
      {{PATIENT\_SYMPTOMS}}  
    \</document\_content\>  
  \</document\>  
  \<document index\="2"\>  
    \<source\>patient\_records.txt\</source\>  
    \<document\_content\>  
      {{PATIENT\_RECORDS}}  
    \</document\_content\>  
  \</document\>  
  \<document index\="3"\>  
    \<source\>patient01\_appt\_history.txt\</source\>  
    \<document\_content\>  
      {{PATIENT01\_APPOINTMENT\_HISTORY}}  
    \</document\_content\>  
  \</document\>  
\</documents\>

Find quotes from the patient records and appointment history that are relevant to diagnosing the patient's reported symptoms. Place these in \<quotes\> tags. Then, based on these quotes, list all information that would help the doctor diagnose the patient's symptoms. Place your diagnostic information in \<info\> tags.  
