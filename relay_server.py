import json
import queue
import socket
import threading
import timeit
import time
from threading import Thread
from PyJEM import TEM3

BUFFER_SIZE = 1024

stage = TEM3.Stage3()
eos = TEM3.EOS3()
defl = TEM3.Def3()
lens = TEM3.Lens3()
info = {}
conn_open = False


def main():
    # Create a TCP server
    sock = socket.socket()
    host = "0.0.0.0"
    port = 12345
    print("Listening to ", host + ":" + str(port))
    sock.bind((host, port))
    sock.listen(5)

    # main loop
    while True:
        global conn_open
        global info
        connection, address = sock.accept()
        print("Got connection from", address)
        conn_open = True

        # Create an event queue that holds incoming messages and other tasks
        q = queue.Queue()

        receiving_thread = Thread(target=start_receiving, args=(connection, q))
        receiving_thread.start()

        info_thread = Thread(target=start_info_gathering, args=(q, None))
        info_thread.start()

        while True:
            task = q.get()
            if task == "#quit":
                break
            elif task == "#info":
                # info = get_state()
                connection.send(json.dumps(info).encode())
            else:
                try:
                    result = str(exec(task))
                    print(task, "-->", result)
                    # connection.send(result.encode())
                except Exception as exc:
                    print("Exception", exc)

        # wait for the receiving thread to finish and close the connection
        receiving_thread.join()
        conn_open = False
        connection.close()


def start_receiving(connection, q):
    while True:
        data = connection.recv(BUFFER_SIZE)
        if data:
            q.put(data.decode())
        else:
            q.put("#quit")
            break


def start_info_gathering(q, x):
    global conn_open
    global info
    while conn_open:
        for query in INFO_QUERIES:
            result = {}
            result["tst_before"] = time.time()
            result["val"] = eval(query + "()")
            result["tst_after"] = time.time()
            info[query] = result
        if not conn_open:
            break
        time.sleep(0.1)
        q.put("#info")


def get_state():
    results = {}
    timeit.timeit()

    for query in INFO_QUERIES:
        tic = time.perf_counter()
        results[query] = eval(query + "()")

        toc = time.perf_counter()
        print("Getting info for", query, "Took", toc - tic, "seconds")

    return results


INFO_QUERIES = ["stage.GetPos", "stage.Getf1OverRateTxNum", "stage.GetStatus", "eos.GetMagValue", "eos.GetFunctionMode"]

if __name__ == "__main__":
    main()
