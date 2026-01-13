from xync_client.Abc.Order import BaseOrderClient


class OrderClient(BaseOrderClient):
    # 5: Перевод сделки в состояние "оплачено", c отправкой чека
    async def _mark_payed(self, credex_exid: int = None, pmex_exid: int | str = None, receipt: bytes = None):
        self.agent_client.api.mark_as_paid(
            orderId=str(self.order.exid), paymentType=str(pmex_exid), paymentId=str(credex_exid)
        )

    # 6: Отмена одобренной сделки
    async def cancel_order(self) -> bool: ...

    # 7: Подтвердить получение оплаты
    async def confirm(self):
        self.agent_client.api.release_assets(orderId=str(self.order.exid))

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
