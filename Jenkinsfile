pipeline { 
    agent any 
    	stages {
		stage('Build_Backend') { 
		    steps { 
			sh "pip install -r requirements.txt"
			sh "pip install --upgrade 'sentry-sdk[fastapi]'"
		    }
		}
		stage('Deploy to Production') {
		    steps {
			    sh "sudo cp -fr ${WORKSPACE}/app/* /home/judgejudy/twitterdevanswers.api/app"
			    ///
			    //sh "pip install -r requirements.txt"
			    //sh "pip install --upgrade 'sentry-sdk[fastapi]'"
			    sh "sudo bash /home/judgejudy/start_twitterdev.api.sh"
			    sh "sudo systemctl restart devask-backend.service"
		    }
		}
	    }
	}
