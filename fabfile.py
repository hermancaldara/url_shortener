from fabric.api import local, cd, run, env, sudo

env.roledefs = {
    'dev': ['vagrant@192.168.33.10'],
    'prod': ['url-shortener.hermancaldara.com']
}
env.colorize_errors = True

PROJECT_NAME = 'url_shortener'
BASE_DIR = '/var/www/'
CODE_DIR = '/var/www/%s/' % PROJECT_NAME
VIRTUALENV_NAME = PROJECT_NAME
VIRTUALENV_DIR = '%svirtualenv' % CODE_DIR


def deploy():
    test()
    clone_or_update()
    requirements()
    migrate()
    collect_statics()
    restart_gunicorn()
    copy_nginx_config_file()
    restart_nginx()


def test():
    local('python manage.py test --settings=core.settings_test')


def clone_or_update():
    run('if test -d %s; then\
            cd %s;\
            git pull origin master;\
        else\
            cd %s;\
            git clone https://github.com/hermancaldara/url_shortener.git;\
        fi' % (CODE_DIR, CODE_DIR, BASE_DIR))


def requirements():
    with cd(CODE_DIR):
        run('if test -d %s; then\
                %s/bin/pip install -r requirements.txt;\
            else\
                virtualenv %s;\
                %s/bin/pip install -r requirements.txt;\
            fi' % (VIRTUALENV_DIR, VIRTUALENV_DIR, VIRTUALENV_DIR, VIRTUALENV_DIR))


def migrate():
    with cd(CODE_DIR):
        run('%s/bin/python manage.py migrate' % VIRTUALENV_DIR)


def collect_statics():
    with cd(CODE_DIR):
        run('%s/bin/python manage.py collecstatic --noinput' % VIRTUALENV_DIR)


def restart_gunicorn():
    with cd(CODE_DIR):
        run(
            "ps aux | grep gunicorn | grep -v grep | awk '{ print $2 }' | xargs kill -9 && " +
            "%s/bin/gunicorn --config gunicorn_config.py core.wsgi" % VIRTUALENV_DIR,
            pty=False
        )


def copy_nginx_config_file():
    with cd(CODE_DIR):
        sudo('\
            cp url_shortener.conf /etc/nginx/sites-available/;\
            if test ! -e /etc/nginx/sites-enabled/url_shortener.conf; then\
                ln -s /etc/nginx/sites-available/url_shortener.conf /etc/nginx/sites-enabled/url_shortener.conf;\
            fi;\
        ')


def restart_nginx():
    with cd(CODE_DIR):
        sudo('/etc/init.d/nginx restart')
