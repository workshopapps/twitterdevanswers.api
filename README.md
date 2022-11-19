##  Dev Ask Backend

These are instructions on how to run this app on your Local Machine for Development purposes


##   Steps on How to Successfully clone and run this app

##   Clone Repo

Make sure you have python installed on your system

     python --version
    
Clone this github repo 

     git clone https://github.com/workshopapps/twitterdevanswers.api.git
    
 Checkout to another branch (Your Task Branch)

     git checkout -b <name of branch>
     
  Pull from dev Branch

     git pull origin dev
    

##   Install Dependencies

After this repo has been successfully cloned , here are the instructions you need to follow 

Create Virtual environment

   Window users   
     
     python -m venv venv 
     
   MacOs users
     
     python3 -m venv venv
  
    
Activate virtual Environment

  Windows Users
    
    venv/Scripts/activate
  
  Mac Users
    
    source venv/Scripts/activate
  
Install Dependencies 

     pip install -r requirements.txt

Run App 

    uvicorn app.main:app --reload




