<!-- Editor notes (delete before publish):
     - VERIFY AT PUBLISH: Orb's close was slated for July 1, 2026 and m3ter for Salesforce's fiscal Q2 2027. If either has closed by publish date, change "agreed to acquire" to "acquired."
     - Open polish items: header capitalization is mixed (sentence vs title case); lede still ends on "the answer is no."
     - Placeholder near the close for in-session specifics (currently none inserted).
-->

# The Platform Playbook: Billing Is a Component, Not a Company

When I joined Atlassian in 2022 to take [Stripe's then-young billing system](https://stripe.com/customers/atlassian) and grow it for Atlassian's enterprise use cases, half the valley was shopping for the same thing: a standalone system to own billing. You could sort the market by age. The old guard — Zuora — was built for the seat- and subscription-based world. A cohort of teenagers — Bill.com, Recurly, Chargebee — had grown up around recurring revenue. And a set of upstarts — Metronome, m3ter, Orb — was betting everything on a use case that was still niche at the time: usage-based billing.

Four years later, the question those companies were all implicitly asking — can billing be a standalone application? — has answered itself. The answer is no.

## Billing is a Feature

Billing is not a standalone company. It is a feature of a platform. And the platform everyone in this market is racing to build is the one enterprise software has always organized itself around: the B2B commerce system. In the old vocabulary, that is quote-to-cash and record-to-report — configure, price, quote; contract, bill, collect; recognize, reconcile, report. Billing is one organ in that body. It was never the body.

Every move in the billing market over the last two years is the same move from a different seat: billing being absorbed into a platform that already owns the rest of the cycle, or a billing company spending everything it has to grow into that platform itself.

## The "out of the box" lie

Billing is one of those deceptively hard domains. It sits between sales and finance and bridges governance and product capability — the exact point where how you sell becomes how you collect, and how you collect becomes what you can report. Nobody bills the way the box assumes; every "out of the box" billing system needs real customization or a layer of orchestration on top, because the way a company prices and bills is part of its own special sauce. (this topic requires its own separate post about "no one sells and bills the way they think they do" — if i can rally, I'll write that blog another time.)

That is exactly why billing can't stand alone. Its output — a usage event, a rated charge, an invoice — does nothing until it touches the things around it: the quote and contract that justify it, the ledger and revenue schedule that record it, the payment rail that collects it, the CRM that owns the customer. Billing is connective tissue, and connective tissue is only valuable attached to a body.

## One law, two tactics

### Tactic one: join a platform that already exists.

- Stripe [bought Metronome for a reported $1 billion](https://stripe.com/newsroom/news/stripe-completes-metronome-acquisition) (completed January 2026), slotting metering into a stack that already runs payments, invoicing, quotes, and revenue recognition — quote-to-cash for internet businesses, with Metronome completing the consumption end. Announcing it, Patrick Collison [said the quiet part out loud](https://x.com/patrickc/status/1995961389706608734): "Metered pricing is the native business model for the AI era."
- Salesforce [agreed to acquire m3ter](https://www.salesforce.com/news/stories/salesforce-signs-definitive-agreement-to-acquire-m3ter/) (definitive agreement signed June 2026; expected to close in Salesforce's fiscal Q2 2027) and will fold its metering into Agentforce Revenue Management and Revenue Cloud — the quote-to-cash engine bolted directly onto the CRM that owns the customer relationship. Tellingly, Salesforce put its standalone CPQ product into [End of Sale](https://www.cldpartners.com/salesforce-cpq-is-entering-an-end-of-sale-phase-whats-next/) and rolled it into the suite. Even the platform won't sell the pieces separately anymore.
- Adyen [agreed to acquire Orb for $335 million](https://www.adyen.com/press-and-media/jtrg4qd7j3p4rj) (announced June 2026, expected to close July 1, 2026), unifying billing with the payments-and-collection end of the same cycle.

### Tactic two: become THAT platform yourself.

- Zuora didn't stay a billing company. It became a quote-to-cash platform — CPQ for quoting, Zephr for access and packaging, Togai for usage metering, [Zuora Revenue](https://www.zuora.com/products/revenue/) for recognition and the subledger — pushing right to the edge of the ERP. It [went private with Silver Lake and GIC](https://www.zuora.com/press-release/silver-lake-gic-zuora/) ($1.7B, closed February 2025) to keep funding that build away from quarterly scrutiny.
- Chargebee, still independent and VC-backed ([last valued at $3.5 billion in 2022](https://www.fintechfutures.com/investment-banking/subscription-management-platform-chargebee-valued-at-3-5bn-following-250m-raise)), is rolling up adjacencies — including Inai, a payments-orchestration startup, in 2025 — to become a subscription-commerce suite rather than a billing tool.
- Recurly, backed by Accel-KKR, [bought Prive and Redfast in 2025](https://recurly.com/press/recurly-acquires-prive-and-redfast-to-accelerate-the-future-of-subscription-growth/) to integrate billing, payments, analytics, engagement, and ecommerce subscription management into one platform.

## Why now: the tax came due

To say agents made fragmentation expensive would be incorrect. They didn't. Architectural fragmentation was always expensive. Stitching billing to the CRM, the payment rail, and the revenue subledger always cost real money — headcount, systems, integration, maintenance, endless reconciliation. Companies paid it anyway, for years, because there was no good unified alternative (other than building it all themselves), and because occasionally the stitching itself was the point: a proprietary risk model, a bespoke pricing engine, a customer view nobody else had. Special sauce justified the tax. Absent that sauce, you paid it resentfully.

Two things changed — and neither was the cost of fragmentation.

First, the unified alternative finally got good. API-native platforms — Stripe, not the old clunky platform suite — made buying the whole cycle actually work. For any company whose edge was something other than commercial orchestration, building your own stitching stopped being defensible. The sauce wasn't worth the cost of the kitchen.

Second, AI raised the bar on what the unified system of record has to do. Ask an agent a plain question about a customer — Who are they? Did they convert? Do they pay on time? How much have they spent with us this year? Did we recognize all of that revenue, or did a special case force us to defer it? — and watch it walk straight across the CRM, the billing engine, the payment rail, and the revenue subledger. Here's what AI actually changed: the agent can write every query and bridge every database itself — syntax correct, no engineer required. The mechanical cost of fragmentation just went to zero. The rest of the tax didn't. The rules that define "good standing" or "fully recognized" still live outside every vendor, in glue someone maintains, and each vendor still has to expose enough of its state, cleanly enough, for the agent to reach it. The platform's entire pitch is the elimination of that tax — one record, one place to ask, the rules native to the system instead of bolted on outside it.

So the cost of fragmentation didn't move. The alternative got good, and the value of paying the tax collapsed for everyone whose orchestration was never their moat. Fragmentation was never free — it was a bet that your orchestration was special. For most companies, that bet just stopped paying.

What's left is a small set of companies for whom commercial orchestration genuinely is the product — and they don't buy billing either. They build the platform, and billing is one organ inside it. It is the same move payments made a decade ago: acceptance commoditized, and the risk-and-trust judgment on top became the moat.

## What this means if you're buying

This hands the buyer a sharp test: is commercial orchestration my special sauce? If not, stop paying the integration tax — join a platform, and treat your billing decision as the platform decision it actually is. The real question was never "which billing tool is best," but "whose quote-to-cash and record-to-report am I joining, and is metering native to it." If commercial orchestration *is* your sauce, then you are not buying billing — you are building a platform, and billing is a component of it. The one position that no longer exists is the middle: running billing as a standalone business, paying the tax, with no sauce to show for it.

## Usage and Billing are Platform Features Now

The standalone billing company was a phase, not a category — the window before the platforms arrived and before an agent had to answer for the whole customer relationship in one breath. The market just told us what billing is worth on its own and what it's worth wired into commerce, and the gap between those two numbers is the entire story. Billing was never the product. The system of record was — and in the AI era, the commerce platform is the only thing that can be it.
