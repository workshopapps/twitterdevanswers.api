pipeline { 
    agent any 
    options {
            skipStagesAfterUnstable()
        }
    stages {
        stage('Build and deploy to Production') {
            steps {
		    sh "sudo cp -rf ${WORKSPACE}/app/* /home/judgejudy/twitterdevanswers.api/app"
		    sh "sudo su - judgejudy && whoami"
	    	   // sh "sudo pm2 stop main"
		   sh "source venv/bin/activate; \
                   pip install -r requirements.txt; --no-warn-script-location; \
                   uvicorn app.main:app --host 0.0.0.0 --reload --port 3310"'
            }
        }
    }
}
