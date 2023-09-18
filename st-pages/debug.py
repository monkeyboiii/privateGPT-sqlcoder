from multiprocessing import Process
import streamlit as st
import time
import os
import signal


state = st.session_state
if "subpid" not in state:
    state["subpid"] = None

st.title("Controls")
start = st.button("Start")
stop = st.button("Stop")


def job():
    for _ in range(10):
        print(f"[*] In progress pid {os.getpid()}")
        time.sleep(1)


if start:
    p = Process(target=job)
    p.start()
    state["subpid"] = p.pid
    st.write("Started process with pid:", state["subpid"])

if stop:
    os.kill(state["subpid"], signal.SIGKILL)
    st.write("Stopped process with pid:", state["subpid"])
    state["subpid"] = None

print("[*] Debug refreshed...")
