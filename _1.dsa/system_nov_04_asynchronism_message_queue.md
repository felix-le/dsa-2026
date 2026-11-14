# Lesson 8: asynchronism, message queue and task queue

## Problems:

In lesson 1: we know:

1. latency is the time it takes to process a request.
2. Throughput is the number of request in a period time.

However, when one thread is blocking, it will increase latency itself and reduce the throughput.

#### For example:

when we call one person, we need to wait until the person is free call. We cannot connect him whenever he is in a call.

So, in real life, users send an email -> they wait for 3 seconds until they can get the response.

During 3 seconds, the flow: user send request to a server -> the server send his email.
-> wait for database, wait for sending email, ...

#### Advantage & disadvantage:

- easy to understand, step by step
- one step is down, -> others are down -> performance of server is down
  -> Throughput is down.

## II. message queue

In lesson 5: we learned load balance: a system separate requests into multiple servers at the same time, so no servers get overload.

Queue will order requests with time flow.

### Definition:

message queue is a queue connect producer, and consumer where resolve the message. its duty is to push message into a queue.

By doing that the system will decoupling. producer and consumer will work independently.

It is a buffer while the traffic spike - when peak traffic in only few mins.

Solution names:

RabbitMQ: message broker - flexing routing - send correct addresses.
Kafka: store a mount of messages
SQS: Solution from Amazon control.

#### Tasks?

Task queue will get tasks then send them to workers then take the results.
Background jobs: working without attention from users.

In python we have Celery and RQ. One can control multiple workers while one is lighter. Their jobs:

- retry
- Scheduling
- Result tracking.

## III. Trade-off

#### The communicate way:

- At least once: it can send twice to make sure delivery successfully/.
- At most once: send only 1 time but the letter can be lost.

Dangerous: back-pressure:

Consumer is slower than producer -> Queue is longer and longer -> must choose:

- slow down producer
- reduce the message in message queue?
  --> otherwise, the server will be crashed as overload of memory.

#### IIII. When and when not

Should use:

- waiting jobs: send email, create receipts
- Traffic spike (up/down)
- retry

Shouldn't use:

- Show result immediately
- Easy job
- System is small
