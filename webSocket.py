import ssl
import asyncio
import websockets

the_clients = set()

async def handler(websocket, path):
    the_clients.add(websocket)
    try:
        async for message in websocket:
            await asyncio.gather(*[client.send(message) for client in the_clients if client != websocket])
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        the_clients.remove(websocket)

async def start_server():
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain("cert.pem", "key.pem")  # Provide your certificate and key

    server = await websockets.serve(handler, "0.0.0.0", 8765, ssl=ssl_context)
    print("Secure server started on wss://0.0.0.0:8765")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(start_server())
w
