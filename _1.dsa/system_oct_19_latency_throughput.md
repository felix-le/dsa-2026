# Lesson 1:

Performance vs Scalability, Latency vs Throughput

A service is scalable if adding resources increases performance proportionally (scalable).

Performance problem = slow even for a single user. Scalability problem = fast for one user, slow under heavy load.

## Latency vs Throughput

Latency is the time to complete one action. throughput is the number of actions completed per unit of time.
Aim for maximal throughput with acceptable latency.

Example:

A coffee shop, latency = time to make one cup, throughput = number of cups made per hour. It is fast but have only one staff, so when we have a lot of customers, the throughput is low. It is scalability problem.
