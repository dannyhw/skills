---
name: british-plain-english
description: |
  Write or rewrite text in plain British English, following the GOV.UK
  writing guidelines and A to Z style guide: UK spelling, short sentences,
  active voice, front-loaded content, no negative contractions, must / need
  to / can for requirements, every technical term explained at first use,
  no AI slop. Use for documentation, READMEs, runbooks, error messages,
  release notes, incident reports, UI copy, emails and explanations for
  readers outside the field. Also use when the user says "British English",
  "UK English", "plain English", "GOV.UK style", "write it the British way",
  "en-GB", "layman's terms", "explain it simply", "no jargon", "de-slop" or
  "make this readable" in a British context. The same rules govern the
  chat reply: answer first, prose only.
license: MIT
metadata:
  version: "0.1.0"
  basis: GOV.UK writing guidelines and A to Z style guide (Open Government Licence v3.0)
---

# British plain English

Write plain British English that a busy reader outside your field understands on one read. The rules come from the GOV.UK writing guidelines, where plain English is mandatory. Specialists prefer it too: the more expert the reader, the stronger their preference for plain text. There are 2 registers: the document you write or rewrite, and the reply you type in chat.

## The document

When you write or rewrite documentation, apply these rules to the prose:

1. Never touch code, identifiers, commands, flags, file paths, quoted errors, product names or facts. American spelling inside code stays: `color`, `initialize`, `license` keys and `canceled` statuses are identifiers.
2. Use UK spelling for everything else: organise, colour, centre, behaviour, catalogue, programme (but computer program), licence (noun) and license (verb), practice (noun) and practise (verb), cancelled, modelling, judgement. `references/spelling.md` has the full map.
3. Front-load. The first sentence of the page and of each section gives the most important fact. Then taper to detail. Do not repeat a summary in the next paragraph.
4. Keep sentences to 25 words or fewer and paragraphs to 5 sentences or fewer. One instruction per step. Put the condition before the command, with a comma: "If the build fails, read the log."
5. Use the active voice and address the reader as "you". Use "we" only after you have named the organisation. "An access token is needed" becomes "You need an access token".
6. Requirements: "must" for a hard rule, "need to" for a step in a process, "can" for an option. Do not use "should", "may", "might" or "may be able to" for these. A required "should" becomes "must" or "need to". An optional one is deleted or becomes "can".
7. Contractions: positive ones are fine (you'll, it's, we're). Never use negative contractions (can't, don't, won't, isn't) because readers misread them as the opposite. Write "cannot", "do not". Never use should've, could've, would've.
8. Use short, common words: "buy" not "purchase", "help" not "assist", "about" not "approximately", "start" not "initiate". Break up words ending in -ion and -ment into verbs: "carry out an installation of" becomes "install". `references/word-swaps.md` maps the GOV.UK words to avoid and the AI-overused words to plain ones.
9. Explain a technical term or abbreviation the first time you use it, in a few words. Technical terms are not jargon when the reader needs them. Do not explain product names, standard names (Postgres, S3, HTTP) or the tool the document is about. Name the host, the flag or the earlier step that a command depends on.
10. One word, one meaning, for the whole document. Pick "check" or "make sure" and keep it. Pick "configuration" or "settings" and keep it.
11. State the fact, not its importance. No buzzwords (robust, seamless, leverage, deliver, empower, key, transform). No "please" or "please note". No "not just X, it is Y", no decorative triplets, no "in conclusion".
12. No semicolons and no em dashes. Write 2 sentences, or name the relation ("because", "but", "for example"). No "eg", "ie" or "etc": write "for example", "such as", "that is", or name the items.
13. Formatting carries structure only. Sentence case for every heading. Headings are descriptive, front-loaded, never questions. No bold for emphasis. No emoji. No footnotes.
14. Bullet lists need a lead-in line that ends in a colon and at least 2 bullets. Each bullet starts in lower case, reads on from the lead-in and holds one sentence. No "and" or "or" at the end of a bullet, no semicolons and no full stop after the last bullet. Numbered steps are full sentences with a capital letter and a full stop.
15. Warnings: the command or condition first, then the risk. "Do not run this against production. The command deletes rows."

For dates, times, numbers, quotes and other house-style points, read `references/style-points.md`. For an error message, a runbook, an incident report, release notes, a commit message or UI copy, read `references/use-cases.md` first.

Before (AI output):

> **Connection timeouts.** If sqlpipe hangs or fails with `dial tcp: i/o timeout`, you should verify that the host can reach the Postgres port — this is often a firewall rule that isn't configured correctly (e.g. a security group). Please note you may need to authorize sqlpipe's IP.

After:

> ## Fix connection timeouts
>
> sqlpipe stops with `dial tcp: i/o timeout` when it cannot connect to the Postgres port (5432 by default). A firewall or security group usually blocks it.
>
> 1. Check that the host that runs sqlpipe can connect to port 5432.
> 2. If the database is managed, for example RDS, add the IP address of the sqlpipe host to its allowed list.

## The reply

Every chat reply follows these rules:

1. Answer in prose. No headers, no bullet lists, no bold, no tables. A code block is fine when the reader must copy it. A numbered list is fine for 3 or more steps the reader must run in order.
2. The first sentence gives the answer or the result. Do not restate the question.
3. No em dashes. Name the relation or write 2 sentences.
4. Explain a technical term in a few words the first time you use it: "idempotent (safe to run twice)".
5. UK spelling. No negative contractions. No openers ("Certainly", "Great question") and no closers ("I hope this helps", "Let me know").
6. Do not shorten quoted error text, security warnings or confirmations before a destructive action.

Before: The failure stems from control-plane leader election during pod churn — nothing to worry about! You don't need to do anything.
After: The pods restarted and the queue lost its leader for a short time. It recovered by itself, so you do not need to do anything.

## Self-check before you deliver

1. Reply: search for `—`, `**`, `#` and lines that start with `-`. Remove each one.
2. Spelling: search the prose (not the code) for `ize`, `yze`, `or ` endings such as color and behavior, `er` endings such as center, `canceled`, `modeling`, `program` for a schedule, `license` as a noun. Fix each hit.
3. Document: count the words in your 3 longest sentences and split anything over 25. Search for `n't`, `should`, `may`, `might`, `please`, `;`, `—`, `e.g.`, `eg`, `i.e.`, `etc`, `**`. Fix each hit. Check that every bullet starts in lower case after a lead-in line, and that every heading is in sentence case and not a question.

## Limits

These rules are for facts and instructions, not marketing copy or brand writing, because they remove persuasion. Say so, and offer them for the docs instead. For ASD-STE100 Simplified Technical English compliance, use an STE skill instead: STE requires American spelling, so it conflicts with this skill.

## References

- `references/spelling.md`: US to UK spelling map, and the words that change with their part of speech
- `references/word-swaps.md`: the GOV.UK words to avoid and AI-overused words, with plain British replacements
- `references/style-points.md`: dates, times, numbers, quotes, brackets, abbreviations, lists and headings
- `references/use-cases.md`: the pattern for error messages, runbooks, incident reports, release notes, commits, agent prompts, UI copy and emails
