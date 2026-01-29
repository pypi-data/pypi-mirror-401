
refactoring_advisor_url("http://127.0.0.1:9989").
validator_url("http://127.0.0.1:9999").

!start.


+!start <-
    .my_name(N) ;
    .print("Hello from", N).

+spec(S) <-
    .print("ack:spec").

+upload(C) : not code(_) <-
    .print("uploaded data incoming.");
    -upload(C) ;
    +code(C).

+code(C) : spec(S) & refactoring_advisor_url(R) <-
    .print("Received a code to refactor.") ;
    .send_str(R, tell, S) ;
    .wait(1000);
    .send_str(R, upload, C).

+upload(C) : code(_)  <-
    .print("received refactored code") ;
    .print(C) ;
    -upload(C);
    +proposal(C).

+proposal(C) : spec(S) & validator_url(V) <-
    .print("Going to submit the proposal to", V);
    .send_str(V, tell, S) ;
    .wait(1000);
    .send_str_cb(V, propose, C, validation).

+proposal(_) <- .print("error").

+!validation("valid") : proposal(C) <-
    .print("Received a validation.") ;
    +final(C).

+!validation("invalid") : code(C) <-
    .print("Received an invalidation.") ;
    +final(C).

+final(C) <-
    .print("Final code:") ;
    .print(C).