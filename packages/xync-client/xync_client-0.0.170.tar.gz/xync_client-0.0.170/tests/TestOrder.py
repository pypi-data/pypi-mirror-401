import pytest
from xync_client.Abc.Order import BaseOrderClient
from xync_schema.models import Agent, Ex

from xync_client.Abc.Agent import BaseAgentClient

from xync_client.Abc.BaseTest import BaseTest


class AgentTest(BaseTest):
    @pytest.fixture(scope="class")
    async def cl(self) -> BaseAgentClient:
        agent = await Agent.filter(auth__not_isnull=True, status__gt=0).prefetch_related("actor__ex").first()
        ex: Ex = agent.actor.ex
        acl: BaseAgentClient = agent.client(ex.client())
        yield acl
        await acl.close()

    @pytest.fixture(scope="class")
    async def cl1(self) -> BaseOrderClient:
        agent = (await self.exq).agents.filter(auth__not_isnull=True).offset(1).first()
        acl = BaseOrderClient(agent)
        yield acl
        await acl.close()
