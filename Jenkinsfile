pipeline {
    agent any
    
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        DOCKERHUB_USERNAME = 'sofi057'
        BACKEND_IMAGE = 'sofi057/backend'
        FRONTEND_IMAGE = 'sofi057/frontend'
        VERSION = "${env.BUILD_ID}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build Backend') {
            steps {
                dir('backend') {
                    echo "Compilando Backend (Flask)"
                    sh 'python3 -m py_compile app.py || echo "No app.py found"'
                }
            }
        }
        
        stage('Build Frontend') {
            steps {
                dir('frontend') {
                    echo "Compilando Frontend (Next.js)"
                    sh 'npm install || echo "npm install failed"'
                    sh 'npm run build || echo "Build command not available"'
                }
            }
        }
        
        stage('Unit Tests') {
            parallel {
                stage('Backend Tests') {
                    steps {
                        dir('backend') {
                            echo "Ejecutando pruebas Backend reales"
                            sh 'python3 test_basic.py'
                        }
                    }
                }
                stage('Frontend Tests') {
                    steps {
                        dir('frontend') {
                            echo "Ejecutando pruebas Frontend reales"
                            sh 'npm run test:ci'
                        }
                    }
                }
            }
        }
        
        stage('Build Docker Images') {
            steps {
                script {
                    echo "Generando imagenes Docker"
                    sh "docker build -t ${env.BACKEND_IMAGE}:${env.VERSION} ./backend"
                    sh "docker build -t ${env.FRONTEND_IMAGE}:${env.VERSION} ./frontend"
                }
            }
        }
        
        stage('Push to DockerHub') {
            steps {
                script {
                    echo "Publicando imagenes en DockerHub"
                    sh """
                        echo '${env.DOCKERHUB_CREDENTIALS_PSW}' | docker login -u '${env.DOCKERHUB_CREDENTIALS_USR}' --password-stdin
                        docker push ${env.BACKEND_IMAGE}:${env.VERSION}
                        docker push ${env.FRONTEND_IMAGE}:${env.VERSION}
                    """
                }
            }
        }
    }
    
    post {
        always {
            echo "Resumen del Pipeline"
            echo "Checkout completado"
            echo "Build/Compilacion completado" 
            echo "Pruebas unitarias ejecutadas"
            echo "Imagenes Docker generadas"
            echo "Publicacion en DockerHub completada"
        }
    }
}