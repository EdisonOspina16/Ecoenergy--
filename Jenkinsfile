pipeline {
    agent any
    
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        DOCKERHUB_USERNAME = 'sofi057'
        BACKEND_IMAGE = 'sofi057/backend'
        FRONTEND_IMAGE = 'sofi057/frontend'
        MOSQUITTO_IMAGE = 'sofi057/mosquitto'
        VERSION = "${env.BUILD_ID}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build Docker Images') {
            steps {
                script {
                    // Login a DockerHub
                    sh "echo ${env.DOCKERHUB_CREDENTIALS_PSW} | docker login -u ${env.DOCKERHUB_CREDENTIALS_USR} --password-stdin"
                    
                    // Construir imágenes
                    sh "docker build -t ${env.BACKEND_IMAGE}:${env.VERSION} ./backend"
                    sh "docker build -t ${env.FRONTEND_IMAGE}:${env.VERSION} ./frontend"
                }
            }
        }
        
        stage('Push to DockerHub') {
            steps {
                script {
                    // Push de las imágenes
                    sh "docker push ${env.BACKEND_IMAGE}:${env.VERSION}"
                    sh "docker push ${env.FRONTEND_IMAGE}:${env.VERSION}"
                }
            }
        }
    }
    
    post {
        always {
            // Limpieza
            sh 'docker logout'
        }
        success {
            echo "Pipeline completado - Imágenes publicadas:"
            echo "${env.BACKEND_IMAGE}:${env.VERSION}"
            echo "${env.FRONTEND_IMAGE}:${env.VERSION}"
        }
    }
}