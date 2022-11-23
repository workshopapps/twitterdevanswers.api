pipeline { 
    agent any 
    options {
            skipStagesAfterUnstable()
        }
    stages {
        stage('Build') { 
            steps { 
                sh 'pip install -r requirements.txt'
                sh 'uvicorn app.main:app --host 0.0.0.0 --reload' 
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
                sh 'ssh -o StrictHostKeyChecking=no deployment-user@52.203.249.167 "
                cd devask;\
                cd backend;\
                git pull origin dev; \
                cd ..;\
                docker compose down --remove-orphans;\
                docker compose up
                "'
            }
        }
    }
}
