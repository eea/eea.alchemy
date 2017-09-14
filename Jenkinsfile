pipeline {
  agent any

  environment {
        GIT_NAME = "eea.alchemy"
    }

  stages {
    stage('Tests') {
      steps {
        parallel(

          "WWW": {
            node(label: 'docker-1.13') {
              script {
                def NAME="$BUILD_TAG-www"
                try {
                  sh '''docker run -i --net=host --name="$NAME" -e GIT_NAME="$GIT_NAME" -e GIT_BRANCH="$BRANCH_NAME" eeacms/www-devel /debug.sh bin/test -v -vv -s $GIT_NAME'''
                } finally {
                  sh '''docker rm -v $NAME'''
                }
              }
            }
          },

          "KGS": {
            node(label: 'docker-1.13') {
              script {
                def NAME="$BUILD_TAG-kgs"
                try {
                  sh '''docker run -i --net=host --name="$NAME" -e GIT_NAME="$GIT_NAME" -e GIT_BRANCH="$BRANCH_NAME" eeacms/kgs-devel /debug.sh bin/test --test-path /plone/instance/src/$GIT_NAME -v -vv -s $GIT_NAME'''
                } finally {
                  sh '''docker rm -v $NAME'''
                }
              }
            }
          },

          "Plone4": {
            node(label: 'docker-1.13') {
              script {
                def NAME="$BUILD_TAG-plone4"
                try {
                  sh '''docker run -i --net=host --name="$NAME" -v /plone/instance/parts -e GIT_BRANCH="$BRANCH_NAME" -e ADDONS="$GIT_NAME" -e DEVELOP="src/$GIT_NAME" eeacms/plone-test:4 -v -vv -s $GIT_NAME'''
                } finally {
                  sh '''docker rm -v $NAME'''
                }
              }
            }
          }
        )
      }
    }

    stage('Code Analysis') {
      steps {
        parallel(

          "ZPT Lint": {
            node(label: 'docker-1.13') {
              script {
                try {
                  def NAME="$BUILD_TAG-zptlint"
                  def GIT_SRC="https://github.com/eea/$GIT_NAME.git --branch=$BRANCH_NAME"
                  sh '''docker run -i --net=host --name="$NAME" -e GIT_SRC="$GIT_SRC" eeacms/zptlint'''
                } finally {
                  sh '''docker rm -v $NAME'''
                }
              }
            }
          },

          "JS Lint": {
            node(label: 'docker-1.13') {
              script {
                def NAME="$BUILD_TAG-jslint"
                def GIT_SRC="https://github.com/eea/$GIT_NAME.git --branch=$BRANCH_NAME"
                try {
                  sh '''docker run -i --net=host --name="$NAME" -e GIT_SRC="$GIT_SRC" eeacms/jslint4java'''
                } finally {
                  sh '''docker rm -v $NAME'''
                }
              }
            }
          },

          "PyFlakes": {
            node(label: 'docker-1.13') {
              script {
                def NAME="$BUILD_TAG-pyflakes"
                def GIT_SRC="https://github.com/eea/$GIT_NAME.git --branch=$BRANCH_NAME"
                try {
                  sh '''docker run -i --net=host --name="$NAME" -e GIT_SRC="$GIT_SRC" eeacms/pyflakes'''
                } finally {
                  sh '''docker rm -v $NAME'''
                }
              }
            }
          },

          "i18n": {
            node(label: 'docker-1.13') {
              script {
                  def NAME="$BUILD_TAG-i18n"
                  def GIT_SRC="https://github.com/eea/$GIT_NAME.git --branch=$BRANCH_NAME"
                try {
                  sh '''docker run -i --net=host --name=$NAME -e GIT_SRC="$GIT_SRC" eeacms/i18ndude'''
                } finally {
                  sh '''docker rm -v $NAME'''
                }
              }
            }
          }
        )
      }
    }

    stage('Code Syntax') {
      steps {
        parallel(

          "JS Hint": {
            node(label: 'docker-1.13') {
              script {
                def NAME="$BUILD_TAG-jshint"
                def GIT_SRC="https://github.com/eea/$GIT_NAME.git --branch=$BRANCH_NAME"
                try {
                  sh '''docker run -i --net=host --name="$NAME" -e GIT_SRC="$GIT_SRC" eeacms/jshint'''
                } catch (err) {
                  echo "Unstable: ${err}"
                } finally {
                  sh '''docker rm -v $NAME'''
                }
              }
            }
          },

          "CSS Lint": {
            node(label: 'docker-1.13') {
              script {
                def NAME="$BUILD_TAG-csslint"
                def GIT_SRC="https://github.com/eea/$GIT_NAME.git --branch=$BRANCH_NAME"
                try {
                  sh '''docker run -i --net=host --name="$NAME" -e GIT_SRC="$GIT_SRC" eeacms/csslint'''
                } catch (err) {
                  echo "Unstable: ${err}"
                } finally {
                  sh '''docker rm -v $NAME'''
                }
              }
            }
          },

          "PEP8": {
            node(label: 'docker-1.13') {
              script {
                def NAME="$BUILD_TAG-pep8"
                def GIT_SRC="https://github.com/eea/$GIT_NAME.git --branch=$BRANCH_NAME"
                try {
                  sh '''docker run -i --net=host --name="$NAME" -e GIT_SRC="$GIT_SRC" eeacms/pep8'''
                } catch (err) {
                  echo "Unstable: ${err}"
                } finally {
                  sh '''docker rm -v $NAME'''
                }
              }
            }
          },


          "PyLint": {
            node(label: 'docker-1.13') {
              script {
                try {
                  def NAME="$BUILD_TAG-pylint"
                  def GIT_SRC="https://github.com/eea/$GIT_NAME.git --branch=$BRANCH_NAME"
                  sh '''docker run -i --net=host --name="$NAME" -e GIT_SRC="$GIT_SRC" eeacms/pylint'''
                } catch (err) {
                  echo "Unstable: ${err}"
                } finally {
                  sh '''docker rm -v $NAME'''
                }
              }
            }
          }

        )
      }
    }
  }

  post {
    changed {
      script {
        def url = "${env.BUILD_URL}/display/redirect"
        def status = currentBuild.currentResult
        def subject = "${status}: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'"
        def summary = "${subject} (${url})"
        def details = """<h1>${env.JOB_NAME} - Build #${env.BUILD_NUMBER} - ${status}</h1>
                         <p>Check console output at <a href="${url}">${env.JOB_BASE_NAME} - #${env.BUILD_NUMBER}</a></p>
                      """

        def color = '#FFFF00'
        if (status == 'SUCCESS') {
          color = '#00FF00'
        } else if (status == 'FAILURE') {
          color = '#FF0000'
        }
        slackSend (color: color, message: summary)
        emailext (subject: '$DEFAULT_SUBJECT', to: '$DEFAULT_RECIPIENTS', body: details)
      }
    }
  }
}
