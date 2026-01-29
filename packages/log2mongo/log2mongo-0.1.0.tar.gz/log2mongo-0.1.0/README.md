# log2mongo
It is a lightweight Package for store logs in MongoDB

Requirements
------------
* Python 3.12+
* Pymongo 4.0+

Installing
----------
```bash
pip install log2mongo
```

How to use it
-------------

* Create an instance directly
 - Full example: https://github.com/ablogo/WebSocketServer/blob/main/main.py

 ```bash
 #import
 from log2mongo import log2mongo

 #initialize
 log = log2mongo('connection_string_to_mongoDB', 'ws-server-logs', level = 'DEBUG')

 #use it
 log.logger.debug('server starting')
 ```

* Using with dependency injection
  - Full exampe: https://github.com/ablogo/AuthFastApi/blob/main/src/dependency_injection/containers.py

  https://github.com/ablogo/AuthFastApi/blob/main/src/services/login_service.py

 containers.py
 ```bash
 #import
 from dependency_injector import containers, providers
 from log2mongo import log2mongo

 #initialize
 logging = providers.Singleton(
    log2mongo,
    'connection_string_to_mongoDB',
    'ws-server-logs',
    level = 'DEBUG',
    )

 #use it
 log.logger.debug('server starting')
 ```
 main.py
 ```bash
 #import
 from dependency_injector.wiring import Provide, inject
 from log2mongo import log2mongo

 #invoke dependency
 log_service: log2mongo = Provide[Container.logging]

 #use it
 @inject
 def main(log = log_service):
     try:
         log.logger.debug('server starting')
     except Exception as e:
         log.logger.error(e)
 ```

 Constructor parameters
 ----------------------
 * db_url: connection string to the database
 * db_name: database name
 * db_collection[optional]: collection name
   If this parameter is not provided, the lof level will be used as the collection name; that is, a collection called 'debug' will be created fo all messages of that level, another called 'error' for messages of that level, and so on
 * file_name[optional]: the file name where it will be invoke
 * clean_providers[optional]:All logs providers are cleared, if the value is TRUE. Default value = TRUE
 * level[optional]: log level. Default value = Error/40
