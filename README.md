# Tapease

## Installation

1. `git clone https://github.com/web2py/web2py.git web2py` [web2py](http://www.web2py.com/init/default/download)
2. Setup [MySQL Community Server](http://dev.mysql.com/downloads/mysql) locally.
  - `create schema tapease`
  - Create a new user with all schema privileges for the mmwd schema:
    - Username: `web2py`
    - Password: [password]
3. `cd web2py/applications`
4. `git clone git@github.com:henrynguyen7/tapease.git tapease`
5. `mkdir tapease/private`
6. Add a file named `conf.json` to the `private` folder with the following:

>        {
>            "mysql": {
>               "username": "web2py",
>               "password": "asdfasdf",
>               "database": "tapease",
>               "hostname": "127.0.0.1",
>               "port": "3306"
>            }
>        }

7. `pip install -r tapease/requirements.txt`
8. Copy routes.py to web2py root directory.
9. Run web2py: `python web2py.py`

From here, you can view the administrative console at [http://127.0.0.1:8000/admin/default/site](http://127.0.0.1:8000/admin/default/site) or go directly to the site at [http://127.0.0.1:8000/tapease/default/index](http://127.0.0.1:8000/tapease/default/index).

## Configuring Logging

In the server root dir, create a file named `logging.conf` with the following contents:

>        #  Configure the Python logging facility.
>        #  To use this file, copy it to logging.conf and edit logging.conf as required.
>        #  See http://docs.python.org/library/logging.html for details of the logging facility.
>        #  Note that this is not the newer logging.config facility.
>        #
>        #  The default configuration is console-based (stdout) for backward compatibility;
>        #  edit the [handlers] section to choose a different logging destination.
>        #
>        #  Note that file-based handlers are thread-safe but not mp-safe;
>        #  for mp-safe logging, configure the appropriate syslog handler.
>        #
>        #  To create a configurable logger for application 'myapp', add myapp to
>        #  the [loggers] keys list and add a [logger_myapp] section, using
>        #  [logger_welcome] as a starting point.
>        #
>        #  In your application, create your logger in your model or in a controller:
>        #
>        #  import logging
>        #  logger = logging.getLogger("web2py.app.myapp")
>        #  logger.setLevel(logging.DEBUG)
>        #
>        #  To log a message:
>        #
>        #  logger.debug("You ought to know that %s" % details)
>        #
>        #  Note that a logging call will be governed by the most restrictive level
>        #  set by the setLevel call, the [logger_myapp] section, and the [handler_...]
>        #  section. For example, you will not see DEBUG messages unless all three are
>        #  set to DEBUG.
>        #
>        #  Available levels: DEBUG INFO WARNING ERROR CRITICAL
>
>        [loggers]
>        keys=root,rocket,markdown,web2py,rewrite,cron,app,welcome,mymobilewatchdog
>
>        [handlers]
>        keys=consoleHandler,messageBoxHandler,rotatingFileHandler
>        #keys=consoleHandler,rotatingFileHandler
>        #keys=osxSysLogHandler
>        #keys=notifySendHandler
>
>        [formatters]
>        keys=simpleFormatter
>
>        [logger_root]
>        level=WARNING
>        handlers=consoleHandler,rotatingFileHandler
>
>        [logger_web2py]
>        level=WARNING
>        handlers=consoleHandler,rotatingFileHandler
>        qualname=web2py
>        propagate=0
>
>        #  URL rewrite logging (routes.py)
>        #  See also the logging parameter in routes.py
>        #
>        [logger_rewrite]
>        level=WARNING
>        qualname=web2py.rewrite
>        handlers=consoleHandler,rotatingFileHandler
>        propagate=0
>
>        [logger_cron]
>        level=WARNING
>        qualname=web2py.cron
>        handlers=consoleHandler,rotatingFileHandler
>        propagate=0
>
>        # generic app handler
>        [logger_app]
>        level=WARNING
>        qualname=web2py.app
>        handlers=consoleHandler,rotatingFileHandler
>        propagate=0
>
>        # mymobilewatchdog app handler
>        [logger_tapease]
>        level=DEBUG
>        qualname=web2py.app.tapease
>        handlers=consoleHandler,rotatingFileHandler
>        propagate=0
>
>        # loggers for legacy getLogger calls: Rocket and markdown
>        [logger_rocket]
>        level=WARNING
>        handlers=consoleHandler,messageBoxHandler,rotatingFileHandler
>        qualname=Rocket
>        propagate=0
>
>        [logger_markdown]
>        level=WARNING
>        handlers=consoleHandler,rotatingFileHandler
>        qualname=markdown
>        propagate=0
>
>        [handler_consoleHandler]
>        class=StreamHandler
>        level=WARNING
>        formatter=simpleFormatter
>        args=(sys.stdout,)
>
>        [handler_messageBoxHandler]
>        class=gluon.messageboxhandler.MessageBoxHandler
>        level=ERROR
>        formatter=simpleFormatter
>        args=()
>
>        [handler_notifySendHandler]
>        class=gluon.messageboxhandler.NotifySendHandler
>        level=ERROR
>        formatter=simpleFormatter
>        args=()
>
>        # Rotating file handler
>        #   mkdir logs in the web2py base directory if not already present
>        #   args: (filename[, mode[, maxBytes[, backupCount[, encoding[, delay]]]]])
>        #
>        [handler_rotatingFileHandler]
>        class=handlers.RotatingFileHandler
>        level=DEBUG
>        formatter=simpleFormatter
>        args=("/var/log/web2py/web2py.log", "a", 1000000, 5)
>
>        [handler_osxSysLogHandler]
>        class=handlers.SysLogHandler
>        level=WARNING
>        formatter=simpleFormatter
>        args=("/var/run/syslog", handlers.SysLogHandler.LOG_DAEMON)
>
>        [handler_linuxSysLogHandler]
>        class=handlers.SysLogHandler
>        level=WARNING
>        formatter=simpleFormatter
>        args=("/dev/log", handlers.SysLogHandler.LOG_DAEMON)
>
>        [handler_remoteSysLogHandler]
>        class=handlers.SysLogHandler
>        level=WARNING
>        formatter=simpleFormatter
>        args=(('sysloghost.domain.com', handlers.SYSLOG_UDP_PORT), handlers.SysLogHandler.LOG_DAEMON)
>
>        [formatter_simpleFormatter]
>        format=%(asctime)s %(levelname)s %(funcName)s():%(lineno)d : %(message)s
>        datefmt=

This will create a rotating log file at `/var/log/web2py/web2py.log`.

NOTE that this is merely `[web2py]/examples/logging.example.conf` modified with a few additional attributes for the app. See the [Web2py logging](http://www.web2py.com/books/default/chapter/29/04/the-core#Logging) page for more info.

## References
- [Web2py guide](http://www.web2py.com/book)
- [Web2py logging](http://www.web2py.com/books/default/chapter/29/04/the-core#Logging)
- [Web2py API](http://www.web2py.com/init/static/epydoc/index.html)
- [Web2py Google Group](https://groups.google.com/forum/#!forum/web2py)