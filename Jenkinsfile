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
            input{
                message "Click OK! to deploy to Production?"
                ok "OK"
            }
            steps {
                     sh "sudo cp -rf backend /home/judgejudy/twitterdevanswers.api"
                 //  sh "sudo su - judgejudy && whoami"
	    	 //  sh "sudo pm2 stop main"
                     sh "sudo pm2 start /home/judgejudy/twitterdevanswers.api/main.py --interpreter python3"
            }
        }
    }
}
