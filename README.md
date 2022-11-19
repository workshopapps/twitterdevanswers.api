#  Dev Ask Backend

These instructions will get you a copy of Dev Ask project up and running on your local machine for development and testing purposes. 


##   Steps on Setting Up and running this Project Successfully

###   Clone Repo

Make sure you have python installed on your system

     python --version
    
Clone this github repo 

     git clone https://github.com/workshopapps/twitterdevanswers.api.git
    
 Checkout to another branch (Your Task Branch)

     git checkout -b <name of branch>
     
  Pull from dev Branch

     git pull origin dev
    

###   Install Dependencies

After this repo has been successfully cloned , here are the instructions you need to follow :-

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

###   Running the tests
Run the command below in the root folder to execute the written tests

    pytest tests
