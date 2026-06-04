# Contributor Guidelines
This is, after all, an open-source project. Anyone and everyone is invited to collaborate, discuss, and propose changes to the code. Of course, there must be rules for how a contributor can, well, contribute, so that *conflicts can be avoided*, *bugs can be negated*, and *all can be **rewarded** and **credited** for thier work*.

## Communication Guidelines
- Treat everyone with respect.
- Criticise actions, ideas, and/or code, not people.
- Keep conversations on-topic and to-the-point.
- Avoid necroposting.
- Avoid adding unessescary fuel into a possibly already-heated conversation.

## Contribution Guidelines
- **KNOW PYTHON**. This is non-negotiable, sorry! 😅
- **When using AI, please disclose in some way that you are using it.** (i.e. commenting `#ai-generated` in the changed code or commenting about AI usage in PR). This is to prevent the library from being completely reliant on AI. **Note that all PRs that do not disclose AI usage will be _CLOSED_.**
- Keep code clean of explicit content.
- Always know something well before doing it. (i.e. knowing what a function does exactly before messing with it)
- Try not to change anything fundamental about existing code. There are exceptions to this rule, like security vulnerabities.
- Be sure to read through the [wiki](https://github.com/Boss-1s/key_multivalue_storage/wiki) and [security policy](https://github.com/Boss-1s/key_multivalue_storage/blob/main/docs/SECURITY.md).

## Reccomendations when contributing
- Keep commit messages clear, to make release note creation easier. Commit messages should be summary of the changes. Anything extra can be added to the commit _description_.
- Keep the same file format, always.
- Use spaces for tabs instead of, well, tabs. Pylint will get really mad when you use tab characters...
- Don't be afraid to ask questions when stumped! It dosent hurt to learn a new thing or two.
- When committing, please always try to prefix the commits as follows:

| prefix | description |
| :---: | :---: |
| _`feat:`_ | new feature |
|_`fix:`_|small tasks like bug fixes or typo fixes|
|_`chore:`_|small tasks like lint notes, low code security risks, or dependancy updates. All general commits can also use this prefix.|
|_`refactor:`_|tasks like prettification, readability fixes, and removing dupes|
|_`fatal:`_|critical tasks involving code breaks and/or critical code insconsistencies in files. **Only use `fatal` on errors that break everything related to that file.**|

Note that these contributor guidelines are subject to change. Happy contributing!
