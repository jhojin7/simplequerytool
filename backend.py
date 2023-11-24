import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import pymysql
import pandas as pd


app = FastAPI()


@app.get("/")
def main():
    with open("asdf.html", 'r') as f:
        return HTMLResponse(f.read())


@app.get("/query")
def get_result():
    query = "select * from users"
    conn = pymysql.connect(
        host="todo-lists.c2qmblxhpvie.ap-northeast-2.rds.amazonaws.com",
        user="admin",
        password="newmasterpassword",
        database="db")
    with conn.cursor() as cursor:
        cursor.execute(query)
        res = cursor.fetchall()
        print(res)
        df = pd.DataFrame(res)
        html = df.to_html(columns=None, index=False)
    return HTMLResponse(f"""
<div id="lol">
<form hx-get="/query" hx-target="#lol">
    <label name="q" for="q"></label>
    <textarea id="q">select * from table;</textarea>
    <button type="submit">Send query</button>
</form>
<div class="result" style="border:1px solid black">{html}</div>
</div>
""")


if __name__ == "__main__":
    uvicorn.run("backend:app", reload=True)
