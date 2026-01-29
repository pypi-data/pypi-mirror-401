from typing import Dict, Any
import requests

from .enums import MediaType
from .classes import *


class YuChatAPI:
    """
    https://docs.yuchat.ru/api-docs/intro
    """

    def __init__(
            self,
            token: str,
            base_url: str = "https://yuchat.ai",
    ):
        """
        Инициализация клиента YuChat

        :param token: Bearer токен для авторизации
        :param базовый URL API
        """

        self.__base_url = base_url.rstrip('/')
        self.__token = token
        self.__session = requests.Session()
        self.__session.headers.update({"Authorization": f"Bearer {token}", "Content-Type": "application/json"})

    def _request(
            self,
            method: str,
            endpoint: str,
            **kwargs,
    ) -> Dict:
        """
        Базовый метод для выполнения запросов

        :param method: method (GET, POST)
        :param endpoint: endpoint метода
        :param kwargs: kwargs
        :return: ответ
        """

        r = self.__session.request(
            method=method,
            url=f"{self.__base_url}{endpoint}",
            **kwargs,
        )

        if r.status_code == 429:
            raise Exception(f"Rate limit exceeded: {r.text}")
        elif r.status_code == 403:
            raise Exception(f"Authentication error: {r.text}")
        elif r.status_code == 404:
            return {}

        r.raise_for_status()

        if r.status_code == 204 or len(r.content) == 0:
            return {}

        return r.json()

    def send_message(
            self,
            workspace_id: str,
            chat_id: str,
            markdown: str,
            file_ids: Optional[List[str]] = None,
            reply_to: Optional[str] = None,
    ) -> SendChatMessageResponse:
        """
        Отправка сообщения

        :param workspace_id: id workspace
        :param chat_id: id чата
        :param markdown: текст сообщения в Markdown
        :param file_ids: id файлов, прикрепленных к сообщению
        :param reply_to: id сообщения для ответа
        :return: SendChatMessageResponse
        """

        payload: dict = {
            "workspaceId": workspace_id, "chatId": chat_id, "markdown": markdown,
            **({"fileIds": file_ids} if file_ids else {}),
            **({"replyTo": reply_to} if reply_to else {}),

        }

        return SendChatMessageResponse.model_validate(
            self._request(
                method="POST",
                endpoint="/public/v1/chat.message.send",
                json=payload,
            ),
        )

    def edit_message(
            self,
            workspace_id: str,
            chat_id: str,
            chat_message_id: str,
            new_markdown: str,
    ) -> EditChatMessageResponse:
        """
        Редактирование сообщения

        :param workspace_id: id workspace
        :param chat_id: id чата
        :param chat_message_id: id сообщения для редактирования
        :param new_markdown: новый текст сообщения
        :return: EditChatMessageResponse
        """

        payload = {
            "workspaceId": workspace_id, "chatId": chat_id,
            "chatMessageId": chat_message_id, "newMarkdown": new_markdown,
        }

        return EditChatMessageResponse.model_validate(
            self._request(
                method="POST",
                endpoint="/public/v1/chat.message.edit",
                json=payload,
            ),
        )

    def delete_message(
            self,
            workspace_id: str,
            chat_id: str,
            chat_message_id: str,
    ) -> DeleteChatMessageResponse:
        """
        Удаление сообщения

        :param workspace_id: id workspace
        :param chat_id: id чата
        :param chat_message_id: id сообщения для удаления
        :return: DeleteChatMessageResponse
        """

        payload = {
            "workspaceId": workspace_id, "chatId": chat_id, "chatMessageId": chat_message_id,
        }

        return DeleteChatMessageResponse.model_validate(
            self._request(
                method="POST",
                endpoint="/public/v1/chat.message.delete",
                json=payload,
            ),
        )

    def forward_message(
            self,
            workspace_id: str,
            source_chat_id: str,
            source_chat_message_id: str,
            target_chat_id: str,
            markdown: str,
    ) -> ForwardChatMessageResponse:
        """
        Пересылка сообщения

        :param workspace_id: id workspace
        :param source_chat_id: id исходного чата
        :param source_chat_message_id: id сообщения для пересылки
        :param target_chat_id: id целевого чата
        :param markdown: текст к пересылаемому сообщению
        :return: ForwardChatMessageResponse
        """

        payload = {
            "workspaceId": workspace_id, "sourceChatId": source_chat_id,
            "sourceChatMessageId": source_chat_message_id, "targetChatId": target_chat_id,
            "markdown": markdown,
        }

        return ForwardChatMessageResponse.model_validate(
            self._request(
                method="POST",
                endpoint="/public/v1/chat.message.forward",
                json=payload,
            ),
        )

    def create_workspace_chat(
            self,
            workspace_id: str,
            participants: Optional[List[str]] = None,
            name: Optional[str] = None,
            chat_type: Optional[WorkspaceChatType] = None,
            announce_channel: Optional[bool] = None,
            description: Optional[str] = None,
    ) -> CreateWorkspaceChatResponse:
        """
        Создание публичного/приватного чата внутри workspace

        :param workspace_id: id workspace
        :param participants: список MembershipId участников чата
        :param name: название чата
        :param chat_type: тип чата
        :param announce_channel: False - могут писать все, True - только админы
        :param description: описание чата
        :return: CreateWorkspaceChatResponse
        """

        payload: dict = {
            "workspaceId": workspace_id,
            **({"participants": participants} if participants else {}),
            **({"name": name} if name else {}),
            **({"type": chat_type.value} if chat_type else {}),
            **({"announceChannel": announce_channel} if announce_channel else {}),
            **({"description": description} if description else {}),
        }

        return CreateWorkspaceChatResponse.model_validate(
            self._request(
                method="POST",
                endpoint="/public/v1/chat.workspace.create",
                json=payload,
            ),
        )

    def create_personal_chat(
            self,
            workspace_id: str,
            participant: str,
    ) -> CreatePersonalChatResponse:
        """
        Создание персонального чата (личные сообщения)

        :param workspace_id: id workspace
        :param participant: MembershipId участника чата
        :return: CreatePersonalChatResponse
        """

        payload = {
            "workspaceId": workspace_id, "participant": participant,
        }

        return CreatePersonalChatResponse.model_validate(
            self._request(
                method="POST",
                endpoint="/public/v1/chat.personal.create",
                json=payload,
            ),
        )

    def create_thread_chat(
            self,
            workspace_id: str,
            chat_id: str,
            parent_message_id: str,
    ) -> CreateThreadChatResponse:
        """
        Создание обсуждения внутри чата

        :param workspace_id: id workspace
        :param chat_id: id чата
        :param parent_message_id: id сообщения, внутри которого создается обсуждение
        :return: CreateThreadChatResponse
        """

        payload = {
            "workspaceId": workspace_id, "chatId": chat_id, "parentMessageId": parent_message_id,
        }

        return CreateThreadChatResponse.model_validate(
            self._request(
                method="POST",
                endpoint="/public/v1/chat.thread.create",
                json=payload,
            ),
        )

    def list_workspace_chats(
            self,
            workspace_id: str,
            chat_ids: Optional[List[str]] = None,
            max_count: int = 100,
    ) -> ListWorkspaceChatsResponse:
        """
        Получение списка чатов внутри workspace

        :param workspace_id: id workspace
        :param chat_ids: id чатов, информацию о которых нужно получить
        :param max_count: максимальное количество чатов
        :return: ListWorkspaceChatsResponse
        """

        payload: dict[str, Any] = {
            "workspaceId": workspace_id, "maxCount": max_count,
            **({"chatIds": chat_ids} if chat_ids else {}),
        }

        return ListWorkspaceChatsResponse.model_validate(
            self._request(
                method="POST",
                endpoint="/public/v1/chat.workspace.list",
                json=payload,
            ),
        )

    def invite_to_chat(
            self,
            workspace_id: str,
            chat_id: str,
            member_ids: List[str],
    ) -> InviteToChatResponse:
        """
        Приглашение участников в чат

        :param workspace_id: id workspace
        :param chat_id: id чата
        :param member_ids: id участников, которых нужно пригласить
        :return: InviteToChatResponse
        """

        payload = {
            "workspaceId": workspace_id, "chatId": chat_id, "memberId": member_ids,
        }

        return InviteToChatResponse.model_validate(
            self._request(
                method="POST",
                endpoint="/public/v1/chat.invite",
                json=payload,
            ),
        )

    def kick_from_chat(
            self,
            workspace_id: str,
            chat_id: str,
            member_ids: List[str],
    ) -> KickFromChatResponse:
        """
        Удаление участника из чата

        :param workspace_id: id workspace
        :param chat_id: id чата
        :param member_ids: id участников, которых нужно удалить
        :return: KickFromChatResponse
        """

        payload = {
            "workspaceId": workspace_id, "chatId": chat_id, "memberId": member_ids,
        }

        return KickFromChatResponse.model_validate(
            self._request(
                method="POST",
                endpoint="/public/v1/chat.kick",
                json=payload,
            ),
        )

    def list_members(
            self,
            workspace_id: str,
    ) -> ListMembersResponse:
        """
        Получение списка участников workspace

        :param workspace_id: id workspace
        :return: ListMembersResponse
        """

        return ListMembersResponse.model_validate(
            self._request(
                method="POST",
                endpoint="/public/v1/member.list",
                json={"workspaceId": workspace_id},
            ),
        )

    def get_presigned_url(
            self,
            workspace_id: str,
            file_name: str,
            media_type: MediaType,
            access_chat_id: Optional[str] = None,
    ) -> PreSignedUrlResponse:
        """
        Получение ссылки для загрузки файла на сервер

        :param workspace_id: id workspace
        :param file_name: имя файла
        :param media_type: тип файла
        :param access_chat_id: id чата, в котором будет доступ к файлу
        :return: GetPreSignedUrlResponse
        """

        payload = {
            "workspaceId": workspace_id, "fileName": file_name, "mediaType": media_type.value,
            **({"accessChatId": access_chat_id} if access_chat_id else {}),
        }

        return PreSignedUrlResponse.model_validate(
            self._request(
                method="POST",
                endpoint="/public/v1/file.getPreSignedUrl",
                json=payload,
            )
        )

    def get_download_url(
            self,
            file_id: str,
    ) -> DownloadUrlResponse:
        """
        Получение ссылки для скачивания файла

        :param file_id: id файла
        :return: DownloadUrlResponse
        """

        return DownloadUrlResponse.model_validate(
            self._request(
                method="POST",
                endpoint="/public/v1/file.getDownloadUrl",
                json={"fileId": file_id},
            )
        )

    def get_updates(
            self,
            offset: Optional[int] = None,
            limit: int = 100,
    ) -> UpdatesResponse:
        """
        Получение всех событий, адресованных боту

        :param offset: id последнего обработанного события
        :param limit: максимальное количество событий
        :return: UpdatesResponse
        """

        return UpdatesResponse.model_validate(
            {
                "updates": self._request(
                    method="GET",
                    endpoint="/public/v1/bot.getUpdates",
                    params={"limit": limit, **({"offset": offset} if offset else {})},
                ),
            }
        )

    def set_webhook(
            self,
            url: str,
            certificate: Optional[str] = None,
            update_types: Optional[List[UpdateType]] = None,
            secret_token: Optional[str] = None,
    ) -> None:
        """
        Установка Webhook

        :param url: webhook url
        :param certificate: содержимое .pem сертификата в Base64
        :param update_types: типы обновлений для получения
        :param secret_token: токен для проверки в заголовке X-YuChat-Bot-Api-Secret-Token
        :return: None
        """

        payload = {
            "url": url,
            **({"certificate": certificate} if certificate else {}),
            **({"updateTypes": [ut.value for ut in update_types]} if update_types else {}),
            **({"secretToken": secret_token} if secret_token else {}),
        }

        self._request(method="POST", endpoint="/public/v1/bot.setWebhook", json=payload)

    def delete_webhook(
            self,
    ) -> None:
        """
        Удаление Webhook

        :return: None
        """

        self._request(method="DELETE", endpoint="/public/v1/bot.deleteWebhook")

    def get_webhook_info(
            self,
    ) -> WebhookInfoResponse:
        """
        Получение информации о Webhook

        :return: WebhookInfoResponse
        """

        return WebhookInfoResponse.model_validate(
            self._request(
                method="GET",
                endpoint="/public/v1/bot.getWebhookInfo",
            ),
        )

    def find_email_by_user_id(
            self,
            user_id: str,
            workspace_id: str,
    ) -> str:
        """
        Поиск email по id участника

        :param user_id: id участника, email которого нужно найти
        :param workspace_id: id workspace
        :return: email
        """

        for member in self.list_members(workspace_id=workspace_id).members:
            try:
                member_id = member.profile.profile_id
            except AttributeError:
                continue
            if user_id == member_id:
                return member.profile.primary_email

        raise RuntimeError(f"Member with {user_id} not found.")
