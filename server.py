import socket
from datetime import datetime

# connect with client
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.sendto("hello client".encode("utf-8"), ('127.0.0.1', 12345))

# global variables: the essential elements of ack/reject packet
Access_OK = int("0xfffb", 16)
Not_Paid = int("0xfff9", 16)
Not_Exist = int("0xfffa", 16)
Start_of_Packet_identifier = int("0xffff", 16)
End_of_Packet_identifier = int("0xffff", 16)
Client_id = 250


def readFile():
    with open('verification.txt') as f:
        msg_list = f.readlines()
    dic = {}
    # for each line of messages, build an individual data packet
    for msg in msg_list:
        msg_parts = msg.split(", ")
        subscriber = int(msg_parts[0])
        speed = msg_parts[1]
        paid = msg_parts[2][0]
        dic[subscriber] = [speed, paid]
    return dic


# clear and initialize the output file
file = open('output_server.txt', 'w')
file.truncate(0)
now = datetime.now()
file.write("Welcome to my program, now is: " + now.strftime("%H:%M:%S"))
file.write("\n\nServer receives the following messages:\n\n")
file.close()

stats = readFile()
# print(stats)
for i in range(5):
    data, addr = server_socket.recvfrom(4096)
    segment_no = data[5]
    length = data[6]
    tech = data[7]
    b_subscriber = data[8:-2]
    print(data)
    int_subscriber = int.from_bytes(b_subscriber, "big")
    print(type(int_subscriber))
    if (not int_subscriber in stats.keys()) or (int(stats[int_subscriber][0]) != tech):
        # error 2
        print("error 2: Not exist")
        rej_msg = Start_of_Packet_identifier.to_bytes(2, 'big') + Client_id.to_bytes(1, 'big') + \
                  Not_Exist.to_bytes(2, 'big') + segment_no.to_bytes(1, 'big') + length.to_bytes(1, 'big') + \
                  tech.to_bytes(1, 'big') + b_subscriber + \
                  End_of_Packet_identifier.to_bytes(2, 'big')
        server_socket.sendto(rej_msg, addr)
        print("reject sent")
    elif stats[int_subscriber][1] == '0':
        # error 1
        print("error 1: Not paid")
        rej_msg = Start_of_Packet_identifier.to_bytes(2, 'big') + Client_id.to_bytes(1, 'big') + \
                  Not_Paid.to_bytes(2, 'big') + segment_no.to_bytes(1, 'big') + length.to_bytes(1, 'big') +\
                  tech.to_bytes(1, 'big') + b_subscriber + End_of_Packet_identifier.to_bytes(2, 'big')
        server_socket.sendto(rej_msg, addr)
        print("reject sent")
    else:
        # correct message, should send ACK
        ACK_msg = Start_of_Packet_identifier.to_bytes(2, 'big') + Client_id.to_bytes(1, 'big') +\
                  Access_OK.to_bytes(2, 'big') + segment_no.to_bytes(1, 'big') + length.to_bytes(1, 'big') +\
                  tech.to_bytes(1, 'big') + b_subscriber + End_of_Packet_identifier.to_bytes(2, 'big')
        server_socket.sendto(ACK_msg, addr)
        seq_num = segment_no  # memorize the segment_no of successfully received message
        # write in output file
        file = open('output_server.txt', 'a')
        file.write(f"{int_subscriber} has successfully been connected.\n")
        file.close()
