# STYLE: how to write

Chat is compressed. Anything that outlives the chat is ASD-STE100 prose. Both lead with the answer.

## CM: output style

- CM-1: Compressed style from the first token, every session.
- CM-2: Drop articles, filler, pleasantries, hedging. Fragments fine. Chat only; never the text in CM-6.
- CM-3: Identifiers, commands, paths, numbers, units, error strings stay verbatim.
- CM-4: Never drop a negation. Never add a word to sound terse.
- CM-5: Write in full: security warnings, irreversible-action confirmations, multi-step instructions.
- CM-6: Normal prose in anything that outlives the chat: code, comments, commits, documents, ticket bodies, third-party text. Follows WR.
- CM-7: Pull request bodies and review findings: one point per line, under 300 characters.
- CM-8: A pull request body is a TL;DR: one line of purpose, then a Change / Why table, then the ticket ids.
- CM-9: A review finding is one line: `path:line: severity: problem. fix.`
- CM-10: Always TL;DR. Answer first, then detail.
- CM-11: Cut every sentence that announces what you will say or just said.
- CM-12: A chat answer stops at ten lines: verdict, then only what the operator needs to decide. Security warnings and multi-step instructions are outside the count. Cut evidence, never the verdict; name in one line what is held back.
- CM-13: Never paste a delegated report into chat. Relay its verdict and paths.

## WR: lasting prose

ASD-STE100 Simplified Technical English: controlled vocabulary, one idea per sentence, active voice, present tense, articles kept. One word, one meaning. No noun used as a verb. No stack of more than three nouns. An instruction has 20 words at most; a description 25.

Replace on sight: elevate (raise), delve (explore), leverage (use), foster (encourage), embark, unleash, crucial (important), robust (strong), navigating (managing), comprehensive (complete), tapestry, key points (main points), to be able to (to).

- WR-1: The project names the spelling (British or American). None named: British.
- WR-2: An identifier keeps its vendor's spelling (`color-mix()`, package names, API fields).
