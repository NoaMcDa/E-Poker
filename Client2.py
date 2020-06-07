
import asyncio
import websockets

Money = 1000
Me = []





async def hello():
    uri = "ws://localhost:8765"
    result = ""
    async with websockets.connect(uri) as websocket:
            while True:
                print("enter your username: ")
                Usernameandpass = input()
                print("enter your password: ")
                Usernameandpass += "#" + input()
                print(Usernameandpass)
                await websocket.send(Usernameandpass)
                result = await websocket.recv()
                if ("welcome" in result):
                    Me.append(Usernameandpass.split("#")[0])
                    break
                else:
                    print(result)

            result = await websocket.recv()
            Me.append(result)
            print(Me)

            handstring = await websocket.recv()
            print(handstring)


            Money = int(await websocket.recv())
            print(Money)

            msg =await websocket.recv()
            print(msg)


asyncio.get_event_loop().run_until_complete(hello())

