import sentry_sdk
from app.routers import user, notification, questions, auth, like, answer, following, tag, blog, wallet, admin, admin_utils
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

import sys
sys.path.append('..')
# from app.routers import googleauth


# DO NOT COMMENT OUT SENTRY PACKAGE, IF YOUR CODE DOESNT WORK, pip install --upgrade 'sentry-sdk[fastapi]' WOULD INSTALL NECESSARY PACKAGES.

# Integration of Sentry Monitoring

sentry_sdk.init(
    dsn="https://45476b789dc3420faec99388d0e830c3@o4504279440097280.ingest.sentry.io/4504279970676736",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0,
)


#  Description of Dev ASk Api
description = """

 
## HTTP Methods
The following methods are used in this api :- 

* **GET** 
* **POST** 
* **UPDATE** 
* **PATCH**
* **PUT**
* **DELETE** 
"""

app = FastAPI(
    title="DEV ASK",
    description=description,
    swagger_ui_parameters={"operationsSorter": "method", "apiSorter": "alpha"}
)

origins = ['*', 'http://localhost:3000/']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
async def root():
    return {"message": "Hello world"}


app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(admin_utils.router)
app.include_router(answer.router)
app.include_router(blog.router)
app.include_router(following.router)
app.include_router(like.router)
app.include_router(notification.router)
app.include_router(questions.router)
app.include_router(tag.router)
app.include_router(user.router)
# app.include_router(googleauth.router)
app.include_router(wallet.router)
