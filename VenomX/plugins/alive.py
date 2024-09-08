from VenomX import app, cdx, eor


@app.on_message(cdx(["alive"]))
async def alive_(client, message):
    return await eor(message, "**I am Alive.**")
