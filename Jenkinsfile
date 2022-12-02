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
			    sh "sudo cp -fr ${WORKSPACE}/app/* /home/judgejudy/twitterdevanswers.api/backend"
			    sh "sudo su - judgejudy && whoami"
			   // sh "sudo pm2 stop main"
			    //sh "python3 -m venv venv"
			    //sh "source venv/bin/activate"
			    //sh "pip install -r requirements.txt"
			    sh "pm2 start /home/judgejudy/twitterdevanswers.api/backend/main.py --interpreter python3 -p 3310"
		    }
		}
	    }
	}
