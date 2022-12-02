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
		    sh "sudo cp -rf ${WORKSPACE}/app/* /home/judgejudy/twitterdevanswers.api/app"
		    //  sh "sudo su - judgejudy && whoami"
	    	 //  sh "sudo pm2 stop main"
                     sh "sudo pm2 start /home/judgejudy/twitterdevanswers.api/app/main.py --interpreter python3 -p 5567"
            }
        }
    }
}
