"""
NOTE:
    the below code is to be maintained Python 2.x-compatible
    as the whole Cookiecutter Django project initialization
    can potentially be run in Python 2.x environment
    (at least so we presume in `pre_gen_project.py`).

"""
from __future__ import print_function

import os
import random
import shutil
import string

try:
    # Inspired by
    # https://github.com/django/django/blob/master/django/utils/crypto.py
    random = random.SystemRandom()
    using_sysrandom = True
except NotImplementedError:
    using_sysrandom = False

TERMINATOR = "\x1b[0m"
WARNING = "\x1b[1;33m [WARNING]: "
INFO = "\x1b[1;33m [INFO]: "
HINT = "\x1b[3;33m"
SUCCESS = "\x1b[1;32m [SUCCESS]: "

DEBUG_VALUE = "debug"


def remove_celery_files():
    file_names = [
        os.path.join("server", "settings", "components", "celery.py"),
        os.path.join("server", "apps", "oauth", "tasks.py"),
        os.path.join("server", "celery.py"),
        os.path.join(".idea", "runConfigurations", "Beat.xml"),
        os.path.join(".idea", "runConfigurations", "Worker.xml"),
        os.path.join(".idea", "runConfigurations", "Flower.xml"),
    ]
    for file_name in file_names:
        os.remove(file_name)
    shutil.rmtree(os.path.join("server", "apps", "async_tasks"))


def remove_sentry_files():
    file_names = [
        os.path.join("server", "settings", "components", "sentry.py"),
    ]
    for file_name in file_names:
        os.remove(file_name)


def remove_wechat_files():
    file_names = [
        os.path.join("server", "settings", "components", "wechat.py"),
    ]
    for file_name in file_names:
        os.remove(file_name)


def remove_meilisearch_files():
    file_names = [
        os.path.join("server", "settings", "components", "meili.py"),
    ]
    for file_name in file_names:
        os.remove(file_name)



def generate_random_string(
    length, using_digits=False, using_ascii_letters=False, using_punctuation=False
):
    """
    Example:
        opting out for 50 symbol-long, [a-z][A-Z][0-9] string
        would yield log_2((26+26+50)^50) ~= 334 bit strength.
    """
    if not using_sysrandom:
        return None

    symbols = []
    if using_digits:
        symbols += string.digits
    if using_ascii_letters:
        symbols += string.ascii_letters
    if using_punctuation:
        all_punctuation = set(string.punctuation)
        # These symbols can cause issues in environment variables
        unsuitable = {"'", '"', "\\", "$"}
        suitable = all_punctuation.difference(unsuitable)
        symbols += "".join(suitable)
    return "".join([random.choice(symbols) for _ in range(length)])


def set_flag(file_path, flag, value=None, formatted=None, *args, **kwargs):
    if value is None:
        random_string = generate_random_string(*args, **kwargs)
        if random_string is None:
            print(
                "We couldn't find a secure pseudo-random number generator on your "
                "system. Please, make sure to manually {} later.".format(flag)
            )
            random_string = flag
        if formatted is not None:
            random_string = formatted.format(random_string)
        value = random_string

    with open(file_path, "r+") as f:
        file_contents = f.read().replace(flag, value)
        f.seek(0)
        f.write(file_contents)
        f.truncate()

    return value


def set_django_secret_key(file_path):
    django_secret_key = set_flag(
        file_path,
        "!!!SET DJANGO_SECRET_KEY!!!",
        length=64,
        using_digits=True,
        using_ascii_letters=True,
    )
    return django_secret_key


def generate_random_user():
    return generate_random_string(length=32, using_ascii_letters=True)


def generate_random_password():
    return generate_random_string(length=10, using_digits=True, using_ascii_letters=True)


def set_celery_flower_user(file_path, value):
    celery_flower_user = set_flag(
        file_path, "!!!SET CELERY_FLOWER_USER!!!", value=value
    )
    return celery_flower_user


def set_sentry_enable(file_path, value):
    sentry_enable = set_flag(
        file_path, "!!!SET SENTRY_ENABLE!!!", value=value
    )
    return sentry_enable


def set_celery_flower_password(file_path, value=None):
    celery_flower_password = set_flag(
        file_path,
        "!!!SET CELERY_FLOWER_PASSWORD!!!",
        value=value,
        length=64,
        using_digits=True,
        using_ascii_letters=True,
    )
    return celery_flower_password


def append_to_gitignore_file(ignored_line):
    with open(".gitignore", "a") as gitignore_file:
        gitignore_file.write(ignored_line)
        gitignore_file.write("\n")


def set_flags_in_envs():
    envs_path = os.path.join("config", ".env.template")

    set_django_secret_key(envs_path)

    set_celery_flower_user(envs_path, value="admin")
    set_celery_flower_password(
        envs_path, value=generate_random_password()
    )


def set_sentry_flags_in_envs(value):
    envs_path = os.path.join("config", ".env.template")
    set_sentry_enable(envs_path, value=str(value))


def remove_celery_compose_dirs():
    shutil.rmtree(os.path.join("docker", "django", "celery"))


def remove_wechat():
    shutil.rmtree(os.path.join("server", "apps", "utils", "wechat.py"))


def main():
    shutil.copyfile(
        os.path.join("config", ".env.template"), os.path.join("config", ".env.example")
    )

    set_flags_in_envs()

    if "{{ cookiecutter.use_celery }}".lower() == "n":
        remove_celery_files()
        remove_celery_compose_dirs()

    if "{{ cookiecutter.use_sentry }}".lower() == "y":
        set_sentry_flags_in_envs(True)
    else:
        set_sentry_flags_in_envs(False)
        remove_sentry_files()

    if "{{ cookiecutter.use_wechat }}".lower() == "n":
        remove_wechat_files()

    if "{{ cookiecutter.use_meilisearch }}".lower() == "n":
        remove_meilisearch_files()

    os.rename(os.path.join("config", ".env.template"), os.path.join("config", ".env"))
    os.rename(os.path.join(".gitignore.template"), os.path.join(".gitignore"))

    print(SUCCESS + "Project initialized, keep up the good work!" + TERMINATOR)


if __name__ == "__main__":
    main()
