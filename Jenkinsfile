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
			    sh "sudo cp -fr ${WORKSPACE}/app/* /home/judgejudy/twitterdevanswers.api/app"
			    sh "sudo su - judgejudy && whoami"
			   // sh "sudo pm2 stop main"
			    sh "python3 -m venv venv"
			    sh "source venv/bin/activate"
			    sh "pip install -r requirements.txt"
			    sh "sudo systemctl restart twitterdevanswers.api.service"
		    }
		}
	    }
	}
