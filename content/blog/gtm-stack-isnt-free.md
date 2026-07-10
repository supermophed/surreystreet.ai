# Innovation in Your GTM Stack Isn't Free

Every so often I get consumed on a topic and decide to join a series of meet ups or demo days to see what's happening with start ups in the space. Ever since [my post on billing](/blog/billing-is-not-a-standalone-app/) and thinking about how transformations need to evolve in the age of AI (more on that later), I've been thinking a lot about the GTM stack, who's playing and where it's going. So, I went to a demo day for the GTM stack last night. Seven startups, a room full of founders, and honestly — the energy was electric. They weren't wrong when they said San Francisco is back! Alive!

One of the presenters opened on a line I keep hearing: the GTM stack is hopelessly fragmented. She's right — it is. But the tool she was showing to fix it was, itself, one more tool for the stack. Wha - Wha. And I don't mean that as a knock. Fragmentation is the point.

Fragmentation isn't a bug someone's about to fix. It's a permanent condition. Consolidation is a vendor-level story — Salesforce buys this capability to fill out their offering; Adyen buys that start-up to move up the funnel in their unified platform strategy. But down at the install level, no two Salesforces have ever looked alike. Every company bends its CRM into a shape only it understands. That gap — between the tidy vendor logos and the messy reality of your actual instance — is where all the new stuff is playing. And there's a lot of new stuff, because building has gotten cheap and fast enough that a two-person team can take a real swing at a problem.

Two demos genuinely stuck with me.

The first was Retrieval AI ([www.rtrvr.ai](https://www.rtrvr.ai)) — a browser extension for the prosumer that scrapes the web. The founder pulled up the Luma invite for the event we were sitting in, grabbed every attendee's name and email, opened LinkedIn, scraped everyone's profile, ran real due diligence across the web on each person, and fired off a personalized LinkedIn connection request to the whole room — start to finish, hands off. He said the whole run, ~500 people, cost under a dollar, because it runs on DeepSeek. It was jaw-dropping — the kind of thing that would've been a quarter of RevOps work two years ago, done in the time it took him to narrate the slide. Truly amazing. (Also maybe a little unsettling, if I'm honest: it rides your own logged-in session, so no password changes hands. It made me think how much personal information is really out on the web and can be eventually correlated back to you somehow. :) )

The second was Otto, and the demo really surprised me how obvious and simple a solution they constructed. A guy got up and told a story every field rep knows in their bones: he hated data entry. Great dinner with a prospect, then sitting at the bar afterward thumbing notes into his phone before he forgot them. Otto gives you a phone number — a chief of staff you call from the car on the way home. You just talk. "Here's what happened, here's what mattered, log it in the CRM." It reads you your calendar, nudges your to-dos, pulls info, emails you a report. And the second I saw it I thought — oh, of course. That's what reps are. They don't live in front of a screen; their whole job is relationships, and reading the problems buried inside them. (I can't tell you how many sales people I know who hate the CRM.) Otto unhooks them from the toil and still feeds the machine the data it needs. That's not a feature. That's understanding the actual human you're building for.

So the talent is real, and so is the innovation — I left that room impressed. But here's the operator's read I couldn't shake. Look at what none of these did: none of them replaced the CRM, touched quote-to-cash, or owned the data underneath. They built *on top of* the system of record — and the system of record is exactly where the durable value stays put.

You can see it clearest in enrichment, which ran through half the demos. The tools that grab the data are racing to zero. The data itself isn't — and the giants know it. Salesforce rents it, HubSpot bought it (Clearbit, now Breeze), Microsoft owns it outright — it bought LinkedIn, the very graph the scrapers were pulling from. Rent it, buy it, or own it, but somebody always owns it. And the giants aren't sitting still on the tool layer either: Salesforce has Agentforce, Microsoft has Copilot, HubSpot has Breeze, all baking agents and enrichment straight into the platform you already pay for, grounded in data that's already there. The clever tool a startup demos tonight is a checkbox in someone's license next quarter.

Which is the catch tucked inside all that opportunity. Adding a tool is never free. The average B2B sales team already runs a dozen of them; the best-run teams have cut back to five or six. Every one you add quietly raises the bar — your close rate, your LTV, your average deal profit all have to climb just to earn it back. And the bar's higher now, because you're not only paying for the tool, you're paying it to beat the "good enough" version already bundled into your platform. The tools that clear that bar are the ones aimed where the giants won't go: your weird install, your edge case, the CRM they don't own. Everything else is rent.

So — did I leave discouraged? Honestly, the opposite. The barrier to building something real has collapsed, the people in that room were sharp, and the problems are finally getting interesting. That's worth being excited about. Just — if you're the one buying — love the demo, then make it prove it's worth the rent. While the city is buzzing with AI fervor, bring your judgment anyway.

---

**The seven that demoed** (all worth a look):

- [Retrieval AI](https://www.rtrvr.ai) — browser agent that scrapes and automates the web
- [Nimble](https://www.nimbleway.com) — web-search agents that turn the live web into structured data
- [Otto](https://ottosales.ai) — voice-first AI "chief of staff" for sales reps
- [Boomerang](https://www.theboomerang.co) — lead scraping and prospecting data
- [Fuse](https://tryfuse.ai) — AI-native outbound sales platform
- [Yuzu Labs](https://www.yuzulabs.io) — a GTM "brain" / agent layer that sits on your CRM
- [Scalekit](https://www.scalekit.com) — auth and RBAC for AI agents
