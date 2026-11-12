# Security

## Communication between servers: TCP, UDP, HTTP, REST, RPC

Security: C I A

- Confidentiality: Only authorized parties can read the data.
- Integrity: data is not secretly altered in transit.
- Availability: system still answers while under attack.

HTTP: every word in the request is readable by anyone standing in the middle of the connection.

HTTPS: HTTP running over TLS - data encrypted before it leaves the machine.

### TLS: Handshake:

- Client send ClientHello + with cipher suites it supports. (cipher: An algorithm to encrypt)
- Server replies with a ServerHello and a certificate - with a trusted Certificate Authority (Confirm this is a real server)
- Two sides exchange keys and agree on a session key -> use fast symmetric encryption (decrypt - encrypt)

## Authentication vs Authorization - bcrypt and salt

- Authentication - AuthN: who are you?
- Authorization - AuthZ: what are you allowed to do?
- **Password** must never be stored as plain text in the DB. It is a hash of the password: a one-way function. One more thing, two users use the same password get the same hash, so hackers can hashes up in a rainbow table of millions of common passwords.
- bcrypt: fixes both problems. Each password is mixed with a random salt (a random string before hash) - different for every user. bcrypt also has a cost factor which raising the cost by one doubles the hashing time -> computers get faster -> raise the cost.

- Login successfully -> server issues a session or a token for later requests. The token travel in a cookie marked HttpOnly (avoid JS read), only send via HTTPS, SameSite: stop sending cookies with request from other pages, plus limited on cross-site (# domains, pages). Role-based access control decides which resources that token may touch.

### 3. OAuth 2.0 - delegation without the password

OAuth 2.0 lets a third-party app access part of our data, within a narrow scope, without the password.

#### Roles:

- Resource owner: us, the owner of the data
- Client - third party: Asking for access.
- Authorization server: where we login and consent. It holds the data.

OAuth is authorization not authentication.

#### Authorization flow:

1. Client redirects you to the authorization server.
2. login and consent to the requested scope (read-only)
3. Authorization server returns an authorization code.
4. Client exchanges that code with a code verifier for access token and a refresh token.
5. Client calls the resource server with the access token.
6. On expiry: use the refresh token to get a new access token - no need for the user to login again.

The code is single-use and expires very quickly-> intercepting it is hard to exploit.

Mobile apps and single-page apps cannot keep a client secret because their code runs on the user's machine.

Never put an access token in a URL, because URLs end up in history logs.

## 4. SQL injection, XSS, CSRF

### SQL injection

- SQL injection: Including a code in the request: When user input is concatenated straight into a SQL statement and becomes part of the statement. The hacker needs no password, only a string that changes the meaning of the query.

```sql
Query: "SELECT * FROM users WHERE name = '" + input + "' AND password = '" + pw + "'"

Hacker input: ' OR '1'='1

Result: SELECT * FROM users WHERE name = '' OR '1'='1' AND password = 'x'
'1'='1' is always true → logged in without a password.
```

- How to fix?

* Parameterized query: prepared statement. The SQL is written in advance with placeholders -> user data only fills data positions, never to be interpreted as SQL code.

* Add one more layer: The application's database account gets only minimum privileges for reading and writing its own tables - no dropping at all.

```sql
Prepared statement: SELECT * FROM users WHERE name = ? AND password = ?
```

Hacker input ' OR '1'='1 fills the ? as plain data.
It is matched literally as a name → no match → login fails.

### Cross-site scripting

- XSS: When an attacker's code runs in the victim's browser, under the name of a trusted site.

* Stored XSS saves the malicious code in the database and show it to everyone.
* Reflected XSS: Hides the code in a link.
* DOM-based XSS: Entirely on the client side.

- Defenses:

* escape data in the right context when rendering
* set a content security policy to restict foreign scripts
* Mark cookies HttpOnly -> Malicious scripts cannot read the session cookie.

### Cross-site request forgery (CSRF)

- the attacker exploits the victim's own browser. The browser automatically sends cookies with every request to that domain including requests started from a different site.

* Hidden form on a malicious page can send a money transfer using the victim's logged in session.

- Defense: A secret CSRF token in every form, checked on the server, SameSite cookies, check the origin of the request.

## 5. Rate limiting

- Capping: how many requests one client may send in a time window.

* Password brute force
* API scraping
* Denial of service

- Defense

* Fixed Window: window boundary - there are some window, one is 100 requests in 1 min, filled 1 window -> countdown 1min -> open new window.
* sliding Window: Smoother, counts over a moving time range. Check every latest 60 seconds.
* Token Bucket: allows short, controlled bursts - good for APIs used by real users. USERS Will have a token number. After using, it will restore with a "r" speed -> use faster -> wait longer.
* Leaky bucket: give a number of token -> request limited.

### Where will we set the limit:

- API Gateway
- Load Balancer
- The counters in Redis with a TTL
- Always return 429 too many requests with a retry-after header.
- Limit by: IP for public APIs, by user for logged in APIs, by API key for partners.

**Recap**:
Who attacks, how and which layer stops them?
