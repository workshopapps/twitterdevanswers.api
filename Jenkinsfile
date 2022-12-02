pipeline { 
    agent any 
    	stages {
		stage('Build') { 
		    steps { 
			sh "pip install -r requirements.txt"
		    }
		}
		stage('Deploy to Production') {
		    steps {
			    sh "sudo cp -rf ${WORKSPACE}/app/* /home/judgejudy/twitterdevanswers.api/app"
			    sh "sudo su - judgejudy && whoami"
			   // sh "sudo pm2 stop main"
			    sh "python3 -m venv venv"
			    sh "source venv/bin/activate"
			    sh "pip install -r requirements.txt"
			    sh "uvicorn app.main:app --host 0.0.0.0 --reload --port 3310 &""
		    }
		}
	    }
	}
