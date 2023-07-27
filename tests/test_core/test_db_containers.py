import psycopg2
import pytest

from testcontainers.core import generic
from testcontainers.core.utils import is_arm
from testcontainers.db.mssql import SqlServerContainer
from testcontainers.db.mysql import MySqlContainer
from testcontainers.db.oracle import OracleDbContainer
from testcontainers.db.postgres import PostgresContainer


# @pytest.mark.skipif(is_arm(), reason='mysql container not available for ARM')
# def test_docker_run_mysql():
#     config = MySqlContainer('mysql:5.7.17')
#     with config as mysql:
#         e = sqlalchemy.create_engine(mysql.get_connection_url())
#         result = e.execute("select version()")
#         for row in result:
#             assert row[0].startswith('5.7.17')


def test_docker_run_postgres():
    postgres_container = PostgresContainer("postgres:14.8")
    with postgres_container as postgres:
        postgres.check_connection()
        conn = psycopg2.connect(
            # dbname=self.POSTGRES_DB,
            database=postgres.POSTGRES_DB,
            user=postgres.POSTGRES_USER,
            password=postgres.POSTGRES_PASSWORD,
            host=postgres.get_container_host_ip(),
            port=postgres.get_exposed_port(5432),
        )
        cursor = conn.cursor()
        cursor.execute("select version()")
        result = cursor.fetchone()
        print(len(result))
        print(result)
        print(result[0])
        # for row in result:
        #     assert row[0].lower().startswith("postgresql 14.8")


# def test_docker_run_postgres_with_driver_pg8000():
#     postgres_container = PostgresContainer("postgres:9.5", driver="pg8000")
#     with postgres_container as postgres:
#         e = sqlalchemy.create_engine(postgres.get_connection_url())
#         e.execute("select 1=1")
#
#
# def test_docker_run_mariadb():
#     with MySqlContainer("mariadb:10.6.5").maybe_emulate_amd64() as mariadb:
#         e = sqlalchemy.create_engine(mariadb.get_connection_url())
#         result = e.execute("select version()")
#         for row in result:
#             assert row[0].startswith('10.6.5')
#
#
# @pytest.mark.skip(reason="needs oracle client libraries unavailable on Travis")
# def test_docker_run_oracle():
#     with OracleDbContainer() as oracledb:
#         e = sqlalchemy.create_engine(oracledb.get_connection_url())
#         result = e.execute("select * from V$VERSION")
#         versions = {'Oracle Database 11g Express Edition Release 11.2.0.2.0 - 64bit Production',
#                     'PL/SQL Release 11.2.0.2.0 - Production',
#                     'CORE\t11.2.0.2.0\tProduction',
#                     'TNS for Linux: Version 11.2.0.2.0 - Production',
#                     'NLSRTL Version 11.2.0.2.0 - Production'}
#         assert {row[0] for row in result} == versions
#
#
# def test_docker_run_mssql():
#     image = 'mcr.microsoft.com/azure-sql-edge'
#     dialect = 'mssql+pymssql'
#     with SqlServerContainer(image, dialect=dialect) as mssql:
#         e = sqlalchemy.create_engine(mssql.get_connection_url())
#         result = e.execute('select @@servicename')
#         for row in result:
#             assert row[0] == 'MSSQLSERVER'
#
#     with SqlServerContainer(image, password="1Secure*Password2", dialect=dialect) as mssql:
#         e = sqlalchemy.create_engine(mssql.get_connection_url())
#         result = e.execute('select @@servicename')
#         for row in result:
#             assert row[0] == 'MSSQLSERVER'
