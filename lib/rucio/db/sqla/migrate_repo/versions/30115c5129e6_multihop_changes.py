# Copyright 2013-2019 CERN for the benefit of the ATLAS collaboration.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Authors:
# - Cedric Serfon <cedric.serfon@cern.ch>, 2019

''' Multihop changes '''

import sqlalchemy as sa

from alembic import context
from alembic.op import add_column, alter_column, drop_column

from rucio.db.sqla.types import GUID


# Alembic revision identifiers
revision = '30115c5129e6'
down_revision = '2cbee484dcf9'


def upgrade():
    '''
    Upgrade the database to this revision
    '''

    if context.get_context().dialect.name in ['oracle', 'mysql', 'postgresql']:
        schema = context.get_context().version_table_schema if context.get_context().version_table_schema else ''
        alter_column('rse_protocols', 'third_party_copy', nullable=True, new_column_name='third_party_copy_read', schema=schema)
        add_column('rse_protocols', sa.Column('third_party_copy_write', sa.Integer), server_default='0', schema=schema)
        add_column('requests', sa.Column('parent_request_id', GUID()), server_default='0', schema=schema)
        add_column('requests_history', sa.Column('parent_request_id', GUID()), schema=schema)
        add_column('requests', sa.Column('child_request_id', GUID()), server_default='0', schema=schema)
        add_column('requests_history', sa.Column('child_request_id', GUID()), schema=schema)


def downgrade():
    '''
    Downgrade the database to the previous revision
    '''

    if context.get_context().dialect.name in ['oracle', 'mysql', 'postgresql']:
        schema = context.get_context().version_table_schema if context.get_context().version_table_schema else ''
        alter_column('rse_protocols', 'third_party_copy_read', nullable=True, new_column_name='third_party_copy', schema=schema)
        drop_column('rse_protocols', 'third_party_copy_write', schema=schema)
        drop_column('requests', 'parent_request_id', schema=schema)
        drop_column('requests_history', 'parent_request_id', schema=schema)
        drop_column('requests', 'child_request_id', schema=schema)
        drop_column('requests_history', 'child_request_id', schema=schema)
