from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

import splendor_bot
from splendor_bot.server.router import router as splendor_router


app = FastAPI()
# https://stackoverflow.com/questions/73917396/why-doesnt-uvicorn-pick-up-changes-to-css-files
app.mount(
    "/css",
    StaticFiles(
        directory=Path(splendor_bot.__file__).parent.parent.parent.absolute() / "assets/css"
    ),
    name="css",
)

app.include_router(splendor_router)


@app.get("/", response_class=RedirectResponse)
def redirect_splendor(request: Request):
    # return RedirectResponse("/splendor")
    return RedirectResponse("/splendor/reactive_tests")
