# Use cases

The rules in `SKILL.md` apply to any text where a misreading costs the reader time or money. Each case below names the pattern.

## Error messages and CLI output

The reader is in the middle of a failure. Say what happened, the cause if you know it, and what fixes it. No "Oops", no "Sorry", no "please".

> Before: Oops! Something went wrong while attempting to establish a connection. Please ensure your credentials are properly configured and try again.
> After: Could not connect to the database. The password for user `app` was wrong. Set `DB_PASSWORD` and try again.

## Runbooks

The reader is often tired or under pressure. Use numbered steps, one instruction per step, condition first. Put each warning before its step, with the command first and the risk second. Name the host or the service in every step.

## Incident reports and postmortems

Front-load the impact: when, how many, what broke. Use the simple past ("the deploy removed") so the timeline is clear. Say "we do not know yet" rather than "may have impacted".

> Before: We have identified an issue that may have impacted some users' ability to access the service. We sincerely apologise for any inconvenience.
> After: Between 14:02 and 14:31 UTC on 3 March 2026, 12% of requests failed. A deploy at 14:00 removed the cache warm-up step. We reverted it at 14:27.

## Commit messages and PR descriptions

Imperative subject line in sentence case ("Add retry to the upload step"). UK spelling in the body, but never in identifiers. Delete "This PR aims to".

## Release notes and changelogs

One entry, one change. Front-load each entry with what changed for the reader. A breaking change starts with the action: "Update your calls to `v2/users`. The `name` field is now `first_name` and `last_name`."

## Instructions for AI agents (prompts, AGENTS.md, skills)

A prompt is a procedure for a reader that cannot ask questions. One instruction per sentence. Condition first ("If the build fails, stop"). Use "must" for a hard rule. A model reads "should" as optional, so write "must" or delete the rule.

## Support replies and status-page updates

Many readers are not native speakers and many are stressed. Front-load the fact, give the time with its zone, and say what the reader needs to do, if anything.

> Before: We sincerely apologise for any inconvenience this may have caused.
> After: The API was down for 18 minutes from 9:12am UK time. Uploads made during this time were saved and will finish today. You do not need to upload them again.

## Emails

Put the request or the answer in the first sentence. Give a date, not "ASAP" or "end of play". One topic per email where you can.

## UI copy

Buttons and labels start with a verb and use sentence case: 'Save changes', 'Create project'. Refer to them in single quotes in body text. Empty states say what the reader can do: "No projects yet. Create a project to start."

## Where this does not fit

Do not use these rules for marketing pages, launch posts, blog posts or brand writing. They remove persuasion. Write those in your own voice and use these rules for the docs they link to.
