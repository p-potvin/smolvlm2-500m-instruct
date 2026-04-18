## 2026-04-18 - API Key Bcrypt Hashing Migration
**Vulnerability:** API Keys were hashed using simple SHA-256 with a pepper, and verified using direct database lookups.
**Learning:** Bcrypt hashing relies on generating a unique random salt per hash. Thus, standard direct DB queries `hash == db.hash` do not work anymore. You must loop over active keys in the database and verify each one sequentially.
**Prevention:** When upgrading hash algorithms from un-salted fast hashes to salted slow hashes, always remember to rewrite the lookup logic to iterate over candidates and use the verifying function (e.g., `pwd_context.verify()`) rather than doing an exact database string match.

## 2026-04-18 - Subprocess Command Injection Prevention
**Vulnerability:** Subprocesses generating Git commits used string formatting to construct commit messages and passed them to `git commit -m`.
**Learning:** While `shell=False` protects against basic command injection (e.g. `&& rm -rf /`), parameter injection or argument confusion is still possible if untrusted input slips in.
**Prevention:** Use standard input streams for passing untrusted strings as data rather than command arguments. In the context of `git commit`, this means using `-F -` and passing the message via `subprocess.run(..., input=message_string)`.
