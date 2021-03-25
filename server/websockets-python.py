#!/usr/bin/env python3
import asyncio
import datetime
import random
import websockets
import subprocess
import threading


async def time(websocket, path):
    proc = await asyncio.create_subprocess_exec('python3', '-q', '-i',
    # proc = await asyncio.create_subprocess_exec('bash',
                            stdin=asyncio.subprocess.PIPE,
                            stdout=asyncio.subprocess.PIPE,
                            stderr=asyncio.subprocess.PIPE)
    await websocket.send('コマンドをどうぞ')
    
    while True:
        try:
            r = await asyncio.wait_for(websocket.recv(), timeout=0.1)
        except asyncio.TimeoutError:
            pass
        else:
            #print(r.encode('utf-8')+b'\n')
            proc.stdin.write((r).encode('utf-8')+b'\n')
        # proc.stdin.flush()
        
        lines = ''
        while True:
            try:
                line = await asyncio.wait_for(proc.stdout.readline(), timeout=0.1)
            except asyncio.TimeoutError:
                if lines: 
                   await websocket.send(lines)
                break
            else:
                if line: 
                   lines = lines + line.decode('utf-8')
        
        lines = ''
        while True:        
            try:
                line = await asyncio.wait_for(proc.stderr.readline(), timeout=0.1)
            except asyncio.TimeoutError:
                if lines: 
                   await websocket.send(lines)
                break
            else:
                if line: 
                   lines = lines + line.decode('utf-8')
 
    proc.stdin.close()
    proc.terminate()
    proc.wait(timeout=0.2)

start_server = websockets.serve(time, "127.0.0.1", 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
