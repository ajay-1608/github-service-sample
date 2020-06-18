# import socket
# import tqdm
# import os
# import time
# about time mf
# # device's IP address
# CLIENT_HOST = "0.0.0.0"
# CLIENT_PORT = 9898
# # receive 4096 bytes each time
# BUFFER_SIZE = 4096
# SEPARATOR = "<SEPARATOR>"
# # create the CLIENT socket
# # TCP socket
# s = socket.socket()
# # bind the socket to our local address
# s.bind((CLIENT_HOST, CLIENT_PORT))
# # enabling our CLIENT to accept connections
# # 5 here is the number of unaccepted connections that
# # the system will allow before refusing new connections
# s.listen(5)
# print(f"[*] Listening as {CLIENT_HOST}:{CLIENT_PORT}")
# # accept connection if there is any
# CLIENT_socket, address = s.accept()
# # if below code is executed, that means the sender is connected
# print(f"[+] {address} is connected.")
#
# # receive the file infos
# # receive using CLIENT socket, not CLIENT socket
# received = CLIENT_socket.recv(BUFFER_SIZE).decode()
# filename, filesize = received.split(SEPARATOR)
# # remove absolute path if there is
# filename = os.path.basename(filename)
# # convert to integer
# filesize = int(filesize)
# # start receiving the file from he socket
# # and writing to the file stream
# progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
# with open(filename, "wb") as f:
# 	for _ in progress:
# 		# read 1024 bytes from the socket (receive)
# 		bytes_read = CLIENT_socket.recv(BUFFER_SIZE)
# 		if not bytes_read:
# 			# nothing is received
# 			# file transmitting is done
# 			break
# 			# write to the file the bytes we just received
# 			f.write(bytes_read)
# 			# update the progress bar
# 			progress.update(len(bytes_read))
#
# # close the CLIENT socket
# CLIENT_socket.close()
# # close the CLIENT socket
# s.close()
import logging
import asyncio
from rpcudp.protocol import RPCProtocol


async def sayhi(protocol, address):
    # call rpc that returns immediately
    result = await protocol.sayhi_quickly(address, "Fast Snake Plissken")
    print(result[1] if result[0] else "No response received.")

    # call rpc that delays for a bit
    result = await protocol.sayhi_slowly(address, "Slow Snake Plissken")
    print(result[1] if result[0] else "No response received.")


logging.basicConfig(level=logging.DEBUG)
loop = asyncio.get_event_loop()
loop.set_debug(True)

# Start local UDP server to be able to handle responses
listen = loop.create_datagram_endpoint(RPCProtocol, local_addr=('0.0.0.0', 4567))
transport, protocol = loop.run_until_complete(listen)

# Call remote UDP server to say hi
func = sayhi(protocol, ('192.168.0.102', 1234))
loop.run_until_complete(func)

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

transport.close()
loop.close()
#hello world hahahaha
