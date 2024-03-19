// CONFIGURATION
def DOCKER_REGISTRY = "134757864544.dkr.ecr.us-east-1.amazonaws.com"
def SLACK_CHANNEL = "t-content-tools-bots"
def KRAKEN_VERSION = "0.52.0"

// defaults
def COMMIT_SHA = "undefined"
def BRANCH_TAG = "undefined"
def BRANCH_LABEL = "undefined"
def IMAGE_TAG = "undefined"
def IMAGE_NAME = "undefined"
def BUILD_TIME = "undefined"
def RELEASE_TAG = "undefined"
def skipRemainingSteps = false


pipeline {

    agent {
        label 'default'
    }

    options {
        ansiColor("xterm")
        buildDiscarder(logRotator(numToKeepStr:"50"))
        timeout(time: 30, unit: "MINUTES")
        timestamps()
    }

    environment {
        COMMIT_MESSAGE = sh (script: 'git log -1 --pretty=%B', returnStdout: true).replaceAll('\"','\'').replaceAll("\n"," ").replaceAll("\r","").trim()
        SERVICE_NAME = "${JOB_NAME.tokenize('/')[2]}".toLowerCase()
        AWS_DEFAULT_REGION = "us-east-1"
    }

    stages {
        stage("Checkout Repo") {
            steps {
                checkout scm

                script {
                    COMMIT_SHA = sh(returnStdout: true, script: 'git rev-parse --short HEAD').trim()
                    BRANCH_LABEL = "${env.BRANCH_NAME}"
                    BRANCH_TAG = env.BRANCH_NAME.replaceAll('/', '-').replaceAll('_','-').toLowerCase()
                    IMAGE_TAG = "${BRANCH_TAG}-${BUILD_ID}-${COMMIT_SHA}"
                    BUILD_TIME = sh(returnStdout: true, script: 'date +%s').trim()
                    RELEASE_TAG = BRANCH_TAG
                    IMAGE_NAME = "threatexchange-hma"
                }
            }
        }

        stage('Build Containers') {
            steps {
                script {
                    docker.withRegistry("${ECR}", "${ECR_ARN}") {
                        sh """
                            docker build hasher-matcher-actioner/ \
                                -t ${IMAGE_NAME}:${IMAGE_TAG} \
                                -f hasher-matcher-actioner/Dockerfile

                            docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${DOCKER_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}
                        """
                    }
                }
            }
        }

        stage('Publish Containers') {
            steps {
                script {
                    docker.withRegistry("${ECR}", "${ECR_ARN}") {
                        sh """
                            docker push ${DOCKER_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            cleanWs();
        }
        success {
            slackSend(
                color: "good",
                channel: "${SLACK_CHANNEL}",
                message: """
                *SUCCESS: <${env.RUN_DISPLAY_URL}|${env.JOB_NAME} #${env.BUILD_NUMBER}>* <https://github.com/Giphy/ThreatExchange/commit/${COMMIT_SHA}|`${COMMIT_SHA}`>

                Container Ready for Deploy: `${DOCKER_REGISTRY}/${IMAGE_NAME}:${BRANCH_TAG}`
                """.stripMargin().stripIndent(),
            )
        }
        failure {
            slackSend(
                color: "danger",
                channel: "${SLACK_CHANNEL}",
                message: """
                *FAILURE: <${env.RUN_DISPLAY_URL}|${env.JOB_NAME} #${env.BUILD_NUMBER}>* <https://github.com/Giphy/ThreatExchange/commit/${COMMIT_SHA}|`${COMMIT_SHA}`>

                See more info: ${env.RUN_DISPLAY_URL}
                """.stripMargin().stripIndent(),
            )
        }
    }

}
