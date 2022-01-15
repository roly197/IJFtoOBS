import asyncio
import simpleobsws

loop = asyncio.get_event_loop()
ws = simpleobsws.obsws(host='127.0.0.1', port=4444, password='judo', loop=loop) # Every possible argument has been passed, but none are required. See lib code for defaults.

async def make_request():
    await ws.connect() # Make the connection to OBS-Websocket
    #result = await ws.call('GetVersion') # We get the current OBS version. More request data is not required
    #print(result) # Print the raw json output of the GetVersion request
    #await asyncio.sleep(1)

    #data = {'source': 'SB2_GoldenScore', 'render': False}
    #result = await ws.call('SetSceneItemRender', data) # Make a request with the given data
    result = await ws.call('GetCurrentScene') # Make a request with the given data
    print(result)
    print(type(result))
    print(result['name'])
    await ws.disconnect() # Clean things up by disconnecting. Only really required in a few specific situations, but good practice if you are done making requests or listening to events.

loop.run_until_complete(make_request())