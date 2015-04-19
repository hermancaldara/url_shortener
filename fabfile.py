from fabric.api import local, cd, run, env, sudo

env.hosts = ['192.168.33.10']
env.user = 'vagrant'
env.password = 'vagrant'
env.colorize_errors = True

PROJECT_NAME = 'url_shortener'
CODE_DIR = '/var/www/%s/' % PROJECT_NAME
VIRTUALENV_NAME = PROJECT_NAME


def deploy():
    test()
    update()
    requirements()
    migrate()
    restart_gunicorn()
    restart_nginx()


def test():
    local('python manage.py test')


def update():
    with cd(CODE_DIR):
        run('git pull origin master')


def requirements():
    with cd(CODE_DIR):
        run('$HOME/.virtualenvs/%s/bin/pip install -r requirements.txt' % VIRTUALENV_NAME)


def migrate():
    with cd(CODE_DIR):
        run('$HOME/.virtualenvs/%s/bin/python manage.py migrate' % VIRTUALENV_NAME)


def restart_gunicorn():
    with cd(CODE_DIR):
        run(
            "ps aux | grep gunicorn | grep -v grep | awk '{ print $2 }' | xargs kill -9 && " +
            "source $HOME/.virtualenvs/%s/bin/activate &&" % VIRTUALENV_NAME +
            "gunicorn --config gunicorn_config.py core.wsgi",
            pty=False
        )


def restart_nginx():
    with cd(CODE_DIR):
        sudo('/etc/init.d/nginx restart')
