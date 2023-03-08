import socket
from datetime import datetime


# connect to server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.bind(('127.0.0.1', 12345))
data, addr = client_socket.recvfrom(4096)


# global variables: the essential elements of data packet
Start_of_Packet_identifier = int("0xffff", 16)
End_of_Packet_identifier = int("0xffff", 16)
Client_id = 250
Acc_Per = int("0xfff8", 16)
Access_OK = int("0xfffb", 16)
Not_Paid = int("0xfff9", 16)
Not_Exist = int("0xfffa", 16)

def build_data_packets():
    """read five messages that need to be transmitted"""
    with open('input.txt') as f:
        msg_list = f.readlines()

    packets = []
    # for each line of messages, build an individual data packet
    for msg in msg_list:
        msg_parts = msg.split(", ")
        segment_no = int(msg_parts[0])
        source_subscriber_no = msg_parts[1]
        tech = msg_parts[2]
        length = len(source_subscriber_no + tech)
        packet = Start_of_Packet_identifier.to_bytes(2, 'big') + Client_id.to_bytes(1, 'big') + Acc_Per.to_bytes(2, 'big') +\
                 segment_no.to_bytes(1, 'big') + length.to_bytes(1, 'big') + int(tech).to_bytes(1, 'big') + \
                 int(source_subscriber_no).to_bytes(5, 'big') + End_of_Packet_identifier.to_bytes(2, 'big')
        packets.append(packet)

    return packets


def ini_output():
    """clear and initialize the output file"""
    file = open('output_client.txt', 'w')
    file.truncate(0)
    now = datetime.now()
    file.write("Welcome to my program, now is: " + now.strftime("%H:%M:%S"))
    file.write("\n\nClient receives the following responses:\n\n")
    file.close()


data_packets = build_data_packets()  # build a packets for all messages
ini_output()


for i in range(5):
    buffer = data_packets[i]
    print(buffer)
    client_socket.sendto(buffer, addr)
    response, addr = client_socket.recvfrom(4096)
    print(response)
    keyword = response[3:5]
    if keyword == Access_OK.to_bytes(2, 'big'):
        print("run")
        subscriber = int.from_bytes(response[8:-2], 'big')
        sentense = f"The segment no.{int(response[5])}, subscriber {subscriber} permitted to access the network message.\n"
        print(sentense)
        # write in output file
        file = open('output_client.txt', 'a')
        file.write(sentense)
        file.close()
    elif keyword == Not_Exist.to_bytes(2, 'big'):
        error_seg_no = int(response[5])
        error_subscriber = int.from_bytes(response[8:-2], 'big')
        sentense1 = f"The segment no.{error_seg_no}, subscriber {error_subscriber}, "
        sentense2 = f"was rejected because it doesn't exist.\n"
        print(sentense1 + sentense2)
        # write in output file
        file = open('output_client.txt', 'a')
        file.write(sentense1 + sentense2)
        file.close()
    else:
        error_seg_no = int(response[5])
        error_subscriber = int.from_bytes(response[8:-2], 'big')
        sentense1 = f"The segment no.{error_seg_no}, subscriber {error_subscriber}, "
        sentense2 = f"was rejected because the bill has not been paid yet.\n"
        print(sentense1 + sentense2)
        file = open('output_client.txt', 'a')
        file.write(sentense1 + sentense2)
        file.close()