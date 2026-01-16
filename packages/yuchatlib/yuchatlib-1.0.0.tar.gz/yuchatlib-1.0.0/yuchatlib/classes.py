from pydantic import BaseModel, Field
from typing import Optional, List
import datetime

from .enums import (
    AccountLocation,
    AccountType,
    MemberRoleType,
    MemberStatus,
    WorkspaceChatType,
    ChatMemberRoleType,
    ChatPermission,
    UpdateType,
)


class BaseData(BaseModel):
    """Наследуемый класс"""

    workspace_id: str = Field(alias="workspaceId")
    chat_id: str = Field(alias="chatId")


class WorkspaceChat(BaseData):
    """Информация о чате"""

    membership_ids: List[str] = Field(alias="membershipIds")
    name: str
    type: WorkspaceChatType
    announce_channel: bool = Field(alias="announceChannel")
    role: Optional[ChatMemberRoleType] = None
    permissions: Optional[List[ChatPermission]] = None
    description: Optional[str] = None


class WorkspaceChatMembership(BaseModel):
    """Модель API: Членство в чате"""

    chat: WorkspaceChat
    role: ChatMemberRoleType
    permissions: List[ChatPermission]


class SendChatMessageResponse(BaseModel):
    """Модель API: отправка сообщения"""

    message_id: str = Field(alias="messageId")


class EditChatMessageResponse(BaseModel):
    """Модель API: редактирование сообщения"""

    updated_at: datetime.datetime = Field(alias="updatedAt")


class DeleteChatMessageResponse(BaseModel):
    """Модель API: удаление сообщения"""

    updated_at: datetime.datetime = Field(alias="updatedAt")


class ForwardChatMessageResponse(BaseModel):
    """Модель API: пересылка сообщения"""

    message_id: str = Field(alias="messageId")


class CreateWorkspaceChatResponse(BaseModel):
    """Модель API: создание чата в Workspace"""

    chat_id: str = Field(alias="chatId")


class CreatePersonalChatResponse(BaseModel):
    """Модель API: создание личного чата"""

    chat_id: str = Field(alias="chatId")


class CreateThreadChatResponse(BaseModel):
    """Модель API: создание обсуждения в чате"""

    chat_id: str = Field(alias="chatId")


class ListWorkspaceChatsResponse(BaseModel):
    """Модель API: получение списка чатов в Workspace"""

    chats: List[WorkspaceChat]


class InviteToChatResponse(BaseModel):
    """Модель API: приглашение участника"""

    chat: WorkspaceChat


class KickFromChatResponse(BaseModel):
    """Модель API: удаление участника"""

    chat: WorkspaceChat


class AccountDetails(BaseModel):
    """Информация об аккаунте участника"""

    position: Optional[str] = None
    department: Optional[str] = None
    phone_number: Optional[str] = Field(alias="phonenumber")
    location: Optional[AccountLocation] = None


class Profile(BaseModel):
    """Профиль участника"""

    profile_id: str = Field(alias="profileId")
    primary_email: str = Field(alias="primaryEmail")
    full_name: str = Field(alias="fullName")
    type: AccountType
    details: Optional[AccountDetails] = None


class Presence(BaseModel):
    """Присутствие участника"""

    is_online: bool = Field(alias="isOnline")
    is_on_call: bool = Field(alias="isOnCall")
    last_seen_at: datetime.datetime = Field(alias="lastSeenAt")


class Member(BaseModel):
    """Участник"""

    member_id: str = Field(alias="memberId")
    profile: Profile
    role_type: MemberRoleType = Field(alias="roleType")
    presence: Optional[Presence] = None
    status: Optional[MemberStatus] = None


class ListMembersResponse(BaseModel):
    """Модель API: получение списка участников"""

    members: List[Member]


class PreSignedUrlResponse(BaseModel):
    """Модель данных API: получение ссылки для загрузки файла на сервер"""

    url: str
    file_id: str = Field(alias="fileId")


class DownloadUrlResponse(BaseModel):
    """Модель данных API: получение ссылки на скачивание"""

    url: str


class NewChatMessage(BaseData):
    """Обновление: новое сообщение"""

    message_id: str = Field(alias="messageId")
    author: str
    markdown: str
    created_at: datetime.datetime = Field(alias="createdAt")
    parent_message_id: Optional[str] = Field(alias="parentMessageId")
    parent_message_author: Optional[str] = Field(alias="parentMessageAuthor")
    file_ids: Optional[List[str]] = Field(alias="fileIds")


class InviteToChat(BaseData):
    """Обновление: участника пригласили в чат"""

    inviter: str


class JoinedToChat(BaseData):
    """Обновление: участник зашел в чат"""

    joined: List[str]
    inviter: Optional[str] = None


class LeftFromChat(BaseData):
    """Обновление: участник вышел из чата"""

    left: List[str]
    kicker: Optional[str] = None


class Update(BaseModel):
    """Обновление"""

    update_id: int = Field(alias="updateId")
    new_chat_message: Optional[NewChatMessage] = Field(alias="newChatMessage")
    invite_to_chat: Optional[InviteToChat] = Field(alias="inviteToChat")
    joined_to_chat: Optional[JoinedToChat] = Field(alias="joinedToChat")
    left_from_chat: Optional[LeftFromChat] = Field(alias="leftFromChat")


class UpdatesResponse(BaseModel):
    """Модель данных API: получение обновлений"""

    updates: Optional[List[Update]] = None


class WebhookInfo(BaseModel):
    """Информация о Webhook"""

    url: str
    has_custom_certificate: bool = Field(alias="hasCustomCertificate")
    pending_update_count: Optional[int] = Field(alias="pendingUpdateCount")
    last_error_date: Optional[datetime.datetime] = Field(alias="lastErrorDate")
    last_error_message: Optional[str] = Field(alias="lastErrorMessage")
    update_types: Optional[List[UpdateType]] = Field(alias="updateTypes")


class WebhookInfoResponse(BaseModel):
    """Модель данных API: запрос информации о Webhook"""

    webhook_info: WebhookInfo = Field(alias="webhookInfo")
