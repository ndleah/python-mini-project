from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates

from utils import (
    Feed,
    add_feed_to_db,
    delete_feed_from_db,
    get_all_feeds,
    get_articles_for_feed,
)

app = FastAPI()

template_dir = Jinja2Templates(directory="templates")


@app.get("/")
async def index(request: Request):
    return template_dir.TemplateResponse("index.html", {"request": request})


@app.get("/addfeed")
async def add_feed_page(request: Request):
    return template_dir.TemplateResponse("add_feed.html", {"request": request})


@app.post("/addfeed")
async def add_feed_submit(url: str = Form(...), tag: str = Form(...)):
    feed = Feed(url)
    add_feed_to_db(url=url, title=feed.title, tag=tag, link=feed.link)
    return {"message": "add successfully"}


@app.get("/deletefeed")
async def delete_feed_page(request: Request):
    return template_dir.TemplateResponse("delete_feed.html", {"request": request})


@app.post("/deletefeed")
async def delete_feed_submit(url: str = Form(...)):
    delete_feed_from_db(url)
    return {"message": "deleted successfully"}


@app.get("/feeds_list")
async def get_rss_feeds(request: Request):
    feeds = get_all_feeds()
    return template_dir.TemplateResponse(
        "feeds_list.html", {"request": request, "feeds": feeds}
    )


@app.get("/feeds_list/{feed_id}")
async def get_feed_articles(request: Request, feed_id: int):
    articles = get_articles_for_feed(feed_id)
    articles_sorted = sorted(
        articles, key=lambda x: x.get("published_parsed"), reverse=True
    )
    return template_dir.TemplateResponse(
        "articles_list.html", {"request": request, "articles_sorted": articles_sorted}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

