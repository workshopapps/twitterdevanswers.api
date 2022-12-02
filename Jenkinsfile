pipeline { 
    agent any 
    options {
            skipStagesAfterUnstable()
        }
    stages {
        stage('Build') { 
            steps { 
                sh 'pip install -r requirements.txt'
            }
        }
        
        stage('Deploy to Production') {
            steps {
		    sh "sudo cp -rf ${WORKPACE}/twitterdevanswers.api/* /home/judgejudy/twitterdevanswers.api/backend"
		    //  sh "sudo su - judgejudy && whoami"
	    	 //  sh "sudo pm2 stop main"
                     sh "sudo pm2 start /home/judgejudy/twitterdevanswers.api/main.py --interpreter python3 --port 5567"
            }
        }
    }
}
