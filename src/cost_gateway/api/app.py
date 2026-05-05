from typing import Any, Dict, List

from decimal import Decimal

from fastapi import Depends, FastAPI
from fastapi.openapi.utils import get_openapi
from uvicorn import Config, Server

from cost_gateway.api.model import CostModel
from cost_gateway.cost.service import CostService


class CostGatewayAPI(FastAPI):
    def openapi(self) -> Dict[str, Any]:
        if self.openapi_schema:
            return self.openapi_schema
        openapi_schema = get_openapi(
            title="Cost Gateway",
            version="0.0.0",
            description="Collects all types of costs and exposes them via prometheus",
            contact={
                "name": "HIRO-MicroDataCenters",
                "email": "all-hiro@hiro-microdatacenters.nl",
            },
            license_info={
                "name": "MIT",
                "url": "https://github.com/HIRO-MicroDataCenters-BV" "/cost-gateway/blob/main/LICENSE",
            },
            routes=self.routes,
        )
        self.openapi_schema = openapi_schema
        return self.openapi_schema


async def start_fastapi(port: int, cost_service: CostService) -> None:
    app = create_app(cost_service)
    config = Config(app=app, host="0.0.0.0", port=port, loop="asyncio")
    server = Server(config)

    # Start the server without blocking the current event loop
    await server.serve()


def create_app(cost_service: CostService) -> CostGatewayAPI:
    app = create_api()

    app.state.cost_service = cost_service

    return app


def create_api() -> CostGatewayAPI:
    app = CostGatewayAPI()

    @app.get(path="/", operation_id="status", description="Get Application Status")
    async def root():
        return {"application": "CostGateway", "status": "OK"}

    @app.get(path="/costs/", response_model=List[CostModel], operation_id="list_costs")
    async def list_costs(cost_service: CostService = Depends(lambda: get_cost_service(app))) -> List[CostModel]:
        list_of_costs = await cost_service.list()
        return [CostModel.from_object(cost) for cost in list_of_costs]

    @app.put("/costs/{name}/customize/{value}", response_model=List[CostModel], operation_id="set_custom_cost")
    async def set_custom_cost(
        name: str, value: Decimal, cost_service: CostService = Depends(lambda: get_cost_service(app))
    ) -> List[CostModel]:
        cost_service.set_custom_cost(name, value)
        list_of_costs = await cost_service.list()
        return [CostModel.from_object(cost) for cost in list_of_costs]

    @app.put("/costs/{name}/uncustomize", response_model=List[CostModel], operation_id="remove_custom_cost")
    async def remove_custom_cost(
        name: str, cost_service: CostService = Depends(lambda: get_cost_service(app))
    ) -> List[CostModel]:
        await cost_service.remove_custom_cost(name)
        list_of_costs = await cost_service.list()
        return [CostModel.from_object(cost) for cost in list_of_costs]

    return app


app = create_api()


def get_cost_service(app: FastAPI) -> CostService:
    return app.state.cost_service  # type: ignore
