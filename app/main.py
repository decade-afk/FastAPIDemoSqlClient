from fastapi import FastAPI, HTTPException
from .database import get_db_connection

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI with MySQL"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM items WHERE id = %s", (item_id,))
        item = cursor.fetchone()
        conn.close()
        if item:
            return {"id": item[0], "name": item[1]}
        else:
            # 确保这里正确返回404
            raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))