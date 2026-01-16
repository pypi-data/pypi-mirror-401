from asyncio import sleep

from bybit_p2p._exceptions import FailedRequestError
from xync_client.Bybit.agent import AgentClient

from xync_client.Abc.Order import BaseOrderClient


class OrderClient(BaseOrderClient):
    agent_client: AgentClient

    # 5: Перевод сделки в состояние "оплачено", c отправкой чека
    async def _mark_payed(self, credex_exid: int = None, pmex_exid: int | str = None, receipt: bytes = None):
        params = dict(orderId=str(self.order.exid), paymentType=str(pmex_exid), paymentId=str(credex_exid))
        try:
            self.agent_client.api.mark_as_paid(**params)
        except FailedRequestError as e:
            if e.status_code == 912100202:  # Server error, please try again later
                await sleep(5, self.agent_client.api.mark_as_paid(**params))
            else:
                raise e

    # 7: Подтвердить получение оплаты
    async def confirm(self):
        try:
            self.agent_client.api.release_assets(orderId=str(self.order.exid))
        except FailedRequestError as e:
            if e.status_code == 912100202:  # Server error, please try again later
                await sleep(5, self.agent_client.api.release_assets(orderId=str(self.order.exid)))
            else:
                raise e

    # 6: Отмена одобренной сделки
    async def cancel(self) -> bool: ...

    # 6: Запрос отмены (оплаченная контрагентом продажа)
    async def cancel_request(self) -> bool: ...

    # 6: Одобрение запроса на отмену (оплаченная мной покупка)
    async def cancel_accept(self):
        data = {"orderId": self.order.exid, "examineResult": "PASS"}
        await self.agent_client._post("/x-api/fiat/otc/order/buyer/examine/sellerCancelOrderApply", data)

    # 9, 10: Подать аппеляцию cо скриншотом/видео/файлом
    async def start_appeal(self, file) -> bool: ...

    # 11, 12: Встречное оспаривание полученной аппеляции cо скриншотом/видео/файлом
    async def dispute_appeal(self, file) -> bool: ...

    # 15: Отмена аппеляции
    async def cancel_appeal(self) -> bool: ...

    # 16: Отправка сообщения юзеру в чат по ордеру с приложенным файлом
    async def send_order_msg(self, msg: str, file=None) -> bool: ...

    # 17: Отправка сообщения по апелляции
    async def send_appeal_msg(self, file, msg: str = None) -> bool: ...

    # Загрузка файла
    async def _upload_file(self, order_id: int, path_to_file: str): ...
