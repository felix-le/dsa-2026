Availability vs consistency, CAP theorem

In a distributed system, you can only support two of three guarantees: Availability, consistency, and partition tolerance.

- **Consistency**: every read receives the most recent write or an error. It means all data will be the newest version, or errors will be returned if the system cannot guarantee that. Never return previous versions of data.

- **Availability**: every request receives a response, without guarantee that it contains the most recent version. It means the system will always respond to requests, however, the data returned may not be the most up-to-date version. The system prioritizes responsiveness over accuracy.

- **Partition Tolerance**: The system continues to operate despite network failures or nodes splitting apart. For example, if a internal network partition occurs, the system can still provide some level of service.

**CP vs AP:**

CP: consistency and partition tolerance: whenever network partitions occur, the system will respond with an error rather than return a potentially inconsistent response. For example, bank industry systems, where it is critical to maintain accurate account balances.

CAP Theorem — Quick Quiz

1. What is a network partition?
   A. The server is too slow
   B. Two servers cannot talk to each other
   C. The database is full
   D. Too many users log in
2. During a partition, a CP system will:
   A. Always answer with old data
   B. Return an error or time out instead of giving wrong data
   C. Delete the data
   D. Turn off partition tolerance
3. During a partition, an AP system will:
   A. Always answer, even if the data is not the latest
   B. Never answer any request
   C. Wait forever for the other server
   D. Only accept new users
4. A bank account balance should be:
   A. AP
   B. CP
5. A social media like count should be:
   A. AP
   B. CP

1B, 2B, 3A, 4B, 5A
