pipeline {
    agent any

    environment {
        IMAGE_NAME = 'sagarbompada/python-health-app'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build \
                      -t ${IMAGE_NAME}:${BUILD_NUMBER} \
                      -t ${IMAGE_NAME}:latest .
                '''
            }
        }

        stage('Test Docker Image') {
            steps {
                sh '''
                    docker run -d --rm \
                      --name python-health-test \
                      -p 18000:8000 \
                      ${IMAGE_NAME}:${BUILD_NUMBER}

                    trap 'docker stop python-health-test >/dev/null 2>&1 || true' EXIT

                    for i in $(seq 1 15); do
                      if curl -fsS http://localhost:18000/health; then
                        exit 0
                      fi
                      sleep 2
                    done

                    echo "Health check failed"
                    docker logs python-health-test || true
                    exit 1
                '''
            }
        }

        stage('Login to Docker Hub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    sh '''
                        set +x
                        echo "$DOCKER_PASS" |
                          docker login -u "$DOCKER_USER" --password-stdin
                    '''
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                sh '''
                    docker push ${IMAGE_NAME}:${BUILD_NUMBER}
                    docker push ${IMAGE_NAME}:latest
                '''
            }
        }
    }

    post {
        always {
            sh '''
                docker logout >/dev/null 2>&1 || true
                docker rm -f python-health-test >/dev/null 2>&1 || true
            '''
        }

        success {
            echo 'Build, health check, and Docker Hub push completed.'
        }

        failure {
            echo 'Pipeline failed. Review the stage logs.'
        }
    }
}
