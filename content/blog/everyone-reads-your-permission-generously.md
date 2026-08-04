# Everyone Reads Your Permission Generously

> **TL;DR** — The financial industry spent fourteen years fighting over §1033 only to cover basic bank accounts and credit cards. The data required to understand a complete financial picture — brokerages, retirements, and mortgages — was completely left out. Meanwhile, the access consumers do grant comes with zero guardrails: no declared scope, no committed duration, no guarantee that revoking access actually works. Regulators keep missing the mark, and the rest of the industry quietly capitalizes on the gap.

---

After more than two decades in fintech, I recently began building a product that relies on aggregated bank, card, and investment data. I have a horse in this race, and you deserve to know my bias upfront before reading any further.

Going into this, I expected the hard part to be the modeling. It wasn't. The modeling is the easy part — and surprisingly, so is the basic data access everyone spent a decade and a half arguing about.

## The code is commodity. The permission isn't.

SaaS is cheap. Today, one person can ship a consumer finance app. That Monte Carlo regression that looks so impressive from the outside? It's a commodity. Every tool in the category uses the exact same approach, sitting in open-source libraries that anyone can pull down.

So if the code isn't the moat, what is?

Three things, and none of them is engineering: getting to a customer, getting that customer's *data*, and being allowed to say anything useful about it. Permission to reach someone, permission to see their information, permission to advise them.

This piece is about the middle one.

## Banks share plenty. They just share what's easiest.

First, let's kill a lazy idea that banks refuse to share data. They share enormously. [FDX-standardized connections](https://financialdataexchange.org/fdx-feed/114-million-reasons-to-keep-moving-forward-on-industry-led-standard-for-secure-data-sharing/) grew straight through the litigation — hitting roughly 76 million in 2024, 114 million by spring 2025, and [north of 130 million](https://www.openbankingexpo.com/news/fdx-hails-milestone-in-consumer-accounts-using-its-api/) in early 2026. Plaid's own docs claim [over 10,000 institutions](https://plaid.com/docs/institutions/) across the US and Canada. (Though it's worth noting that number is inflated by brokerages, card issuers, crypto exchanges, payroll providers, and multiple entries per brand.) Either way, data is moving constantly, at a scale most people would find surprising.

But what's moving isn't a consumer right. It's a pile of bespoke deals, negotiated bilaterally, institution by institution, non-standard by construction. At the commercial layer, data access is a gradient: how much, how often, and on what terms, renegotiated whenever leverage shifts. But at the consumer layer — where a person is approving one specific thing — it collapses into a binary switch. Approve the checking account, and you hand over far more than just the checking account. No consumer would design it this way.

I don't think anyone sat down and decided to over-grant, though. Scoping access narrowly is work — you have to model what the consumer actually approved, carry it through every downstream call, and maintain it. Handing over everything behind the login is simply less to build. Nobody was required to do the harder version, so in places it didn't get done. That's the whole explanation, and it's somehow less comforting than malice.

## The level of access your consent grants is negotiated between two companies

Plaid's OAuth documentation says the flow "can provide the ability for end users to configure granular permissions on their Items." Their own example: a user might allow access to a checking account but not the credit card sitting behind the same login.

*Can.* Not does. Not must.

That one word is carrying an enormous amount of weight, and if you've spent any time around these integrations, you know exactly what it's covering. Granularity is a capability the standard makes available, and the implementing institution decides whether to honor it — how narrow the scope actually is, how long the grant lasts, what happens to the other channels sitting behind the same credential. FDX, the standards body, says the quiet part in its own framing: authorization, revocation and reauthorization are "left to market participants."

So consent looks like a switch to the person clicking it. What it actually reaches is a negotiated position between two companies, and the consumer isn't in the room for that conversation.

§1033 would have put an outer limit on exactly this — no access beyond one year without reauthorization. That died with the rule.

Revocation is the same story from the other end. Turning it off in an app is a request that has to propagate through every downstream system that ever received the data — a well-documented weak point in any architecture where consent is stored centrally but enforced locally. Every system downstream is an independent interpreter of a record it received once. When you revoke, you are trusting a chain you cannot see and nobody audits.

## Every institution sets its own terms, and none of them are published

Here is what surprised me most, all pulled straight from Plaid's own engineering documentation:

- **Data Hoarding:** Capital One doesn't provide pending transactions at all, and gives you only 90 days of history.
- **Artificial Throttling:** Charles Schwab permits exactly one active connection per end user, per application. One link per person, per app, full stop.
- **Arbitrary Expirations:** Re-consent clocks run from three months at Brex, to annual at most major banks, to eighteen months at USAA — a six-fold spread across institutions facing identical risks. Meanwhile Wells Fargo doesn't appear on Plaid's consent-refresh list at all — no clock, published nowhere. The random app you connected once to pay a soccer mom for your kid's lunch eight years ago could still be quietly reading your transaction history today.

Sit with that list for a second. If these were security decisions, or cost decisions, they'd converge — these institutions face similar threats and similar economics. They don't converge. Which tells you they aren't engineering positions at all. They're negotiating positions, frozen at whatever moment the last deal was struck.

## Expiry is correct. Nobody asks you at renewal.

There's an obvious reply here, and it's a good one. A credential that never lapses is a security defect. Expiry is correct. Any engineer would tell you the same, and so would I.

So the existence of a clock isn't the problem. The real question is what happens when the clock runs out, and who gets asked.

Everywhere else in software, expiry routes back to the person. GitHub makes you re-authorize. Claude makes you re-authorize. You're shown what you're granting, again, in plain language, and you get to decide again. It's mildly annoying, and it is exactly right, because the friction *is* the feature — it's the moment a human being gets to reconsider.

In this corner of the world, re-authorization is treated as friction to be engineered down. Not as a consumer's opportunity to re-decide. That framing tells you who the system is built for, and it isn't the person whose money it is.

## Coverage is partial, and product quality is decided upstream

Let me put the builder's complaint in one place, so you can weigh it and move on.

**Aggregators don't reach everyone, and the rule wouldn't have either.** There are 8,528 insured depositories in the US — roughly 4,278 banks and [4,250 credit unions](https://ncua.gov/newsroom/press-release/2026/ncua-releases-first-quarter-2026-credit-union-system-performance-data) as of Q1 2026, down about 47% from around 16,111 in 2008. The common assumption is that the top 50 institutions cover ninety-something percent of people. They don't: the top 50 is roughly 58–61% of consumer deposit accounts, the top 100 gets you to 65–68%, and the curve collapses fast after that. The gaps aren't randomly scattered, either — small credit unions are gated at the core processor layer, so entire classes of institutions drop out at once. And Kansas City Fed research finds community banks are the [sole commercial banking presence in about a quarter of US counties](https://www.kansascityfed.org/documents/8159/EconomicReviewV106N2HanauerLytleSummersZiadeh.pdf). Set that against the rule's exemption for institutions under $850 million in assets: in a quarter of American counties, the only bank available is one the rule never required to build a data interface.

**And the things that define your product's quality aren't yours to decide.** Uptime, latency, how often a connection silently breaks, how often a customer gets bounced back to re-authenticate — all of it is determined upstream, by institutions you don't have a relationship with. Plaid's `/institutions/get_by_id` endpoint returns a field called `error_institution` — "the percentage of logins that are failing due to an issue in the institution's system." It cleanly separates bank-caused failure from aggregator-caused failure. The data exists. It's collected continuously. Nobody publishes it. Plaid's status page covers only Plaid's own systems; Akoya's status subdomain doesn't resolve at all. §1033 would have required banks to publish interface performance monthly, to four decimal places, on a rolling thirteen-month basis; that died with the rule. One company does it voluntarily — Monarch publishes [per-institution success and longevity data](https://www.monarch.com/connection-status), broken out by data provider and refreshed daily. A competitor giving away the best public reliability dataset in the industry, because someone there decided it should exist.

But my inconvenience isn't the interesting part, and I'd rather not pretend otherwise. Both of these land on the consumer, just quietly. Whether a person is well served by any of these products depends on where they happen to bank — a thing nobody chooses with data portability in mind. And when a connection breaks, the app looks broken, so they blame the app, churn, leave the review, switch. The institution whose interface actually failed pays nothing, because nobody can see it was them.

## This genuinely costs the banks money

I don't want to hand-wave the other side of it.

A large French bank self-reported €21 million to the European Commission. Large US banks self-reported a median of $21 million to the CFPB — a range of $2 to $47 million a year to establish *and* maintain a developer interface. Two regulators, two continents, the same order of magnitude. That's the closest thing to corroboration the banks' cost claim has, and it's real money for real work.

Regulators also have a documented habit of lowballing this. The UK's CMA estimated £20 million to stand up the Open Banking Implementation Entity; the net cash cost came to [£148 million](https://assets.publishing.service.gov.uk/media/62908644d3bf7f036ebf5880/CMA_OB_Lessons_Learned_Review.pdf), more than seven times the estimate, in the CMA's own lessons-learned review. The European Commission's contractor study put PSD2 API development at roughly €2.2 billion one-off across 1,125 credit institutions, while describing its own evidence base as "limited," "quite divergent," and "very limited data."

So the objection isn't stupid, and anyone arguing this should all be free isn't arguing seriously.

But there's one more number in that same CFPB submission, and it's the one nobody quotes.

The banks reported that the developer interface costs a median of **2.3%** of what they spend on their own consumer-facing interface.

Their app. The one they built for themselves.

Two point three percent. That's the figure at the center of a fourteen-year fight.

It was never really about whether this costs money. It's about who pays, what they get for it, and whether the terms are ones anyone can plan around.

## Investments, retirement, and mortgages were never in the rule

Here's the part that reframed all of it for me.

Plaid's Investments product covers roughly 2,400 institutions, against something like 10,000 for checking. About 24% — and that's the vendor's own optimistic self-report.

The entire brokerage universe sits outside FDIC and NCUA, so none of those coverage numbers include Fidelity, Schwab, Vanguard, or any 401k recordkeeper. Brokerage is *more* concentrated than banking, but access is *worse*, because brokerages have both the incentive and the means to cut aggregators off whenever they choose.

And §1033 never covered investment accounts at all. Reg E deposits and Reg Z credit cards, full stop. Brokerage, retirement, mortgages, auto loans, student loans — all out of scope, with a phase-in on the rest that ran top-down.

Fourteen years of argument. A rule finalized in October 2024 and sued the same day. The Bureau moving for summary judgment against its own rule. A preliminary injunction in October 2025 — enjoined, not struck down, still sitting there. All of it over checking accounts and credit cards.

Everything you'd actually need to see someone's whole financial picture was never on the table.

## Which leaves the discipline voluntary

You can build the app. What you can't do is underwrite a business on an input your counterparty can reprice the moment leverage shifts. That's not a complaint about cost. It's a statement about what's safe to build on.

But the builder's problem is the smaller half of this.

Every unstated boundary in this piece is unstated in the same direction. A person granted access to solve a problem for themselves, and every party downstream (the aggregator, the bank, the app) has some incentive to read that grant as generously as possible. Nobody in the chain is required to be specific about it. And the one person whose data it is has the least ability to find out what they actually gave away.

Including me. That's the uncomfortable part. When a grant comes back broader than what the consumer thought they approved, the party receiving it has very little incentive to bring it up, and I'm the party receiving it. I know exactly how that argument goes in your own head: the data is *right there*, it would make the product better, and they did click approve. There's a great deal that financial data can tell you, and nearly all of it is monetizable by someone.

Which is precisely why the boundary can't be left to whoever benefits from reading it generously. The rule that would have set an outer limit is enjoined; it isn't coming back quickly, and it wouldn't have covered most of what matters anyway. That leaves the discipline voluntary.

Take what you were given. When you want more, ask.

If code isn't the moat, permission is. And right now, the industry is quietly digging that moat as wide as it possibly can.

### Further Reading

*This extends an argument I made in [Billing Is Not a Standalone App](/blog/billing-is-not-a-standalone-app/) — that durable value sits with whoever owns the data underneath — into regulated territory. And none of it touches the question of who's liable when an agent moves the money, which is [the first piece in this series](/blog/agent-password-refund/).*

---

## Sources

Links to primary sources where they exist.

**Data sharing volumes**

- [114 Million Reasons to Keep Moving Forward](https://financialdataexchange.org/fdx-feed/114-million-reasons-to-keep-moving-forward-on-industry-led-standard-for-secure-data-sharing/) — FDX, April 2025 (76M → 114M, a 50% year-over-year increase). Also on [GlobeNewswire](https://www.globenewswire.com/news-release/2025/04/25/3068457/0/en/114-Million-Reasons-to-Keep-Moving-Forward-on-Industry-Led-Standard-for-Secure-Data-Sharing.html).
- [FDX hails 'milestone' in consumer accounts using its API](https://www.openbankingexpo.com/news/fdx-hails-milestone-in-consumer-accounts-using-its-api/) — Open Banking Expo (130M+, early 2026).

**Consent, scope and revocation**

- [Plaid — Link OAuth guide](https://plaid.com/docs/link/oauth/) — source of "can provide the ability for end users to configure granular permissions on their Items," the checking-but-not-credit-card example, and the consent-refresh list (12 months by default; Brex 3 months; USAA 18 months). Wells Fargo does not appear on that list.
- [Plaid — OAuth API reference](https://plaid.com/docs/api/oauth/).
- [FDX — CFPB 1033](https://financialdataexchange.org/cfpb-1033/) — consent components, and authorization/revocation/reauthorization "left to market participants."
- [Why Revoking Customer Consent Doesn't Always Stop Data Processing](https://www.openiam.com/blog/consent-revocation-financial-institutions) — the structural problem of consent stored centrally but enforced locally.
- [UK Open Banking Standards — Revocation](https://standards.openbanking.org.uk/customer-experience-guidelines/introduction/revocation/latest/) — how another regime specifies it.

**Institution-specific terms**

- [Plaid — Auth](https://plaid.com/docs/auth/) — tokenized account and routing numbers at Chase, PNC and US Bank. See also [Plaid on Chase TANs](https://support.plaid.com/hc/en-us/articles/25133498038551-Why-am-I-receiving-R04-Returns-for-ACH-transactions-with-a-Chase-TAN-Tokenized-Account-Number).
- [Plaid — Transactions data](https://plaid.com/docs/transactions/transactions-data/) and [Transactions troubleshooting](https://plaid.com/docs/transactions/troubleshooting/) — Capital One's lack of pending transactions and 90-day history limit.
- Plaid institution documentation — Schwab's one-active-Item-per-user-per-application limit; the re-consent clocks (Brex 3 months; Amex, Bank of America, Capital One, Schwab, Citibank, Fidelity, Navy Federal, PNC and TD annual; USAA 18 months); and the `INSTITUTION_RATE_LIMIT` error, documented without published thresholds.
- [Plaid — /institutions/get_by_id](https://plaid.com/docs/api/institutions/) — the `error_institution` field, "the percentage of logins that are failing due to an issue in the institution's system."
- [Plaid — Investments](https://plaid.com/docs/investments/) ("over 2,400 institutions in the US and Canada") against [Plaid — Institutions](https://plaid.com/docs/institutions/) ("over 10,000"). Both fetched July 2026. Aggregator institution counts include brokerages, card issuers, crypto exchanges and payroll providers, and are not comparable to depository counts.
- [Monarch — Connection Status](https://www.monarch.com/connection-status) and the [dashboard announcement](https://www.monarch.com/blog/connectivity-dashboard) — per-institution success and longevity, by data provider, refreshed daily.

**Coverage and cost**

- [NCUA — First Quarter 2026 Credit Union System Performance Data](https://ncua.gov/newsroom/press-release/2026/ncua-releases-first-quarter-2026-credit-union-system-performance-data) — 4,250 federally insured credit unions, down from 4,411 a year earlier. Also the [Q1 2026 data summary](https://ncua.gov/files/publications/analysis/quarterly-data-summary-2026-Q1.pdf).
- [Kansas City Fed — Community Banks' Ongoing Role in the U.S. Economy](https://www.kansascityfed.org/documents/8159/EconomicReviewV106N2HanauerLytleSummersZiadeh.pdf), Economic Review — sole banking presence in ~a quarter of US counties, ~72% of rural branches, ~two-thirds of rural deposits, and the deliberate outsourcing of technology to core processors. *(Structural-role figures only. This report's market-share data runs 2000–2020; the institution counts above are Q1 2026. Do not combine vintages in a single claim.)*
- FDIC *Quarterly Banking Profile*, first quarter 2026 (released May 2026) — 4,278 insured commercial banks and savings institutions as of March 31, 2026. Note: the Call Report filer count (4,352) is a different figure; the QBP headline is the one to cite.
- Consumer deposit-account concentration (top 50 ≈ 58–61%, top 100 ≈ 65–68%) — modeled from FDIC BankFind (DEPDOM) and Call Report retail-deposit data, Q1 2026. **Modeled, not measured**; deposit-dollar rank is not consumer-account rank, which is why these differ from the more commonly cited dollar-share figures.
- CFPB §1033 final rule, 89 FR 90838 at 90857–58 — institutions above $850 million in assets hold roughly 90% of covered accounts.
- [CMA — Open Banking Lessons Learned Review](https://assets.publishing.service.gov.uk/media/62908644d3bf7f036ebf5880/CMA_OB_Lessons_Learned_Review.pdf) (Kirstin Baker CBE, May 2022) — the £20 million estimate against £148 million net cash cost.
- Bank cost self-reports to the CFPB under compulsory §1022(b) order — $2M–$47M per year to establish and maintain a developer interface, median $21M, and a **median of 2.3% of the bank's spend on its own consumer-facing interface**. ⚠️ Annual establish-and-maintain, not a build price. The Bureau states the sample is "likely not representative of the market as a whole," and several respondents could not separate interface costs from general IT. Directional only.
- European Commission / VVA-CEPS study (Feb 2023), adopted in COM(2023) 365 — ~€2.2 billion one-off PSD2 API development across 1,125 credit institutions. The €21 million French bank figure is from SWD(2023) 231, p.52 fn.133. The Commission characterizes its own evidence as "limited," "quite divergent," "very limited data." ⚠️ The CEPS study also states €3.2bn on p.180, unexplained.

**The rule and the litigation**

- [Required Rulemaking on Personal Financial Data Rights](https://www.federalregister.gov/documents/2024/11/18/2024-25079/required-rulemaking-on-personal-financial-data-rights) — the §1033 final rule, Federal Register, October 2024. Also [12 C.F.R. Part 1033](https://www.ecfr.gov/current/title-12/chapter-X/part-1033) and the [CFPB's own page](https://www.consumerfinance.gov/personal-financial-data-rights/).
- [Personal Financial Data Rights Reconsideration](https://www.federalregister.gov/documents/2025/08/22/2025-16139/personal-financial-data-rights-reconsideration) — the August 2025 ANPRM.
- *Forcht Bank, N.A. v. CFPB* (E.D. Ky.), preliminary injunction October 29, 2025 — [ABA Banking Journal](https://bankingjournal.aba.com/2025/11/kentucky-federal-court-enjoins-cfpb-from-enforcing-current-1033-final-rule/) · [Moore & Van Allen](https://www.mvalaw.com/data-points/cfpb-enjoined-from-enforcing-personal-financial-data-rights-rule-1033) · [American Banker](https://www.americanbanker.com/news/court-halts-compliance-with-cfpbs-final-open-banking-rule).
- [Reversing course, CFPB says it will issue revised open banking rule](https://www.consumerfinancemonitor.com/2025/08/04/reversing-course-cfpb-says-it-will-issue-revised-open-banking-rule/) — the Bureau moving against its own rule.
