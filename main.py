from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None

@app.get("/tasks")
def get_tasks():
    response = supabase.table("tasks").select("*").order("id", desc=True).execute()
    return response.data

@app.post("/tasks")
def create_task(task: TaskCreate):
    response = supabase.table("tasks").insert({"title": task.title, "completed": False}).execute()
    return response.data

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):
    update_data = {k: v for k, v in task.dict().items() if v is not None}
    response = supabase.table("tasks").update(update_data).eq("id", task_id).execute()
    return response.data

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    supabase.table("tasks").delete().eq("id", task_id).execute()
    return {"message": "Task deleted successfully"}