from fastapi import FastAPI
from pydantic import BaseModel


class QuestionTag(BaseModel):
    id: int 
    question_id: int 
    content: str 
    answered: bool() 
    created_at: datetime()
    updated_at: datetime()


app = FastAPI()


@app.post("/tags")
async def question_tag(question_tag: QuestionTag):
    question_tag_dict = question_tag.dict()
    print(question_tag_dict) 
    
    return question_tag_dict 



# @app.post("/items/")
# async def create_item(item: Item):
#     item_dict = item.dict()
#     if item.tax:
#         price_with_tax = item.price + item.tax
#         item_dict.update({"price_with_tax": price_with_tax})
#     return item_dict
