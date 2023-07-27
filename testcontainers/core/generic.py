#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from abc import *

from deprecation import deprecated

from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_container_is_ready

ADDITIONAL_TRANSIENT_ERRORS = []
try:
    import sqlalchemy.exc
    ADDITIONAL_TRANSIENT_ERRORS.append(sqlalchemy.exc.DBAPIError)
except ImportError:
    pass
try:
    import psycopg2
    ADDITIONAL_TRANSIENT_ERRORS.append(psycopg2.OperationalError)
    # ADDITIONAL_TRANSIENT_ERRORS.append(psycopg2.ProgrammingError)
except ImportError:
    pass
try:
    import pymysql
    ADDITIONAL_TRANSIENT_ERRORS.append(pymysql.OperationalError)
except ImportError:
    pass


class DbContainer(DockerContainer, metaclass=ABCMeta):

    def __init__(self, image, *errors, **kwargs):
        super(DbContainer, self).__init__(image, **kwargs)

    @wait_container_is_ready(*ADDITIONAL_TRANSIENT_ERRORS)
    def _connect(self):
        print('_connect')
        self.check_connection()

    @abstractmethod
    def check_connection(self):
        raise NotImplementedError

    @abstractmethod
    def get_connection_url(self):
        raise NotImplementedError

    def _create_connection_url(self, dialect, username, password,
                               host=None, port=None, db_name=None):
        if self._container is None:
            raise RuntimeError("container has not been started")
        if not host:
            host = self.get_container_host_ip()
        port = self.get_exposed_port(port)
        url = "{dialect}://{username}:{password}@{host}:{port}".format(
            dialect=dialect, username=username, password=password, host=host, port=port
        )
        if db_name:
            url += '/' + db_name
        return url

    def start(self):
        self._configure()
        super().start()
        self._connect()
        return self

    @abstractmethod
    def _configure(self):
        raise NotImplementedError


class GenericContainer(DockerContainer):
    @deprecated(details="Use `DockerContainer`.")
    def __init__(self, image):
        super(GenericContainer, self).__init__(image)
