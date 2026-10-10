# CSE543 Information Assurance and Security - Pwn Them All

Created with Grok Build

Eight small web services, one after another. Each one looked closed until you asked who was actually making the decision. In every case the browser, or a proxy in front of it, could supply the fact the server trusted.

The interesting part was not a single clever payload. It was the habit. A check that belonged on the server had been left where the client could read it, skip it, or rewrite it. The notes below are the method, what was new in that step, the lesson, and the mitigation. Host names, request traces, passwords, and flags stay off this page.

## The password lived in the page

The first service was a login form. The page loaded a script, and that script compared the form fields with a password written out in the source.

The method was to read the script the browser was already going to run. Nothing was broken on the server, because the server was not the one deciding.

What was new was how thin the secret was. The "authentication" was a branch in a file the HTML asked for by name. Viewing the source of the page was enough to find the script, and reading the script was enough to learn the comparison.

The lesson is that a browser is an open book. Anyone who can load the page can load the script.

Mitigation: the server checks the password, against a secret the page never receives. Store a slow hash, not the password. The script in the browser may tidy the form. It must not be the lock.

## A form field became a command

The next page ran a script that built a shell command out of a form field, then asked the server to run it.

The method was to notice that the field was concatenated into a command string. Text that ends one command and starts another changes what runs. The script was still client-side, so the construction was visible before any request was sent.

What was new was the jump from "the client can see the check" to "the client can change the command." The same class of mistake as the login, with a worse consequence: the string was destined for a shell.

The lesson is that concatenation is a parser. The shell will parse whatever you glue together.

Mitigation: do not pass form text to a shell. Call a program with an argument array, or call a library function that never sees a command line. If a character must be restricted, use an allowlist of the values you meant to accept. Quote-escaping is the weaker fix, and it is easy to get wrong.

## The record id was the whole authorization

A later service returned a record when the request named that record's id. Changing the id returned a different record. The server did not ask whether this caller was allowed to see it.

The method was to treat every identifier in the request as untrusted, and to try a different one. The response itself showed that the lookup had happened.

What was new was that the bug survived a move onto the server. The earlier levels failed because the check was in the browser. This one failed because the server check was "does this id exist?" rather than "may this user see this id?"

The lesson is that an identifier is not a capability. Knowing the number of a row is not the same as being allowed to read the row.

Mitigation: on every read and every write, load the session on the server and decide from that session. Inaccessible objects should look the same as missing ones, so a guess does not confirm that the row exists.

## The secret was sitting in the form

The next gate was a hidden field and a cookie. Both changed on each visit. Both were delivered to the browser, which is the same machine as the attacker.

The method was to read what the page had been given. A hidden input is not hidden from the person driving the browser, and a cookie the script can see is not hidden either. Once the pairing was visible, replaying a fresh pair was ordinary request editing.

What was new was the costume. A nonce and a cookie look like a protocol. Here they were still client-held facts. The server believed them because it had just handed them out, not because the caller had proved anything the caller alone would know.

The lesson is that a value the browser can read is not a server secret. Freshness does not create identity.

Mitigation: keep the session on the server. Send the browser only an opaque session id, in a cookie marked `HttpOnly` and `Secure`, with `SameSite` set. Bind any one-time value to that server-side session, and do not put the authorization decision in a form field.

## The program that checked access was downloadable

One service stored account data in a script behind a URL. Requesting that URL returned the source. The source showed which request fields selected a file, which field was treated as an administrator switch, and where the saved records lived.

The method was to fetch the script as a file instead of running it. The novelty was how much the disclosure was worth. A logic bug that would have taken a long time to infer was written down in the file: a parameter meant "act as admin," and another parameter chose a path.

The lesson is that source is data. If the web server will hand the file over, every comment and every comparison in it is public.

Mitigation: the web root serves pages, not the programs that implement access checks. An administrator flag is never a request parameter. Paths come from a fixed map on the server, not from a string the caller supplied. Secrets are not stored in the same tree the web server can read.

## The browser's name was treated as a person

The next service branched on the User-Agent header, and it included a file the request could influence. A header is just text the client chooses. An include that follows client input will execute whatever file that input names, if the server is willing to run that kind of file.

The method was to read the branch, then point the include somewhere the client controlled. What was new was the combination. Spoofing a browser name is trivial. The damage came from the include, which turned a cosmetic check into code execution.

The lesson is that a header is not a credential, and a path is not a filename you should open just because a request mentioned it.

Mitigation: ignore User-Agent for authorization. Do not include or require a file whose name comes from the request. Disable remote inclusion. Run the application as a user that cannot read the rest of the system, and do not execute files from any directory a visitor can write.

## The parameter became part of the query

One service built a database query by splicing a parameter into the statement text. The parameter was then able to change the query instead of staying a value. That is SQL injection. Once a parameter sits inside the statement, a scanner can see the bug as easily as a person can.

The method was to find a parameter that was copied into the query, and to confirm that changing it changed the statement rather than a bound value. The automated steps of that confirmation are not part of this writeup.

What was new was how little custom work the bug required. The earlier levels needed reading a script. This one needed only a parameter in the wrong place. The lesson is that string-building a query is the same mistake as string-building a shell command. A different interpreter, the same failure.

Mitigation: send the statement and the values separately. Use parameterized queries. Give the application a database account that cannot read tables it does not need, so a broken query has less to return.

## Encoding was used as if it were encryption

The last response carried a blob that decoded into account material. The transformation was reversible by anyone, with no key.

The method was to recognize the encoding and reverse it. What was new was the disguise. A blob looks opaque in a response body. Opacity is not a key. The lesson is that encoding is for transport. Encryption is for secrecy, and a password in either form does not belong in a response.

Mitigation: do not return credentials, encoded or not. Store a password verifier the server can check without being able to show the password back. If a field must be confidential in transit, use TLS, and still do not put the secret in the body.

## What would have stopped the series

Each level is a different costume on one decision: the server trusted a fact the client was free to choose.

A short list covers the series.

- The browser may display and collect. The server decides.
- Passwords, queries, and commands are data, passed through an API that does not parse them as language.
- Session state lives on the server. The cookie is only a pointer to it.
- Source, backups, and account dumps are not URLs.
- A header, a hidden field, and an encoded blob are all still input.

The original report is a trace of how far each of those trusts could be pushed. The trace itself, including the values that made each service answer, is not published here.
