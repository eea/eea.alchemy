pipeline {
  agent any
  stages {
    stage('Tests') {
      steps {
        parallel(
          },
          "WWW": {
            node(label: 'docker-1.13') {
              sh '''
NAME="$BUILD_TAG-www"
docker run -i --net=host --name=$NAME eeacms/www-devel /debug.sh  bin/test -v -vv -s eea.alchemy
docker rm -v $NAME'''
            }
          },
          "KGS": {
            node(label: 'docker-1.13') {
              sh '''
NAME="$BUILD_TAG-kgs"
docker run -i --net=host --name=$NAME eeacms/kgs-devel /debug.sh  bin/test --test-path /plone/instance/src/eea.alchemy -v -vv -s eea.alchemy
docker rm -v $NAME'''
            }
          },
          "Plone4": {
            node(label: 'docker-1.13') {
              sh '''
NAME="$BUILD_TAG-plone4"
docker run -i --net=host --name=$NAME -v /plone/instance/parts -e ADDONS=eea.alchemy -e DEVELOP=src/eea.alchemy eeacms/plone-test -s eea.alchemy
docker rm -v $NAME'''
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
              sh '''
NAME="$BUILD_TAG-zptlint"
docker run -i --net=host --name=$NAME eeacms/zptlint https://github.com/eea/eea.alchemy.git
docker rm -v $NAME'''
            }
          },

          "JS Lint": {
            node(label: 'docker-1.13') {
              sh '''
NAME="$BUILD_TAG-jslint"
docker run -i --net=host --name=$NAME eeacms/jslint4java https://github.com/eea/eea.alchemy.git
docker rm -v $NAME'''
            }
          },

          "CSS Lint": {
            node(label: 'docker-1.13') {
              sh '''
NAME="$BUILD_TAG-csslint"
docker run -i --net=host --name=$NAME eeacms/csslint https://github.com/eea/eea.alchemy.git
docker rm -v $NAME'''
            }
          },

          "PyFlakes": {
            node(label: 'docker-1.13') {
              sh '''
NAME="$BUILD_TAG-pyflakes"
docker run -i --net=host --name=$NAME eeacms/pyflakes https://github.com/eea/eea.alchemy.git
docker rm -v $NAME'''
            }
          },

          "PyLint": {
            node(label: 'docker-1.13') {
              sh '''
NAME="$BUILD_TAG-pylint"
docker run -i --net=host --name=$NAME eeacms/pylint https://github.com/eea/eea.alchemy.git
docker rm -v $NAME'''
            }
          },

          "i18n": {
            node(label: 'docker-1.13') {
              sh '''
NAME="$BUILD_TAG-i18n"
docker run -i --net=host --name=$NAME eeacms/i18ndude https://github.com/eea/eea.alchemy.git
docker rm -v $NAME'''
            }
          },

        )
      }
    }
  }
}
