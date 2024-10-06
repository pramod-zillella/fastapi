from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from app.models import Base
from app.config import settings
from urllib.parse import quote_plus

password = quote_plus(settings.database_password)
# config.set_main_option("sqlalchemy.url", f'postgresql+psycopg2://{settings.database_username}:{password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}')


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
# config.set_main_option("sqlalchemy.url", f'postgresql+psycopg2://{settings.database_username}:{password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}')

# Assign URL directly
url = f'postgresql+psycopg2://{settings.database_username}:{password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        {'sqlalchemy.url': url},  # Directly pass the URL here
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
