Welcome to the network access permission identification program!

In this program, client will request identification from the server.
So client first send the information of subscriber's phone number and the network type to server.
Server will receive the information and search in database to find the record of payment.
If the subscriber has paid bills for the specific network, server will send ACK(acknowledge) to client.
On the other hand, server will report error if the subscriber is not found or the network type doesn't match or user hasn't paid yet.

In the input.txt, the first two network access request will be approved.
Yet the third request for 4G network will be rejected because the subscriber has only paid for 3G.
The fourth request will be rejected because the user hasn't made payment for the cellular network.
The fifth request will be rejected either because the phone number doesn't exist in the verification database.

I used PyCharm 2022.3.2 to run the program and import two modules: socket, datetime.

Honglin