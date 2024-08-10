import re

import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request, "text": ""})


@app.post("/", response_class=HTMLResponse)
async def submit_form(request: Request, text: str = Form(...)):
    return templates.TemplateResponse("form.html", {"request": request, "text": echo_handler(text)})


def echo_handler(text: str):
    gramms = re.findall('([0-9.]{1,5})г', text)
    calories, protein, fat, carbs = (re.findall(f'([0-9.]{{1,5}}){char}', text) for char in ['К', 'Б', 'Ж', 'У'])

    return '\n'.join([
        text,
        '',
        'Вывод:',
        f'{round(sum([float(x) * float(y) * 0.01 for x, y in zip(gramms, calories)]), 2)} кал',
        f'{round(sum([float(x) * float(y) * 0.01 for x, y in zip(gramms, protein)]), 2)} белков',
        f'{round(sum([float(x) * float(y) * 0.01 for x, y in zip(gramms, fat)]), 2)} жиров',
        f'{round(sum([float(x) * float(y) * 0.01 for x, y in zip(gramms, carbs)]), 2)} углеводов'
    ])


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)