pipeline {
    agent any

    tools {
        sonarQubeScanner 'SonarScanner'
    }

    environment {
        // ── SonarQube ──────────────────────────────────────────────
        // Cambiado de localhost a sonarqube para compatibilidad con Docker
        SONAR_HOST_URL          = 'http://sonarqube:9000'
        SONAR_BACKEND_PROJECT   = 'EcoEnergy-Backend'
        SONAR_FRONTEND_PROJECT  = 'EcoEnergy-Frontend'
    }

    stages {

        // ════════════════════════════════════════════════════════════
        // 1. CHECKOUT
        // ════════════════════════════════════════════════════════════
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        // ════════════════════════════════════════════════════════════
        // 2. INSTALL DEPENDENCIES  (backend & frontend in parallel)
        // ════════════════════════════════════════════════════════════
        stage('Install Dependencies') {
            parallel {
                stage('Backend Dependencies') {
                    steps {
                        dir('backend') {
                            sh '''
                                echo "══ Creating Python virtual environment ══"
                                python3 -m venv venv
                                . venv/bin/activate
                                pip install --upgrade pip
                                pip install -r requirements.txt
                            '''
                        }
                    }
                }
                stage('Frontend Dependencies') {
                    steps {
                        dir('frontend') {
                            sh '''
                                echo "══ Installing Node.js dependencies ══"
                                npm install
                            '''
                        }
                    }
                }
            }
        }

        // ════════════════════════════════════════════════════════════
        // 3. RUN TESTS  (backend & frontend in parallel)
        // ════════════════════════════════════════════════════════════
        stage('Run Tests') {
            parallel {
                stage('Backend Tests') {
                    steps {
                        dir('backend') {
                            sh '''
                                echo "══ Running pytest with coverage ══"
                                . venv/bin/activate
                                python -m pytest \
                                    --junitxml=test-results.xml \
                                    --cov=src \
                                    --cov-report=xml:coverage.xml \
                                    --cov-report=term-missing \
                                    -v
                            '''
                        }
                    }
                    post {
                        always {
                            junit 'backend/test-results.xml'
                        }
                    }
                }
                stage('Frontend Tests') {
                    steps {
                        dir('frontend') {
                            sh '''
                                echo "══ Running vitest with coverage ══"
                                npx vitest run \
                                    --reporter=junit \
                                    --outputFile=test-results.xml \
                                    --coverage
                            '''
                        }
                    }
                    post {
                        always {
                            junit 'frontend/test-results.xml'
                        }
                    }
                }
            }
        }

        // ════════════════════════════════════════════════════════════
        // 4. SONARQUBE ANALYSIS  (backend & frontend in parallel)
        // ════════════════════════════════════════════════════════════
        stage('SonarQube Analysis') {
            parallel {
                stage('SonarQube - Backend') {
                    steps {
                        dir('backend') {
                            withCredentials([string(credentialsId: 'sonar-backend-token', variable: 'SONAR_BACKEND_TOKEN')]) {
                                withSonarQubeEnv('SonarQube') {
                                    script {
                                        def scannerHome = tool 'SonarScanner'
                                        sh """
                                            ${scannerHome}/bin/sonar-scanner \
                                                -Dsonar.projectKey=${SONAR_BACKEND_PROJECT} \
                                                -Dsonar.host.url=${SONAR_HOST_URL} \
                                                -Dsonar.token=\$SONAR_BACKEND_TOKEN \
                                                -Dsonar.sources=src \
                                                -Dsonar.tests=test \
                                                -Dsonar.python.version=3.12 \
                                                -Dsonar.python.coverage.reportPaths=coverage.xml \
                                                -Dsonar.exclusions=venv/**,__pycache__/**,.pytest_cache/** \
                                                -Dsonar.sourceEncoding=UTF-8
                                        """
                                    }
                                }
                            }
                        }
                    }
                }
                stage('SonarQube - Frontend') {
                    steps {
                        dir('frontend') {
                            withCredentials([string(credentialsId: 'sonar-frontend-token', variable: 'SONAR_FRONTEND_TOKEN')]) {
                                withSonarQubeEnv('SonarQube') {
                                    script {
                                        def scannerHome = tool 'SonarScanner'
                                        sh """
                                            ${scannerHome}/bin/sonar-scanner \
                                                -Dsonar.projectKey=${SONAR_FRONTEND_PROJECT} \
                                                -Dsonar.host.url=${SONAR_HOST_URL} \
                                                -Dsonar.token=\$SONAR_FRONTEND_TOKEN \
                                                -Dsonar.sources=src \
                                                -Dsonar.tests=test \
                                                -Dsonar.test.inclusions=**/*.test.js,**/*.test.ts,**/*.test.tsx \
                                                -Dsonar.javascript.lcov.reportPaths=coverage/lcov.info \
                                                -Dsonar.exclusions=node_modules/**,.next/**,dist/**,build/** \
                                                -Dsonar.sourceEncoding=UTF-8
                                        """
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        // ════════════════════════════════════════════════════════════
        // 5. QUALITY GATE
        // ════════════════════════════════════════════════════════════
        stage('Quality Gate') {
            steps {
                echo '══ Waiting for SonarQube Quality Gate ══'
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
    }

    // ════════════════════════════════════════════════════════════════
    // POST-BUILD ACTIONS
    // ════════════════════════════════════════════════════════════════
    post {
        success {
            echo '✅ Pipeline completed successfully — all tests passed and Quality Gate met.'
        }
        failure {
            echo '❌ Pipeline FAILED — check test results or SonarQube Quality Gate.'
        }
        always {
            echo '📋 Archiving test and coverage reports…'
            node('') {
                archiveArtifacts artifacts: 'backend/coverage.xml, backend/test-results.xml, frontend/test-results.xml, frontend/coverage/**', allowEmptyArchive: true
                cleanWs()
            }
        }
    }
}