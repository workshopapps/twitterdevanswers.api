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
        stage('Test'){
            steps {
                sh '$pytest'
            }
        }

        stage('Deploy to Production') {
            input{
                message "Click OK! to deploy to Production?"
                ok "OK"
            }
            steps {
                sh 'ssh -o StrictHostKeyChecking=no deployment-user@52.203.249.167 "source venv/bin/activate; \
                cd mallet/devask;\
                git pull origin dev; \
                pip install -r requirements.txt; --no-warn-script-location; \
                mkdir yes"'
            }
        }
    }
}
