from enum import Enum


class WorkspaceChatType(str, Enum):
    PRIVATE = "PRIVATE"
    PUBLIC = "PUBLIC"
    GENERAL = "GENERAL"
    BREAKOUT = "BREAKOUT"


class ChatMemberRoleType(str, Enum):
    CHAT_MEMBER = "CHAT_MEMBER"
    CHAT_ADMIN = "CHAT_ADMIN"
    CHAT_OWNER = "CHAT_OWNER"


class ChatPermission(str, Enum):
    CHANGE_ROLE = "CHANGE_ROLE"
    ARCHIVE_CHAT = "ARCHIVE_CHAT"
    RENAME_CHAT = "RENAME_CHAT"
    UPDATE_CONFIG = "UPDATE_CONFIG"
    KICK_FROM_CHAT = "KICK_FROM_CHAT"
    SEND_MESSAGES_TO_ANNOUNCE_CHANNEL = "SEND_MESSAGES_TO_ANNOUNCE_CHANNEL"
    PIN_CHAT_MESSAGE = "PIN_CHAT_MESSAGE"
    SCHEDULE_CONFERENCE = "SCHEDULE_CONFERENCE"


class MemberRoleType(str, Enum):
    MEMBER = "MEMBER"
    ADMIN = "ADMIN"
    OWNER = "OWNER"
    GUEST = "GUEST"
    GUEST_CALLER = "GUEST_CALLER"


class MemberStatus(str, Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"


class AccountType(str, Enum):
    REGULAR = "REGULAR"
    BOT = "BOT"
    VOICE_BOT = "VOICE_BOT"
    INTEGRATION_BOT = "INTEGRATION_BOT"
    GUEST_ACCOUNT = "GUEST_ACCOUNT"


class AccountLocation(str, Enum):
    LOCATION_NOT_SET = "LOCATION_NOT_SET"
    OFFICE = "OFFICE"
    HOME = "HOME"
    VACATION = "VACATION"


class UpdateType(str, Enum):
    MESSAGE = "MESSAGE"
    CHAT_MEMBER = "CHAT_MEMBER"


class MediaType(str, Enum):
    RAW = "RAW"
    IMAGE = "IMAGE"
    AUDIO = "AUDIO"
    VIDEO = "VIDEO"
    PDF = "PDF"
    DOC = "DOC"
    XLS = "XLS"
    PPT = "PPT"
