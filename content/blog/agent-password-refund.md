# Your Agent Has Your Password. Who Has Your Refund?

> **TL;DR** — Four protocols shipped in ten months. Every one proves you authorized your agent. Not one says who pays when it gets it wrong. And Reg E only covers transfers you *didn't* authorize — so the proof is the trap. Six parties could have closed that gap. All six passed.

---

You set it up on a Tuesday night. A spending limit, a couple of rules, a signature you barely notice giving. Around three in the morning your agent buys something — the wrong item, or a subscription you canceled in March, or exactly what a malicious web page told it to buy while you slept.

You call your bank in the morning.

And the bank does something no bank has ever been able to do quite this cleanly: it produces cryptographic proof that you authorized this agent to act for you.

That proof isn't the start of your dispute. It's probably the end of it.

I should say up front that I'm building a consumer app that aggregates bank, card and investment data — which makes me one more party in the chain I'm about to describe. Factor that in. I'd rather say it first than have it land as a reveal.

## Human Not Present

None of this is a 2030 thought experiment. In about ten months, the authorisation layer for agentic payments went from conference slides to production.

Google published [AP2](https://cloud.google.com/blog/products/ai-machine-learning/announcing-agents-to-payments-ap2-protocol) in September 2025 with sixty-plus partners, then [handed it to the FIDO Alliance](https://fidoalliance.org/fido-alliance-to-develop-standards-for-trusted-ai-agent-interactions/) in April 2026 for open governance. Stripe and OpenAI shipped the [Agentic Commerce Protocol](https://stripe.com/blog/developing-an-open-standard-for-agentic-commerce) the same month AP2 launched — the same day Instant Checkout went live in ChatGPT. Visa followed in October with its Trusted Agent Protocol. Mastercard shipped [Agent Pay for Machines](https://www.mastercard.com/us/en/news-and-trends/press/2026/june/mastercard-launches-agent-pay-for-machines.html) in June 2026.

AP2 is the one worth understanding, because it's the most honest about what it does. Three cryptographically signed **Mandates** — Intent, Cart, Payment — as W3C Verifiable Credentials. The Intent Mandate is where it gets interesting: it supports what the spec calls a **Human Not Present** flow. You pre-sign an intent with price limits and conditions. Your agent executes against it later. Nobody is watching.

This is genuinely good engineering. It solves a hard problem — how does a merchant know the software at its door really speaks for the human it claims to represent? — and solves it well. Non-repudiable, auditable, clean.

From the consumer's side, it's also the problem.

## Is this really the agent the cardholder authorized?

Regulation E protects you against ***unauthorized*** electronic fund transfers. That one word carries the entire weight.

Under [12 C.F.R. §1005.2(m)](https://www.ecfr.gov/current/title-12/chapter-X/part-1005/subpart-A/section-1005.2), an unauthorized transfer has three parts: initiated by someone *other than you*, *without actual authority*, and *from which you receive no benefit*. The liability caps and the error-resolution rights at §1005.11 — the machinery that actually makes you whole — hang off that definition and nothing else.

Now hold that up against Tuesday night. A signed mandate is about as clean a grant of actual authority as anyone has ever produced. And when your agent buys the wrong thing, you usually still get the thing — so even the no-benefit prong cuts against you. The access device exception does the rest: hand over the keys, and the loss may be yours.

No court has ruled on any of this. I want to be careful there, because the honest claim isn't "consumers have lost their remedy." It's that nobody knows, and the not-knowing *is* the finding. The statute predates the technology by four decades, and the first consumer to learn the answer will learn it the expensive way.

Here's the inversion at the center of it. Old authentication asks: *is this really the cardholder?* Agentic authentication asks: *is this really the agent the cardholder authorized?* Those sound like the same question. In effect they're opposites. Answering the first one **yes** protects you. Answering the second one **yes** forecloses your best remedy.

John Lande — a banking attorney at Dickinson Bradshaw who chairs the firm's cybersecurity practice and spends his days advising financial institutions on fraud exposure — [put it plainly](https://www.dickinsonbradshaw.com/blogs-articles/2026/01/20/new-reg-e-liability-the-ai-bought-that-not-me) in January 2026: *"Someone is going to be left holding the bag for agentic AI misfiring."* Worth noting who's saying that. Not a consumer advocate predicting harm — the banks' own counsel, looking at the same hole.

And there's a jagged edge nobody has touched. An agent talked into a purchase by a malicious page — prompt injection — is neither cleanly authorized nor cleanly unauthorized. You granted authority. You didn't grant *that*. There's no law on it, and no protocol I've read even gestures at it.

## How about liability? Six parties. Six deferrals.

This is the part that changed how I think about the problem. The gap isn't an oversight. Six different parties looked straight at it and deferred.

**The rule.** When the CFPB finalised its [§1033 personal financial data rule](https://www.federalregister.gov/documents/2024/11/18/2024-25079/required-rulemaking-on-personal-financial-data-rights) in 2024, it declined to allocate liability — not for lack of asking. Data providers asked. A trade association asked. An academic asked. *A consumer advocate asked.* The answer: institutions should rely on appropriately developed private network rules.

**The protocols.** AP2 defers liability and dispute resolution to "industry rules and standards." ACP, Visa's TAP and Mastercard's Agent Pay do the equivalent. All of them solve authorisation with real rigour. None allocates loss.

**The CFPB, again.** In [May 2025](https://www.federalregister.gov/documents/2025/05/12/2025-08286/interpretive-rules-policy-statements-and-advisory-opinions-withdrawal) it withdrew Circulars 2022-03 and 2023-03 — its guidance on algorithmic and AI-driven adverse action — as part of a bulk withdrawal of 67 documents. Its [public AI page](https://www.consumerfinance.gov/ai/) is now devoted entirely to the Bureau's internal use of AI, and states: *"CFPB has no AI use cases to report."*

**The prudential regulators.** In [April 2026](https://www.occ.gov/news-issuances/news-releases/2026/nr-occ-2026-29.html) the Fed, OCC and FDIC revised model-risk guidance for the first time since 2011 — and put generative and agentic AI **explicitly out of scope**, on the reasoning that they're novel and fast-moving and need their own framework. To their credit, they've promised a request for information on exactly that. Promised. Not published.

**The consumer advocates.** Consumer Reports published a 108-page [landscape analysis](https://innovation.consumerreports.org/wp-content/uploads/2026/04/AI-in-Consumer-Finance-Landscape-Analysis.pdf) of AI in consumer finance in April 2026. It mentions Reg E, Reg Z, UDAAP, EFTA and §1033 a combined **zero times**. I ran the search twice because I didn't believe it. The [Consumer Finance AI Standard](https://advocacy.consumerreports.org/press_release/consumer-reports-unveils-consumer-finance-ai-standard-a-first-of-its-kind-framework-defining-what-consumers-are-owed-from-ai-powered-financial-products) that followed in June is voluntary by design. Delicia Hand, who leads the work, [told The Financial Brand](https://thefinancialbrand.com/news/customer-experience-banking/who-will-protect-banking-consumers-rights-in-the-age-of-ai-consumer-reports-has-thoughts-198617): *"We're not necessarily looking for the standards to be taken up by regulators."*

**The industry.** The Consumer Bankers Association [white-papered this exact gap](https://consumerbankers.com/research/agentic-ai-payments-navigating-consumer-protection-innovation-and-regulatory-frameworks/) in January 2026, concluded statutory change was unlikely, and proposed — self-regulation through private network rules.

One more for completeness: FDX [launched an agentic AI initiative](https://financialdataexchange.org/fdx-feed/as-ai-agents-get-involved-in-financial-data-sharing-leading-standards-body-launches-initiative-to-stay-ahead/) in April 2026 and closed its Call for Input on May 29. No standard has been published.

Line those up and the shape is unmistakable. Everyone deferred to "industry rules and standards" that don't exist. The consumer is the residual claimant on a question nobody has answered.

Meanwhile the §1033 rule itself is enjoined — *Forcht Bank, N.A. v. CFPB*, [entered October 2025](https://bankingjournal.aba.com/2025/11/kentucky-federal-court-enjoins-cfpb-from-enforcing-current-1033-final-rule/) in the Eastern District of Kentucky — and back at the Bureau for a rewrite. Subpart D never took effect, so nothing was taken from consumers that they had. What the injunction did was foreclose the only US rule that would have meaningfully limited what aggregators may do with the access you grant them.

## Builders gonna build … the easy bit.

Fair objection, and it deserves a real answer — particularly from me, since I'm one of the vendors.

You can supervise aggregators. Mandate SOC 2. Ban credential sharing, require verified agent identities, demand attestation at every hop. **All of it is worth doing.** I'm not making the argument that compliance is too heavy. Fiduciary duty, GLBA, Reg E, SOC 2 exist because people's money is at stake, and they *should* be expensive.

My argument is narrower: the wrong things are getting the rigour. Nothing on that list allocates loss.

Verification tells you *who acted*. It doesn't tell you *who pays*.

And I think I know why we keep building the first one. We always solve the easy part first — the *how*. It's the fun part. The cryptography. The signed mandates. The chain of custody, the tracing, the handoff across six systems that all have to agree. That work is hard in the way engineers enjoy: tractable, testable, demo-able. It has a right answer.

The other part isn't technical at all. It's deciding who eats the loss. It's splitting the hair between an agent authorized to buy something and an agent that bought *that* something. It's drawing a line and then defending it to whoever lands on the wrong side. No elegant solution, no test suite, no standing ovation at a conference. So it doesn't get built — and everyone points at the genuinely beautiful thing they *did* build and calls the job done.

> Verification is a security control. Liability is a remedy. The industry keeps shipping the first and calling it the second.

There's a workable way to allocate this loss without waiting on Congress. That's its own piece, not three rushed paragraphs at the end of this one.

## And the consumer? You own the data. That's all you own.

The statute at the center of all this is called, in full, **Personal Financial Data Rights**. You nominally own the data. In the scenario I opened with, you have no leverage over anyone in the chain and quite possibly no remedy against any of them.

That's ownership without power, and people feel it even when they can't cite the regulation. Consumer Reports asked more than 4,000 Americans whether current law protects them from AI risk in financial services; **57% said no**, and **fewer than one in ten** completely trust financial companies to use AI responsibly. Those aren't numbers about technology. They're numbers about recourse.

CR's standard includes a principle I keep coming back to — a **duty of vigor**: the idea that an AI financial product shouldn't just avoid harming you, it should actively work your side, surfacing the rights you have so you don't need to know the law yourself. Nobody is building that. We're building the exact inverse — systems that are exquisitely good at proving what you agreed to.

Which brings me back to my own seat in this. I'm building a product that adds one more party to the chain — one more entity holding access, one more link where something can go wrong and the loss comes to rest on whoever is least equipped to argue. That's not a flaw in the argument. It's the reason to make it. If I'm going to ask people to trust a new intermediary with their financial data, the least I owe them is honesty about what happens when the intermediary, or the agent, or the protocol, or the bank gets it wrong.

Right now the honest answer is: nobody knows. And everyone who could have answered decided it was someone else's question.

---

## Sources

**Law and rules**

- [12 C.F.R. §1005.2 — Regulation E definitions](https://www.ecfr.gov/current/title-12/chapter-X/part-1005/subpart-A/section-1005.2) (eCFR) · [CFPB copy](https://www.consumerfinance.gov/rules-policy/regulations/1005/2/) · [Part 1005 in full](https://www.ecfr.gov/current/title-12/chapter-X/part-1005), including §1005.11 error resolution
- [Required Rulemaking on Personal Financial Data Rights](https://www.federalregister.gov/documents/2024/11/18/2024-25079/required-rulemaking-on-personal-financial-data-rights) — the §1033 final rule, Federal Register
- *Forcht Bank, N.A. v. CFPB* (E.D. Ky.), preliminary injunction October 29, 2025, Judge Danny C. Reeves — [ABA Banking Journal](https://bankingjournal.aba.com/2025/11/kentucky-federal-court-enjoins-cfpb-from-enforcing-current-1033-final-rule/) · [Moore & Van Allen](https://www.mvalaw.com/data-points/cfpb-enjoined-from-enforcing-personal-financial-data-rights-rule-1033) · [American Banker](https://www.americanbanker.com/news/court-halts-compliance-with-cfpbs-final-open-banking-rule)
- [Interpretive Rules, Policy Statements, and Advisory Opinions; Withdrawal](https://www.federalregister.gov/documents/2025/05/12/2025-08286/interpretive-rules-policy-statements-and-advisory-opinions-withdrawal) — Federal Register, May 12, 2025 (the 67 documents) · [Holland & Knight summary](https://www.hklaw.com/en/insights/publications/2025/05/cfpb-rescinds-67-guidance-documents)
- [CFPB — Artificial Intelligence](https://www.consumerfinance.gov/ai/)
- [OCC news release](https://www.occ.gov/news-issuances/news-releases/2026/nr-occ-2026-29.html) and [Bulletin 2026-13](https://www.occ.gov/news-issuances/bulletins/2026/bulletin-2026-13.html) — revised interagency model risk management guidance, April 17, 2026 · analysis from [Sullivan & Cromwell](https://www.sullcrom.com/insights/memo/2026/April/OCC-Fed-FDIC-Issue-Revised-Guidance-Model-Risk-Management) and [Davis Polk](https://www.davispolk.com/insights/client-update/visual-memo-key-changes-under-federal-banking-agencies-revised-model-risk)

**Protocols**

- [Google — Agent Payments Protocol (AP2)](https://cloud.google.com/blog/products/ai-machine-learning/announcing-agents-to-payments-ap2-protocol), September 2025
- [FIDO Alliance — standards for trusted AI agent interactions](https://fidoalliance.org/fido-alliance-to-develop-standards-for-trusted-ai-agent-interactions/), April 2026 (AP2 contribution; Payments TWG chaired by Mastercard and Visa)
- [Stripe / OpenAI — Agentic Commerce Protocol](https://stripe.com/blog/developing-an-open-standard-for-agentic-commerce), September 2025
- [Mastercard — Agent Pay for Machines](https://www.mastercard.com/us/en/news-and-trends/press/2026/june/mastercard-launches-agent-pay-for-machines.html), June 10, 2026
- Visa — Trusted Agent Protocol, announced October 14, 2025

**Industry and advocacy**

- [Consumer Bankers Association / Davis Wright Tremaine — *Agentic AI Payments*](https://consumerbankers.com/research/agentic-ai-payments-navigating-consumer-protection-innovation-and-regulatory-frameworks/), January 2026
- [Consumer Reports — *AI in Consumer Finance: Landscape Analysis*](https://innovation.consumerreports.org/wp-content/uploads/2026/04/AI-in-Consumer-Finance-Landscape-Analysis.pdf) (PDF), April 2026
- [Consumer Reports — Consumer Finance AI Standard](https://advocacy.consumerreports.org/press_release/consumer-reports-unveils-consumer-finance-ai-standard-a-first-of-its-kind-framework-defining-what-consumers-are-owed-from-ai-powered-financial-products), June 2026 — source of the duty of vigor and the survey of 4,000+ consumers
- [The Financial Brand](https://thefinancialbrand.com/news/customer-experience-banking/who-will-protect-banking-consumers-rights-in-the-age-of-ai-consumer-reports-has-thoughts-198617) — Delicia Hand quote
- [FDX — agentic AI initiative](https://financialdataexchange.org/fdx-feed/as-ai-agents-get-involved-in-financial-data-sharing-leading-standards-body-launches-initiative-to-stay-ahead/), April 2026

**Practitioner view**

- [John Lande, Dickinson Bradshaw — *New Reg E Liability: "The AI Bought That, Not Me"*](https://www.dickinsonbradshaw.com/blogs-articles/2026/01/20/new-reg-e-liability-the-ai-bought-that-not-me), January 20, 2026
