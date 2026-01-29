!start.

+!start <-
    .my_name(N) ;
    .print("Hello from", N).

+!ping[source(X)] <-
    .print("I received a ping request from", X);
    .print("Going to send pong.");
    .send(X, tell, pong);
    .print("Sent.").
