import msgspec
from typing import Any, ClassVar
from datetime import datetime
import enum

"""
Please refer to the discord documentation at: https://discord.com/developers/docs/intro, for more details on the classes.
The documentation in this package aims to be minimal due to the high probability of changing discord documentation on the official site.
However, documentation will be provided to clarify possible instances of misunderstanding when using this package where neccesary.
The msgspec classes in this package are used for the purposes of:
- type validation of JSON data, for example when received from the discord websocket connection or HTTP API endpoints.
- value validation of instantiated msgspec representation classes, conditional on the fields of the classes and
implementing the conditional relations defined in the official documentation for the msgspec classes.
For example,
In the webhook endpoints, the prescence of the files JSON param field indicates that the attachment field should be non-null.
- a serializable interface format for another common data format(e.g msgpack)

IMPORTANT NOTICES:
- The Activity msgspec class is excluded from this module, this package intends to model discord HTTP endpoint data structures only and not the gateway websocket structures. 
If you do decide to use the SetActivityArgument class in the RPC discord section, consider writing your own Activity class. 
- Moreover, this package is subject to changes in the foreseeable future, all updates will be viewable from the official github repository.

In the RPC section of this module, the SetActivityArgument class uses the missing Activity msgspec class:
class SetActivityArgument(msgspec.Struct, kw_only=True):
    pid: int  # application's process id
    activity: 'Activity'  # rich presence to assign to the user (limited to Playing, Listening, Watching, or Competing).

"""
#Auxillary classes for msgspec classes
class HttpMethods(enum.StrEnum):
    GET = "GET"
    POST = "POST"
    PATCH = "PATCH"
    DELETE = "DELETE"

#API Reference-
class Locales(enum.StrEnum):
    INDONESIAN = "id"
    DANISH = "da"
    GERMAN = "de"
    ENGLISH_UK = "en-GB"
    ENGLISH_US = "en-US"
    SPANISH = "es-ES"
    SPANISH_LATAM = "es-419"
    FRENCH = "fr"
    CROATIAN = "hr"
    ITALIAN = "it"
    LITHUANIAN = "lt"
    HUNGARIAN = "hu"
    DUTCH = "nl"
    NORWEGIAN = "no"
    POLISH = "pl"
    PORTUGEUSE_BRAZILIAN = "pt-BR"
    ROMANIAN_ROMANIA = "ro"
    FINNISH = "fi"
    SWEDISH = "sv-SE"
    VIETNAMESE = "vi"
    TURKISH = "tr"
    CZECH = "cs"
    GREEK = "el"
    BULGARIAN = "bg"
    RUSSIAN = "ru"
    UKRANIAN = "uk"
    HINDI = "hi"
    THAI = "th"
    CHINESE_CHINA = "zh-CN"
    JAPANESE = "ja"
    CHINESE_TAIWAN = "zh-TW"
    KOREAN = "ko"

#Receiving and responding to discord interactions-
class InteractionTypes(enum.IntEnum):
    PING = 1
    APPLICATION_COMMAND = 2
    MESSAGE_COMPONENT = 3
    APPLICATION_COMMAND_AUTOCOMPLETE = 4
    MODAL_SUBMIT = 5

class InteractionContextTypes(enum.IntEnum):
    GUILD = 0
    BOT_DM = 1
    PRIVATE_CHANNEL = 2

class InteractionCallbackTypes(enum.IntEnum):
    PONG = 1  # ACK a Ping
    CHANNEL_MESSAGE_WITH_SOURCE = 4  # Respond to an interaction with a message
    DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE = 5  # ACK and edit a response later, user sees loading
    DEFERRED_UPDATE_MESSAGE = 6  # For components, ACK and edit original message later, no loading
    UPDATE_MESSAGE = 7  # For components, edit the message the component was attached to
    APPLICATION_COMMAND_AUTOCOMPLETE_RESULT = 8  # Autocomplete suggestions
    MODAL = 9  # Respond with a popup modal
    PREMIUM_REQUIRED = 10  # Deprecated; upgrade button for monetized apps
    LAUNCH_ACTIVITY = 12  # Launch app activity (only for enabled apps)

class Interaction(msgspec.Struct, kw_only=True):
    """
    This interaction is received from discord for slash commands, user context menu commands, message context menu commands, message components and modal submits.
    
    ***CREATE, GET, EDIT, DELETE FOLLOWUP MESSAGES require json and query string parameter
    testing. 
    In particular, poll is absent from EditFollowupMessage during mapping.
    Addtionally, thread_id is included in CreateFollowupMessage when the documentation 
    explicitly declares an absence of thread_id for this endpoint.
    GetFollowupMessage, EditFollowupMessage declare similarities to their counter part
    webhook endpoint json and query string data structures. But, remains unclear whether
    thread_id should be included or whether the remaining json and query string parameters
    can be forfeited.
    DeleteFollowMessage declares no similarity to the counterpart webhook endpoint, remains
    unclear whether thread_id can be forfeited.

    Therefore, json and query string parameters require verification for the above endpoints.
    
    
    """

    #Urls FOR InteractionResponse ENDPOINTS
    class InteractionResponseUrls(enum.StrEnum):
        CREATE_INTERACTION_RESPONSE = "/interactions/{interaction.id}/{interaction.token}/callback"

        GET_ORIGINAL_INTERACTION_RESPONSE = "/webhooks/{application.id}/{interaction.token}/messages/@original"
        EDIT_ORIGINAL_INTERACTION_RESPONSE = GET_ORIGINAL_INTERACTION_RESPONSE
        DELETE_ORIGINAL_INTERACTION_RESPONSE = GET_ORIGINAL_INTERACTION_RESPONSE
        
        CREATE_FOLLOWUP_MESSAGE = "/webhooks/{application.id}/{interaction.token}"
        GET_FOLLOWUP_MESSAGE = "/webhooks/{application.id}/{interaction.token}/messages/{message.id}"
        EDIT_FOLLOWUP_MESSAGE = GET_FOLLOWUP_MESSAGE
        DELETE_FOLLOWUP_MESSAGE = GET_FOLLOWUP_MESSAGE

    #QUERY PARAMS FOR Interactions ENDPOINTS
    class CreateInteractionResponseQueryParams(msgspec.Struct, omit_defaults=True):
        with_response: bool = False

    class GetOriginalInteractionResponseQueryParams(msgspec.Struct, omit_defaults=True):
        thread_id: str | None = None

    class EditOriginalInteractionResponseQueryParams(msgspec.Struct, omit_defaults=True):
        thread_id: str | None = None

    class CreateFollowupMessageQueryParams(msgspec.Struct, omit_defaults=True):
        """
        Query parameters for the CreateFollowupMessage endpoint.
        """
        thread_id: str | None = None  # ID of the thread to send the message to

    class GetFollowupMessageQueryParams(msgspec.Struct, omit_defaults=True):
        thread_id: str | None = None  # ID of the thread where the message resides

    class EditFollowupMessageQueryParams(msgspec.Struct, omit_defaults=True):
        thread_id: str | None = None  # ID of the thread where the message resides

    #JSON PARAMS FOR Interactions ENDPOINTS
    class EditOriginalInteractionResponseJSONParams(msgspec.Struct, omit_defaults=True):
        content: str | None = None
        embeds: list["Embed"] | None = None
        flags: int | None = None  # class MessageFlags
        allowed_mentions: "AllowedMentions" | None = None
        components: list["Component"] | None = None
        file_locations: list[str] | None = None
        attachments: list["Attachment"] | None = None

    class CreateFollowupMessageJSONParams(msgspec.Struct, omit_defaults=True):
        """
        JSON/Form body parameters for the CreateFollowupMessage endpoint.
        """
        content: str | None = None  # Max 2000 characters
        embeds: list["Embed"] | None = None  # Up to 10 embeds
        allowed_mentions: "AllowedMentions" | None = None
        components: list["Component"] | None = None  # Requires IS_COMPONENTS_V2 flag
        attachments: list["Attachment"] | None = None
        file_locations: list[str] | None = None
        flags: int | None = None  # e.g., MessageFlags.EPHEMERAL | MessageFlags.IS_COMPONENTS_V2
        tts: bool | None = None

    class EditFollowupMessageJSONParams(msgspec.Struct, omit_defaults=True):
        content: str | None = None  # Max 2000 characters
        embeds: list["Embed"] | None = None  # Up to 10 embeds
        allowed_mentions: "AllowedMentions" | None = None
        components: list["Component"] | None = None  # Requires IS_COMPONENTS_V2 flag
        attachments: list["Attachment"] | None = None
        file_locations: list[str] | None = None
        flags: int | None = None  # e.g., MessageFlags.EPHEMERAL | MessageFlags.IS_COMPONENTS_V2
        tts: bool | None = None
 
    __RELATED_ROUTES : ClassVar[tuple] = ()

    @classmethod
    def init_related_routes(cls):
        if(cls.__RELATED_ROUTES == ()):
            cls.__RELATED_ROUTES = (
                {
                    cls.Urls.CREATE_INTERACTION_RESPONSE : {
                        HttpMethods.POST : {
                            "url_params" :  ("interaction"),
                            "query_params": CreateInteractionResponseQueryParams,
                            "payload" : InteractionResponse,
                            "additional_optional_headers": [],
                            "return_type" : InteractionCallbackResponse | 204
                            }
                    },
                    #SAME AS GET_WEBHOOK_MESSAGE
                    cls.Urls.GET_ORIGINAL_INTERACTION_RESPONSE : {
                        HttpMethods.GET : {
                            "url_params" :  ("application", "interaction"),
                            "query_params": GetOriginalInteractionResponseQueryParams,
                            "payload" : None, 
                            "additional_optional_headers": [],
                            "return_type" : Message
                            }
                    },
                    #SAME AS EDIT_WEBHOOK_MESSAGE
                    cls.Urls.EDIT_ORIGINAL_INTERACTION_RESPONSE : {
                        HttpMethods.PATCH : {
                            "url_params" :  ("application", "interaction"),
                            "query_params": EditOriginalInteractionResponseQueryParams,
                            "payload" : EditOriginalInteractionResponseJSONParams, 
                            "additional_optional_headers": [],
                            "return_type" : Message
                            }
                    },
                    cls.Urls.DELETE_ORIGINAL_INTERACTION_RESPONSE : {
                        HttpMethods.DELETE : {
                            "url_params" :  ("application", "interaction"),
                            "query_params": None,
                            "payload" : None,
                            "additional_optional_headers": [],
                            "return_type" : 204
                            }
                    },
                    #SAME AS EXECUTE_WEBHOOK
                    cls.Urls.CREATE_FOLLOWUP_MESSAGE : {
                        HttpMethods.POST : {
                            "url_params" :  ("application", "interaction"),
                            "query_params": CreateFollowupMessageQueryParams,
                            "payload" : CreateFollowupMessageJSONParams,
                            "additional_optional_headers": [],
                            "return_type" : Message | 204
                            }
                    },
                    #SAME AS GET_WEBHOOK_MESSAGE
                    cls.Urls.GET_FOLLOWUP_MESSAGE : {
                        HttpMethods.GET : {
                            "url_params" :  ("application", "interaction", "message"),
                            "query_params": GetFollowupMessageQueryParams,
                            "payload" : None,
                            "additional_optional_headers": [],
                            "return_type" : Message
                            }
                    },
                    #SAME AS EDIT_WEBHOOK_MESSAGE
                    cls.Urls.EDIT_FOLLOWUP_MESSAGE : {
                        HttpMethods.PATCH : {
                            "url_params" :  ("application", "interaction", "message"),
                            "query_params": EditFollowupMessageQueryParams,
                            "payload" : EditFollowupMessageJSONParams,
                            "additional_optional_headers": [],
                            "return_type" : Message
                            }
                    },
                    cls.Urls.DELETE_FOLLOWUP_MESSAGE : {
                        HttpMethods.DELETE : {
                            "url_params" :  ("application", "interaction", "message"),
                            "query_params": None,
                            "payload" : None,
                            "additional_optional_headers": [],
                            "return_type" : 204
                            }
                    },
                }
            )
        return cls.__RELATED_ROUTES

    @classmethod
    def get_related_routes(cls):  # class-level access
        return cls.init_related_routes()

    @property
    def RELATED_ROUTES(self):   # instance-level access
        return self.init_related_routes()

    id: str
    application_id: str
    type: 'InteractionTypes'
    data: 'InteractionData' | None = None 
    guild: 'Guild' | None = None
    guild_id: str | None = None
    channel: 'Channel' | None = None
    channel_id: str | None = None
    member: 'GuildMember' | None = None 
    user: 'User' | None = None 
    token: str
    version: int
    message: 'Message' | None = None
    app_permissions: str
    locale: 'Locales' | None = None 
    guild_locale: str | None = None
    entitlements: list['Entitlement'] = msgspec.field(default_factory=list)
    authorizing_integration_owners: dict['ApplicationIntegrationTypes', int]
    context: 'InteractionContextTypes' | None = None 
    attachment_size_limit: int

class InteractionData(msgspec.Struct, kw_only=True):
    """
    Interaction data is a combined classes for Application Command, Message Component and Modal Submit
    representing the types of interaction possible from a discord activity.
    """
    # Application Command Interaction fields
    id : str | None = None
    name : str | None = None
    type : 'CommandTypes' | None = None
    resolved : 'Resolved' | None = None
    options : list['AppCommandIntOption'] = msgspec.field(default_factory=list)
    guild_id : str | None = None
    target_id : str | None = None
    # Message Component fields
    custom_id: str | None = None             # custom_id of component or modal
    component_type: 'ComponentTypes' | None = None        # Type of the component (e.g., button, select)
    values: list[str] = msgspec.field(default_factory=list)          # Values selected (select menus only)
    # Modal Submit fields
    components: list['InteractionData'] = msgspec.field(default_factory=list)     # Submitted components in modal (input values)

class Resolved(msgspec.Struct, kw_only=True):
    """
    Resolved objects are included in fields when user, member, role, channel or messages are selected in either application commands or component interactions.
    The purpose is to provide additional field values(may not be all the fields) for the selected objects to avoid subsequent API calls.
    """
    users : dict[str, 'User'] = msgspec.field(default_factory=dict)
    members : dict[str, 'GuildMember'] = msgspec.field(default_factory=dict)
    roles : dict[str, 'Role'] = msgspec.field(default_factory=dict)
    channels : dict[str, 'Channel'] = msgspec.field(default_factory=dict)
    messages : dict[str, 'Message'] = msgspec.field(default_factory=dict)
    attachments : dict[str, 'Attachment'] = msgspec.field(default_factory=dict)

class AppCommandIntOption(msgspec.Struct, kw_only=True):
    """
    App Command Int Option is short for Application Command Interaction Data Option in the discord documentation. Its part of the list payload value of the options field on
    the ApplicationCommandInteraction object.
    An option for the invoked application command interaction.
    """
    name : str
    type : 'AppCommandOptionTypes'
    value : str | int | float | bool | None = None
    options : list['AppCommandOption'] = msgspec.field(default_factory=list)
    focused : bool | None = None

class MessageInteraction(msgspec.Struct, kw_only=True):
    """
    MessageInteraction is part of the message object when the message is a response to an Interaction without an existing message.
    """
    id	: str
    type : 'InteractionTypes'
    name : str
    user : 'User'
    member : 'GuildMember' | None = None

class InteractionResponse(msgspec.Struct, kw_only=True):
    type: 'InteractionCallbackTypes'
    data: 'InteractionCallbackData' | None = None

class InteractionCallbackData(msgspec.Struct, kw_only=True, omit_defaults=True):
    """Unified structure for message, autocomplete, and modal interaction callbacks"""

    # Message fields
    tts: bool | None = None
    content: str | None = None
    embeds: list['Embed'] = msgspec.field(default_factory=list)
    allowed_mentions: 'AllowedMentions' | None = None
    flags: int | None = None
    components: list['Component'] = msgspec.field(default_factory=list)
    attachments: list['Attachment'] = msgspec.field(default_factory=list)
    poll: 'PollCreateRequest' | None = None

    # Autocomplete fields
    choices: list['ApplicationCommandOptionChoice'] = msgspec.field(default_factory=list)  # max 25

    # Modal fields
    custom_id: str | None = None  # max 100 chars
    title: str | None = None      # max 45 chars

class InteractionCallbackResponse(msgspec.Struct, kw_only=True, omit_defaults=True):
    """
    Discord will bundle the original interaction object plus the resource that was created.
    """
    interaction: 'InteractionCallback'
    resource: 'InteractionResource' | None = None

class InteractionCallbackResource(msgspec.Struct, kw_only=True, omit_defaults=True):
    type: 'InteractionCallbackTypes'
    activity_instance: 'InteractionActivityInstanceResource' | None = None
    message: 'Message' | None = None

class InteractionCallback(msgspec.Struct, kw_only=True, omit_defaults=True):
    id: str  # snowflake as string
    type: 'InteractionTypes'
    activity_instance_id: str | None = None
    response_message_id: str | None = None
    response_message_loading: bool | None = None
    response_message_ephemeral: bool | None = None

class InteractionActivityInstanceResource(msgspec.Struct, kw_only=True, omit_defaults=True):
    id: str

##Discord request API data models

#Application commands-
##Discord response API data models
class ApplicationCommandTypes(enum.IntEnum):
    CHAT_INPUT = 1
    USER = 2
    MESSAGE = 3
    PRIMARY_ENTRY_POINT = 4

class AppCommandOptionTypes(enum.IntEnum):
    SUB_COMMAND = 1
    SUB_COMMAND_GROUP = 2
    STRING = 3
    INTEGER = 4
    BOOLEAN = 5
    USER = 6
    CHANNEL = 7
    ROLE = 8
    MENTIONABLE = 9
    NUMBER = 10
    ATTACHMENT = 11

class EntryPointCommandHandlerType(enum.IntEnum):
    APP_HANDLER = 1
    DISCORD_LAUNCH_ACTIVITY = 2

class ApplicationCommandOptionTypes(enum.IntEnum):
    SUB_COMMAND = 1
    SUB_COMMAND_GROUP = 2
    STRING = 3
    INTEGER = 4
    BOOLEAN = 5
    USER = 6
    CHANNEL = 7
    ROLE = 8
    MENTIONABLE = 9
    NUMBER = 10
    ATTACHMENT = 11

class ApplicationCommandPermissionTypes(enum.IntEnum):
    ROLE = 1
    USER = 2
    CHANNEL = 3

class ApplicationCommand(msgspec.Struct, kw_only=True, omit_defaults=True):
    id: str  # snowflake
    type: 'ApplicationCommandTypes' | None = None  # one of command types, defaults to 1
    application_id: str  # snowflake
    guild_id: str | None = None
    name: str
    name_localizations: dict['Locales', str] = msgspec.field(default_factory=dict)
    description: str
    description_localizations: dict['Locales', str] = msgspec.field(default_factory=dict)
    options: list['ApplicationCommandOption'] = msgspec.field(default_factory=list)  # array of command options, max 25 (CHAT_INPUT)
    default_member_permissions: str | None = None  # bit set permissions
    dm_permission: bool | None = None  # deprecated
    default_permission: bool | None = None  # deprecated, defaults to true
    nsfw: bool | None = None  # defaults to false
    integration_types: list['ApplicationIntegrationTypes'] = msgspec.field(default_factory=list)  # list of integration types
    contexts: list['InteractionContextTypes'] = msgspec.field(default_factory=list)  # list of interaction context types
    version: str  # snowflake
    handler: 'EntryPointCommandHandlerType' | None = None  # one of command handler types

class ApplicationCommandOption(msgspec.Struct, kw_only=True):
    type: 'ApplicationCommandOptionTypes'
    name: str
    name_localizations: dict['Locales', str] = msgspec.field(default_factory=dict)
    description: str
    description_localizations: dict['Locales', str] = msgspec.field(default_factory=dict)
    required: bool | None = None
    choices: list['ApplicationCommandOptionChoice'] = msgspec.field(default_factory=list)
    options: list["ApplicationCommandOption"] = msgspec.field(default_factory=list)
    channel_types: list['ChannelTypes'] = msgspec.field(default_factory=list)
    min_value: int | float | None = None
    max_value: int | float | None = None
    min_length: int | None = None
    max_length: int | None = None
    autocomplete: bool | None = None

class ApplicationCommandOptionChoice(msgspec.Struct, kw_only=True, kw_only=True):
    name: str
    name_localizations: dict['Locales', str] = msgspec.field(default_factory=dict)
    value: str | int | float

class GuildApplicationCommandPermissions(msgspec.Struct, kw_only=True, kw_only=True):
    """
    Returned when fetching the permissions for an app's command(s) in a guild
    """
    id: str  # snowflake
    application_id: str  # snowflake
    guild_id: str  # snowflake
    permissions: list["ApplicationCommandPermissions"]

class ApplicationCommandPermissions(msgspec.Struct, kw_only=True, kw_only=True):
    """
    Application command permissions allow you to enable or disable commands for specific users, roles, or channels within a guild.
    """
    id: str  # snowflake (role or user ID)
    type: 'ApplicationCommandPermissionTypes'  # 1 = ROLE, 2 = USER, 3 = CHANNEL
    permission: bool

##Discord request API data models


#Components-
class ComponentTypes(enum.IntEnum):
    ACTION_ROW = 1
    BUTTON = 2
    STRING_SELECT = 3
    TEXT_INPUT = 4
    USER_SELECT = 5
    ROLE_SELECT = 6
    MENTIONABLE_SELECT = 7
    CHANNEL_SELECT = 8
    SECTION = 9
    TEXT_DISPLAY = 10
    THUMBNAIL = 11
    MEDIA_GALLERY = 12
    FILE = 13
    SEPARATOR = 14
    CONTAINER = 17

class ButtonStyles(enum.IntEnum):
    PRIMARY = 1
    SECONDARY = 2
    SUCCESS = 3
    DANGER = 4
    LINK = 5
    PREMIUM = 6

class TextInputStyles(enum.IntEnum):
    SHORT = 1
    PARAGRAPH = 2

class Component(msgspec.Struct, kw_only=True):
    """
    Represents any type of interactive Discord component, they are fields to message object and modal.
    The fields available depend on the `type` of the component.
    """

    #All components share these fields.
    type : 'ComponentTypes'
    id : str| int | None = None

    #Some components share these fields.
    custom_id : str | None = None
    components : list['Component'] = msgspec.field(default_factory=list)
    style : 'ButtonStyles' | 'TextInputStyles' | None = None
    label : str | None = None
    content : str | None = None
    emoji : 'Emoji' | None = None
    sku_id : str | None = None
    url : str | None = None
    disabled : bool | None = None
    options : list['SelectOption'] = msgspec.field(default_factory=list)
    placeholder : str | None = None
    min_values : int | None = None
    max_values : int | None = None
    min_length : int | None = None
    max_length : int | None = None
    required : bool | None = None
    value : str | None = None
    placeholder : str | None = None
    default_values : list['SelectDefaultValue'] = msgspec.field(default_factory=list)
    channel_types : list['ChannelTypes'] = msgspec.field(default_factory=list)
    accessory : 'Component' | None = None
    media : 'UnfurledMediaItem' | None = None
    description : str | None = None
    spoiler : bool | None = None
    items : list['MediaGalleryItem'] = msgspec.field(default_factory=list)
    file : 'UnfurledMediaItem' | None = None
    name : str | None = None
    size : int | None = None
    divider : bool | None = None
    spacing : int | None = None
    accent_color : int | None = None

class SelectOption(msgspec.Struct, kw_only=True):
    """
    Select Option is part of the UI components object — specifically for dropdown menus (also called select menus).
    """
    label : str 
    value : str
    description : str | None = None
    emoji : 'Emoji' | None = None
    default : bool | None = None

class SelectDefaultValue(msgspec.Struct, kw_only=True):
    """
    Select Default Value Structure is used in Discord's select menus (dropdown components) — specifically in select menus that allow choosing users, roles, or channels.
    """
    id : str 
    type : str

class UnfurledMediaItem(msgspec.Struct, kw_only=True):
    """
    Unfurled Media Item Structure in Discord is a structure used to represent media items (images, videos, etc.) that are included in a message embed or unfurl, especially in rich content previews or message content rendering.
    """
    url : str
    proxy_url : str | None = None
    height : int | None = None
    width : int | None = None
    content_type : str | None = None
    attachment_id : str | None = None

class MediaGalleryItem(msgspec.Struct, kw_only=True):
    """
    Media Gallery Item is part of Discord's rich media and post-style messages that include multiple images or media items, like galleries.
    It defines one item (image, video, etc.) in a media gallery block, which Discord displays as a grid or carousel of media. 
    This structure includes the media URL or attachment, optional alt text, and spoiler behavior.
    """
    media : 'UnfurledMediaItem'
    description : str | None = None
    spoiler : bool | None = None


###### Start of Discord Resources data models
#Application Role Connection Metadata-
class ApplicationRoleConnectionMetadataTypes(enum.IntEnum):
    INTEGER_LESS_THAN_OR_EQUAL = 1
    INTEGER_GREATER_THAN_OR_EQUAL = 2
    INTEGER_EQUAL = 3
    INTEGER_NOT_EQUAL = 4
    DATETIME_LESS_THAN_OR_EQUAL = 5
    DATETIME_GREATER_THAN_OR_EQUAL = 6
    BOOLEAN_EQUAL = 7
    BOOLEAN_NOT_EQUAL = 8

class ApplicationRoleConnectionMetadata(msgspec.Struct, kw_only=True):
    """
    Sent to discord to register properties which determine where a user passes for a custom linked role.
    """
    type: 'ApplicationRoleConnectionMetadataTypes'
    key: str
    name: str
    name_localizations: dict['Locales', str] = msgspec.field(default_factory=dict)
    description: str
    description_localizations: dict['Locales', str] = msgspec.field(default_factory=dict)

#Application-
class ApplicationFlags(enum.IntEnum):
    APPLICATION_AUTO_MODERATION_RULE_CREATE_BADGE = 1 << 6
    GATEWAY_PRESENCE = 1 << 12
    GATEWAY_PRESENCE_LIMITED = 1 << 13
    GATEWAY_GUILD_MEMBERS = 1 << 14
    GATEWAY_GUILD_MEMBERS_LIMITED = 1 << 15
    VERIFICATION_PENDING_GUILD_LIMIT = 1 << 16
    EMBEDDED = 1 << 17
    GATEWAY_MESSAGE_CONTENT = 1 << 18
    GATEWAY_MESSAGE_CONTENT_LIMITED = 1 << 19
    APPLICATION_COMMAND_BADGE = 1 << 23

class ApplicationEventWebhookStatus(enum.IntEnum):
    DISABLED = 1
    ENABLED = 2
    DISABLED_BY_DISCORD = 3

class ApplicationIntegrationTypes(enum.StrEnum):
    GUILD_INSTALL = "guild_install"
    USER_INSTALL = "user_install"

class Application(msgspec.Struct, kw_only=True):
    """
    Applications (or "apps") are containers for developer platform features, and can be installed to Discord servers and/or user accounts.
    """
    id : str
    name : str
    icon : str
    description : str
    rpc_origins : list[str] = msgspec.field(default_factory=list)
    bot_public : bool
    bot_require_code_grant : bool
    bot : 'User' | None = None
    terms_of_service_url : str | None = None
    privacy_policy_url : str | None = None
    owner : 'User' | None = None
    verify_key : str
    team : 'Team' | None = None
    guild_id : str | None = None
    guild : 'Guild' | None = None
    primary_sku_id : str | None = None
    slug : str | None = None
    cover_image : str | None = None
    flags : 'ApplicationFlags' | None = None
    approximate_guild_count : int | None = None
    approximate_user_install_count : int | None = None
    approximate_user_authorization_count : int | None = None
    redirect_uris : list[str] = msgspec.field(default_factory=list)
    interactions_endpoint_url : str | None = None
    role_connections_verification_url : str | None = None
    event_webhooks_url : str | None = None
    event_webhooks_status : 'ApplicationEventWebhookStatus' | None = None
    event_webhooks_types : list['WebhookEventTypes'] = msgspec.field(default_factory=list)
    tags : list[str] = msgspec.field(default_factory=list)
    install_params : 'InstallParams' | None = None
    integration_types_config : dict['ApplicationIntegrationTypes', 'ApplicationIntegrationTypeConfiguration'] = msgspec.field(default_factory=dict)
    custom_install_url : str | None = None

class ApplicationIntegrationTypeConfiguration(msgspec.Struct, kw_only=True):
    """
    ApplicationIntegrationTypeConfiguration object defines how an application is configured.
    """
    oauth2_install_params : 'InstallParams' | None = None

class InstallParams(msgspec.Struct, kw_only=True):
    """
    InstallParams object defines the actions possible on the application and what actions the application can commit across the discord application.
    InstallParams also defines the actions the application can commit in a server.
    """
    scopes : list['OAuth2Scopes']
    permissions : str

class ActivityInstance(msgspec.Struct, kw_only=True):
    application_id: str  # Application ID (snowflake)
    instance_id: str  # Activity Instance ID
    launch_id: str  # Unique identifier for the launch (snowflake)
    location: str  # Location the instance is running in
    users: list[str]  # IDs of the Users currently connected to the instance (snowflakes)

class ActivityLocation(msgspec.Struct, kw_only=True):
    """Represents the location in which an activity instance is running."""
    id: str  # Unique identifier for the location
    kind: int  # Activity Location Kind Enum (should be replaced with enum type)
    channel_id: str  # ID of the Channel (snowflake)
    guild_id: str | None = None  # ID of the Guild (optional & nullable, snowflake)

class ActivityLocationKind(enum.StrEnum):
    """Enum describing the kind of activity location."""
    GC = "gc"  # Location is a Guild Channel
    PC = "pc"  # Location is a Private Channel, such as a DM or GDM

#Audit log-
class AuditLogEvents(enum.IntEnum):
    # Guild
    GUILD_UPDATE = 1

    # Channels
    CHANNEL_CREATE = 10
    CHANNEL_UPDATE = 11
    CHANNEL_DELETE = 12
    CHANNEL_OVERWRITE_CREATE = 13
    CHANNEL_OVERWRITE_UPDATE = 14
    CHANNEL_OVERWRITE_DELETE = 15

    # Members
    MEMBER_KICK = 20
    MEMBER_PRUNE = 21
    MEMBER_BAN_ADD = 22
    MEMBER_BAN_REMOVE = 23
    MEMBER_UPDATE = 24
    MEMBER_ROLE_UPDATE = 25
    MEMBER_MOVE = 26
    MEMBER_DISCONNECT = 27
    BOT_ADD = 28

    # Roles
    ROLE_CREATE = 30
    ROLE_UPDATE = 31
    ROLE_DELETE = 32

    # Invites
    INVITE_CREATE = 40
    INVITE_UPDATE = 41
    INVITE_DELETE = 42

    # Webhooks
    WEBHOOK_CREATE = 50
    WEBHOOK_UPDATE = 51
    WEBHOOK_DELETE = 52

    # Emojis
    EMOJI_CREATE = 60
    EMOJI_UPDATE = 61
    EMOJI_DELETE = 62

    # Messages
    MESSAGE_DELETE = 72
    MESSAGE_BULK_DELETE = 73
    MESSAGE_PIN = 74
    MESSAGE_UNPIN = 75

    # Integrations
    INTEGRATION_CREATE = 80
    INTEGRATION_UPDATE = 81
    INTEGRATION_DELETE = 82

    # Stage Instances
    STAGE_INSTANCE_CREATE = 83
    STAGE_INSTANCE_UPDATE = 84
    STAGE_INSTANCE_DELETE = 85

    # Stickers
    STICKER_CREATE = 90
    STICKER_UPDATE = 91
    STICKER_DELETE = 92

    # Guild Scheduled Events
    GUILD_SCHEDULED_EVENT_CREATE = 100
    GUILD_SCHEDULED_EVENT_UPDATE = 101
    GUILD_SCHEDULED_EVENT_DELETE = 102

    # Threads
    THREAD_CREATE = 110
    THREAD_UPDATE = 111
    THREAD_DELETE = 112

    # Application Command Permissions
    APPLICATION_COMMAND_PERMISSION_UPDATE = 121

    # Soundboard
    SOUNDBOARD_SOUND_CREATE = 130
    SOUNDBOARD_SOUND_UPDATE = 131
    SOUNDBOARD_SOUND_DELETE = 132

    # Auto Moderation
    AUTO_MODERATION_RULE_CREATE = 140
    AUTO_MODERATION_RULE_UPDATE = 141
    AUTO_MODERATION_RULE_DELETE = 142
    AUTO_MODERATION_BLOCK_MESSAGE = 143
    AUTO_MODERATION_FLAG_TO_CHANNEL = 144
    AUTO_MODERATION_USER_COMMUNICATION_DISABLED = 145
    AUTO_MODERATION_QUARANTINE_USER = 146

    # Creator Monetization
    CREATOR_MONETIZATION_REQUEST_CREATED = 150
    CREATOR_MONETIZATION_TERMS_ACCEPTED = 151

    # Onboarding
    ONBOARDING_PROMPT_CREATE = 163
    ONBOARDING_PROMPT_UPDATE = 164
    ONBOARDING_PROMPT_DELETE = 165
    ONBOARDING_CREATE = 166
    ONBOARDING_UPDATE = 167

    # Home Settings
    HOME_SETTINGS_CREATE = 190
    HOME_SETTINGS_UPDATE = 191

class AuditLog(msgspec.Struct, kw_only=True):
    application_commands: list["ApplicationCommandTypes"]
    audit_log_entries: list["AuditLogEntry"]
    auto_moderation_rules: list["AutoModerationRule"]
    guild_scheduled_events: list["GuildScheduledEvent"]
    integrations: list["Integration"]
    threads: list["Channel"]
    users: list["User"]
    webhooks: list["Webhook"]

class AuditLogEntry(msgspec.Struct, kw_only=True):
    """
    AuditLogEntry represents a single administrative action/event on a discord object(User, Role, Guild etc.)
    """
    target_id: str | None = None
    changes: list["AuditLogChange"] = msgspec.field(default_factory=list)
    user_id: str | None = None
    id: str
    action_type: "AuditLogEvents"
    options: "OptionalAuditEntryInfo" | None = None
    reason: str | None = None

class AuditLogChange(msgspec.Struct, kw_only=True):
    """
    Changes to the field value on the specified target_id representing a discord object.
    """
    new_value: Any | None = None 
    old_value: Any | None = None 
    key: str

class OptionalAuditEntryInfo(msgspec.Struct, kw_only=True):
    application_id: str | None = None
    auto_moderation_rule_name: str | None = None
    auto_moderation_rule_trigger_type: str | None = None
    channel_id: str | None = None
    count: str | None = None
    delete_member_days: str | None = None
    id: str | None = None
    members_removed: str | None = None
    message_id: str | None = None
    role_name: str | None = None
    type: str | None = None
    integration_type: str | None = None

#Auto moderation-
class EventTypes(enum.IntEnum):
    MESSAGE_SEND = 1  # when a member sends or edits a message in the guild
    MEMBER_UPDATE = 2  # when a member edits their profile

class TriggerTypes(enum.IntEnum):
    KEYWORD = 1           # check if content contains words from a user defined list of keywords (max 6 per guild)
    SPAM = 3              # check if content represents generic spam (max 1 per guild)
    KEYWORD_PRESET = 4    # check if content contains words from internal pre-defined wordsets (max 1 per guild)
    MENTION_SPAM = 5      # check if content contains more unique mentions than allowed (max 1 per guild)
    MEMBER_PROFILE = 6    # check if member profile contains words from a user defined list of keywords (max 1 per guild)

class KeywordPresetTypes(enum.IntEnum):
    PROFANITY = 1          # words that may be considered forms of swearing or cursing
    SEXUAL_CONTENT = 2     # words that refer to sexually explicit behavior or activity
    SLURS = 3              # personal insults or words that may be considered hate speech

class ActionTypes(enum.IntEnum):
    BLOCK_MESSAGE = 1             # blocks a member's message and prevents it from being posted
    SEND_ALERT_MESSAGE = 2        # logs user content to a specified channel
    TIMEOUT = 3                   # timeout user for a specified duration
    BLOCK_MEMBER_INTERACTION = 4  # prevents a member from using text, voice, or other interactions

class AutoModerationRule(msgspec.Struct, kw_only=True):
    id: str
    guild_id: str
    name: str
    creator_id: str
    event_type: 'EventTypes'
    trigger_type: 'TriggerTypes'
    trigger_metadata: 'TriggerMetadata'
    actions: list['AutoModerationAction']
    enabled: bool
    exempt_roles: list[str]
    exempt_channels: list[str]

class TriggerMetadata(msgspec.Struct, kw_only=True):
    keyword_filter: list[str] = msgspec.field(default_factory=list)                # For KEYWORD, MEMBER_PROFILE
    regex_patterns: list[str] = msgspec.field(default_factory=list)                # For KEYWORD, MEMBER_PROFILE
    presets: list['KeywordPresetTypes'] = msgspec.field(default_factory=list)                        # For KEYWORD_PRESET, using int for preset types
    allow_list: list[str] = msgspec.field(default_factory=list)                     # For KEYWORD, KEYWORD_PRESET, MEMBER_PROFILE
    mention_total_limit: int | None = None                  # For MENTION_SPAM
    mention_raid_protection_enabled: bool | None = None    # For MENTION_SPAM

class AutoModerationAction(msgspec.Struct, kw_only=True):
    type: 'ActionTypes'                 # The type of action
    metadata: 'ActionMetadata' | None = None  # Additional metadata needed during execution (optional)

class ActionMetadata(msgspec.Struct, kw_only=True):
    channel_id: str | None = None         # For SEND_ALERT_MESSAGE
    duration_seconds: int | None = None   # For TIMEOUT (max 2419200)
    custom_message: str | None = None     # For BLOCK_MESSAGE

#Channel-
class SortOrderTypes(enum.IntEnum):
    LATEST_ACTIVITY = 0
    CREATION_DATE = 1

class ForumLayoutTypes(enum.IntEnum):
    NOT_SET = 0
    LIST_VIEW = 1
    GALLERY_VIEW = 2

class ChannelFlags(enum.IntEnum):
    PINNED = 1 << 1
    REQUIRE_TAG = 1 << 4
    HIDE_MEDIA_DOWNLOAD_OPTIONS = 1 << 15

class ChannelTypes(enum.IntEnum):
    GUILD_TEXT = 0
    DM = 1
    GUILD_VOICE = 2
    GROUP_DM = 3
    GUILD_CATEGORY = 4
    GUILD_ANNOUNCEMENT = 5
    ANNOUNCEMENT_THREAD = 10
    PUBLIC_THREAD = 11
    PRIVATE_THREAD = 12
    GUILD_STAGE_VOICE = 13
    GUILD_DIRECTORY	= 14
    GUILD_FORUM = 15
    GUILD_MEDIA	= 16

class VideoQualityModes(enum.IntEnum):
    AUTO = 1
    FULL = 2

class Channel(msgspec.Struct, kw_only=True):
    """
    Channel represents a guild channel or DM channel in the Discord application
    """

    class WebhookUrls(enum.StrEnum):
        CREATE_WEBHOOK = "/channels/{channel.id}/webhooks"
        GET_CHANNEL_WEBHOOKS = CREATE_WEBHOOK

    class CreateWebhookJSONParams(msgspec.Struct, kw_only=True):
        """
        JSON parameters for creating a Discord webhook.
        """
        name: str                   # required: 1-80 characters
        avatar: str | None = None   # optional: base64 image data

    __RELATED_ROUTES : ClassVar[tuple] = ()
    @classmethod
    def init_related_routes(cls):
        if(cls.__RELATED_ROUTES == ()):
            cls.__RELATED_ROUTES = (
                {
                    cls.Urls.CREATE_WEBHOOK : {
                        HttpMethods.POST : {
                            "url_params" : ("channel"),
                            "query_params": None,
                            "payload" : cls.CreateWebhookJSONParams, 
                            "additional_optional_headers": ["X-Audit-Log-Reason"],
                            "return_type" : Webhook
                            }
                    },
                    cls.Urls.GET_CHANNEL_WEBHOOKS : {
                        HttpMethods.GET : {
                            "url_params" : ("channel"),
                            "query_params": None,
                            "payload" : None,
                            "additional_optional_headers": [],
                            "return_type" : list[Webhook]
                            }
                    },
                }
            )
        return cls.__RELATED_ROUTES

    @classmethod
    def get_related_routes(cls):  # class-level access
        return cls.init_related_routes()

    @property
    def RELATED_ROUTES(self):   # instance-level access
        return self.init_related_routes()

    id: str  # snowflake
    type: 'ChannelTypes'
    guild_id: str | None = None  # snowflake
    position: int | None = None
    permission_overwrites: list['Overwrite'] = msgspec.field(default_factory=list)
    name: str | None = None
    topic: str | None = None
    nsfw: bool | None = None
    last_message_id: str | None = None  # snowflake
    bitrate: int | None = None
    user_limit: int | None = None
    rate_limit_per_user: int | None = None
    recipients: list['User'] = msgspec.field(default_factory=list)
    icon: str | None = None
    owner_id: str | None = None  # snowflake
    application_id: str | None = None  # snowflake
    managed: bool | None = None
    parent_id: str | None = None  # snowflake
    last_pin_timestamp: datetime | None = None
    rtc_region: str | None = None
    video_quality_mode: int | 'VideoQualityModes' = 1
    message_count: int | None = None
    member_count: int | None = None
    thread_metadata: 'ThreadMetadata' | None = None
    member: 'ThreadMember' | None = None
    default_auto_archive_duration: int | None = None
    permissions: str | None = None
    flags: int | None = None
    total_message_sent: int | None = None
    available_tags: list['ForumTag'] = msgspec.field(default_factory=list)
    applied_tags: list[str] = msgspec.field(default_factory=list)  # snowflake array
    default_reaction_emoji: 'DefaultReaction' | None = None
    default_thread_rate_limit_per_user: int | None = None
    default_sort_order: 'SortOrderTypes' | None = None
    default_forum_layout: 'ForumLayoutTypes' | None = None

class FollowedChannel(msgspec.Struct, kw_only=True):
    """
    Represents a followed channel relationship in Discord.
    """
    channel_id: str  # snowflake - source channel ID
    webhook_id: str  # snowflake - created target webhook ID

class Overwrite(msgspec.Struct, kw_only=True):
    """
    Determines which permissions are allowed or denied for a role or channel.
    """
    id : str
    type : int
    allow : str
    deny : str

class ThreadMetadata(msgspec.Struct, kw_only=True):
    """
    Thread metadata object contains a number of thread-specific channel fields.
    """
    archived : bool
    auto_archive_duration : int
    archive_timestamp : datetime
    locked : bool
    invitable : bool | None = None
    create_timestamp : datetime | None = None

class ThreadMember(msgspec.Struct, kw_only=True):
    """
    ThreadMember contains information on a User who joined a thread.
    """
    id : str | None = None
    user_id : str | None = None
    join_timestamp : datetime
    flags : int
    member : 'GuildMember' | None = None

class DefaultReaction(msgspec.Struct, kw_only=True):
    """
    An object that specifies the emoji to use as the default way to react to a forum post. Exactly one of emoji_id and emoji_name must be set.
    """
    emoji_id : str | None = None
    emoji_name : str | None = None

class ForumTag(msgspec.Struct, kw_only=True):
    """
    An object that represents a tag that is able to be applied to a thread in a GUILD_FORUM or GUILD_MEDIA channel.
    """
    id : str
    name : str
    moderated : bool
    emoji_id : str | None = None
    emoji_name : str | None = None

#Emoji-
class Emoji(msgspec.Struct, kw_only=True):
    """
    Emoji object represents either a custom emoji created within a server (guild) or a Unicode emoji used in various 
    features like reactions, messages, and components (like buttons or select menus).
    """
    id : str | None = None
    name : str | None = None
    roles : list[str] = msgspec.field(default_factory=list)
    user : 'User' | None = None
    require_colons : bool | None = None
    managed : bool | None = None
    animated : bool | None = None
    available : bool | None = None

#Entitlement-
class EntitlementTypes(enum.IntEnum):
    PURCHASE = 1
    PREMIUM_SUBSCRIPTION = 2
    DEVELOPER_GIFT = 3
    TEST_MODE_PURCHASE = 4
    FREE_PURCHASE = 5
    USER_GIFT = 6
    PREMIUM_PURCHASE = 7
    APPLICATION_SUBSCRIPTION = 8

class Entitlement(msgspec.Struct, kw_only=True):
    """
    Entitlement represents a user or guild having access to a premium offering in your application.
    """
    id: str  # snowflake
    sku_id: str  # snowflake
    application_id: str  # snowflake
    user_id: str | None = None  # snowflake
    type: "EntitlementTypes"
    deleted: bool
    starts_at: datetime | None = None
    ends_at: datetime | None = None
    guild_id: str | None = None  # snowflake
    consumed: bool | None = None

#Guild scheduled event-
class GuildScheduledEventPrivacyLevels(enum.IntEnum):
    GUILD_ONLY = 2  # the scheduled event is only accessible to guild members

class GuildScheduledEventStatus(enum.IntEnum):
    SCHEDULED = 1
    ACTIVE = 2
    COMPLETED = 3  
    CANCELED = 4   

class GuildScheduledEventEntityTypes(enum.IntEnum):
    STAGE_INSTANCE = 1
    VOICE = 2
    EXTERNAL = 3

class GuildScheduledEventRecurrenceFrequencies(enum.IntEnum):
    YEARLY = 0
    MONTHLY = 1
    WEEKLY = 2
    DAILY = 3

class GuildScheduledEventRecurrenceWeekdays(enum.IntEnum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

class GuildScheduledEventRecurrenceMonths(enum.IntEnum):
    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12

class GuildScheduledEvent(msgspec.Struct, kw_only=True):
    id: str                              # snowflake
    guild_id: str                       # snowflake
    channel_id: str | None = None       # snowflake or null if EXTERNAL entity_type
    creator_id: str | None = None       # snowflake, optional
    name: str                          # 1-100 chars
    description: str | None = None      # 1-1000 chars, optional
    scheduled_start_time: datetime           # ISO8601 timestamp
    scheduled_end_time: datetime | None = None  # ISO8601 timestamp, optional (required if EXTERNAL)
    privacy_level: 'GuildScheduledEventPrivacyLevels'     # privacy level enum/int
    status: 'GuildScheduledEventStatus'                        # event status enum/int
    entity_type: 'GuildScheduledEventEntityTypes'                 # scheduled entity type enum/int
    entity_id: str | None = None       # snowflake, optional
    entity_metadata: 'GuildScheduledEventEntityMetadata' | None = None  # optional metadata object
    creator: 'User' | None = None         # optional user object
    user_count: int | None = None       # optional number of subscribed users
    image: str | None = None            # optional cover image hash
    recurrence_rule: 'GuildScheduledEventRecurrenceRule' | None = None  # optional recurrence rule

class GuildScheduledEventEntityMetadata(msgspec.Struct, kw_only=True):
    location: str | None = None  # For EXTERNAL events, 1–100 chars

class GuildScheduledEventRecurrenceRule(msgspec.Struct, kw_only=True):
    start: datetime                                       # ISO8601 timestamp
    end: datetime | None = None                           # optional ISO8601 timestamp
    frequency: 'GuildScheduledEventRecurrenceFrequencies'                    # how often the event occurs
    interval: int                                         # spacing between events
    by_weekday: list['GuildScheduledEventRecurrenceWeekdays'] = msgspec.field(default_factory=list)  # specific days in a week
    by_n_weekday: list['GuildScheduledEventRecurrenceNWeekday'] = msgspec.field(default_factory=list)  # nth weekday of a month
    by_month: list['GuildScheduledEventRecurrenceMonths'] = msgspec.field(default_factory=list)     # specific months
    by_month_day: list[int] = msgspec.field(default_factory=list)                 # specific month days
    by_year_day: list[int] = msgspec.field(default_factory=list)                  # days in a year (1–364)
    count: int | None = None                              # max number of recurrences                         # max number of recurrences

class GuildScheduledEventRecurrenceNWeekday(msgspec.Struct, kw_only=True):
    n: int  # 1–5
    day: 'GuildScheduledEventRecurrenceWeekdays'

class GuildScheduledEventUser(msgspec.Struct, kw_only=True):
    guild_scheduled_event_id: str  # snowflake
    user: 'User'
    member: 'GuildMember' | None = None

#Guild template-
class GuildTemplate(msgspec.Struct, kw_only=True):
    """
    Represents a code that when used, creates a guild based on a snapshot of an existing guild.
    """
    code: str
    name: str
    description: str | None = None
    usage_count: int
    creator_id: str  # snowflake
    creator: "User"
    created_at: datetime
    updated_at: datetime
    source_guild_id: str  # snowflake
    serialized_source_guild: "Guild"
    is_dirty: bool | None = None

#Guild-
class VerificationLevels(enum.IntEnum):
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    VERY_HIGH = 4

class DefaultMessageNotificationLevels(enum.IntEnum):
    ALL_MESSAGES = 0
    ONLY_MENTIONS = 1

class ExplicitContentFilterLevels(enum.IntEnum):
    DISABLED = 0
    MEMBERS_WITHOUT_ROLES = 1
    ALL_MEMBERS = 2

class GuildFeatures(enum.StrEnum):
    """
    Although this data structure looks seemingly redundant, it can be useful for type validation checking when a string value is recevied from an API.
    """
    ANIMATED_BANNER = "ANIMATED_BANNER"
    ANIMATED_ICON = "ANIMATED_ICON"
    APPLICATION_COMMAND_PERMISSIONS_V2 = "APPLICATION_COMMAND_PERMISSIONS_V2"
    AUTO_MODERATION = "AUTO_MODERATION"
    BANNER = "BANNER"
    COMMUNITY = "COMMUNITY"
    CREATOR_MONETIZABLE_PROVISIONAL = "CREATOR_MONETIZABLE_PROVISIONAL"
    CREATOR_STORE_PAGE = "CREATOR_STORE_PAGE"
    DEVELOPER_SUPPORT_SERVER = "DEVELOPER_SUPPORT_SERVER"
    DISCOVERABLE = "DISCOVERABLE"
    FEATURABLE = "FEATURABLE"
    INVITES_DISABLED = "INVITES_DISABLED"
    INVITE_SPLASH = "INVITE_SPLASH"
    MEMBER_VERIFICATION_GATE_ENABLED = "MEMBER_VERIFICATION_GATE_ENABLED"
    MORE_SOUNDBOARD = "MORE_SOUNDBOARD"
    MORE_STICKERS = "MORE_STICKERS"
    NEWS = "NEWS"
    PARTNERED = "PARTNERED"
    PREVIEW_ENABLED = "PREVIEW_ENABLED"
    RAID_ALERTS_DISABLED = "RAID_ALERTS_DISABLED"
    ROLE_ICONS = "ROLE_ICONS"
    ROLE_SUBSCRIPTIONS_AVAILABLE_FOR_PURCHASE = "ROLE_SUBSCRIPTIONS_AVAILABLE_FOR_PURCHASE"
    ROLE_SUBSCRIPTIONS_ENABLED = "ROLE_SUBSCRIPTIONS_ENABLED"
    SOUNDBOARD = "SOUNDBOARD"
    TICKETED_EVENTS_ENABLED	= "TICKETED_EVENTS_ENABLED"
    VANITY_URL = "VANITY_URL"
    VERIFIED = "VERIFIED"
    VIP_REGIONS = "VIP_REGIONS"
    WELCOME_SCREEN_ENABLED = "WELCOME_SCREEN_ENABLED"
    GUESTS_ENABLED = "GUESTS_ENABLED"
    GUILD_TAGS = "GUILD_TAGS"
    ENHANCED_ROLE_COLORS = "ENHANCED_ROLE_COLORS"

class MFALevels(enum.IntEnum):
    NONE = 0
    ELEVATED = 1

class SystemChannelFlags(enum.IntEnum):
    SUPPRESS_JOIN_NOTIFICATIONS = 1 << 0
    SUPPRESS_PREMIUM_SUBSCRIPTIONS = 1 << 1
    SUPPRESS_GUILD_REMINDER_NOTIFICATIONS = 1 << 2
    SUPPRESS_JOIN_NOTIFICATION_REPLIES = 1 << 3
    SUPPRESS_ROLE_SUBSCRIPTION_PURCHASE_NOTIFICATIONS = 1 << 4
    SUPPRESS_ROLE_SUBSCRIPTION_PURCHASE_NOTIFICATION_REPLIES = 1 << 5

class PremiumTiers(enum.IntEnum):
    NONE = 0
    TIER_1 = 1
    TIER_2 = 2
    TIER_3 = 3

class GuildNSFWLevels(enum.IntEnum):
    DEFAULT = 0
    EXPLICIT = 1
    SAFE = 2
    AGE_RESTRICTED = 3

class GuildMemberFlags(enum.IntFlag):
    DID_REJOIN = 1 << 0
    COMPLETED_ONBOARDING = 1 << 1
    BYPASSES_VERIFICATION = 1 << 2
    STARTED_ONBOARDING = 1 << 3
    IS_GUEST = 1 << 4
    STARTED_HOME_ACTIONS = 	1 << 5
    COMPLETED_HOME_ACTIONS = 1 << 6
    AUTOMOD_QUARANTINED_USERNAME = 1 << 7
    DM_SETTINGS_UPSELL_ACKNOWLEDGED = 1 << 9
    AUTOMOD_QUARANTINED_GUILD_TAG = 1 << 10

class IntegrationExpireBehaviors(enum.IntEnum):
    REMOVE_ROLE = 0
    KICK = 1

class OnboardingModes(enum.IntEnum):
    ONBOARDING_DEFAULT = 0 
    ONBOARDING_ADVANCED = 1 

class PromptTypes(enum.IntEnum):
    MULTIPLE_CHOICE = 0
    DROPDOWN = 1

class Guild(msgspec.Struct, kw_only=True):
    """
    Guild represents an isolated collection of users and channels, and are often referred to as "servers" in the UI.
    """

    class WebhookUrls(enum.StrEnum):
        GET_GUILD_WEBHOOKS = "/guilds/{guild.id}/webhooks"

    __RELATED_ROUTES : ClassVar[tuple] = ()

    @classmethod
    def init_related_routes(cls):
        if(cls.__RELATED_ROUTES == ()):
            cls.__RELATED_ROUTES = (
                {
                    cls.Urls.GET_GUILD_WEBHOOKS : {
                        HttpMethods.GET : {
                            "url_params" : ("guild"),
                            "query_params": None,
                            "payload" : None,
                            "additional_optional_headers": [],
                            "return_type" : list[Webhook]
                            }
                    },
                }
            )
        return cls.__RELATED_ROUTES

    @classmethod
    def get_related_routes(cls):  # class-level access
        return cls.init_related_routes()

    @property
    def RELATED_ROUTES(self):   # instance-level access
        return self.init_related_routes()

    id : str
    name : str
    icon : str | None = None
    icon_hash : str | None = None
    splash : str | None = None
    discovery_splash : str | None = None
    owner : bool | None = None
    owner_id : str
    permissions : str | None = None
    region : str | None = None
    afk_channel_id : str | None = None
    afk_timeout : int
    widget_enabled : bool | None = None
    widget_channel_id : int | None = None
    verification_level : 'VerificationLevels'
    default_message_notifications : 'DefaultMessageNotificationLevels'
    explicit_content_filter	: 'ExplicitContentFilterLevels'
    roles : list['Role']
    emojis : list['Emoji']
    features : list['GuildFeatures']
    mfa_level : 'MFALevels'
    application_id : str | None = None
    system_channel_id : str | None = None
    system_channel_flags : 'SystemChannelFlags'
    rules_channel_id : str | None = None
    max_presences : int | None = None
    max_members : int | None = None
    vanity_url_code : str | None = None
    description : str | None = None
    banner : str | None = None
    premium_tier : 'PremiumTiers'
    premium_subscription_count : int | None = None
    preferred_locale : 'Locales'
    public_updates_channel_id : str | None = None
    max_video_channel_users : int | None = None
    max_stage_video_channel_users : int | None = None
    approximate_member_count : int | None = None
    approximate_presence_count : int | None = None
    welcome_screen : 'WelcomeScreen' | None = None
    nsfw_level : 'GuildNSFWLevels'
    stickers : list['Sticker'] = msgspec.field(default_factory=list)
    premium_progress_bar_enabled : bool
    safety_alerts_channel_id : str | None = None
    incidents_data : 'Incidents' | None = None

class Incidents(msgspec.Struct, kw_only=True):
    """
    Incidents objects represents tracking statistics and controls implemented for abusive events.
    """
    invites_disabled_until : datetime | None = None
    dms_disabled_until : datetime | None = None
    dm_spam_detected_at : datetime | None = None
    raid_detected_at : datetime | None = None

class GuildPreview(msgspec.Struct, kw_only=True):
    """
    Partial information about a guild (server) without needing to be in it.
    """
    id: str
    name: str
    icon: str | None = None
    splash: str | None = None
    discovery_splash: str | None = None
    emojis: list['Emoji'] = msgspec.field(default_factory=list)
    features: list['GuildFeatures'] = msgspec.field(default_factory=list)
    approximate_member_count: int
    approximate_presence_count: int
    description: str | None = None
    stickers: list['Sticker'] = msgspec.field(default_factory=list)

class GuildWidgetSettings(msgspec.Struct, kw_only=True):
    """
    Settings for the Discord widget.
    """
    enabled: bool
    channel_id: str | None = None

class GuildWidget(msgspec.Struct, kw_only=True):
    """
    Guild Widget in Discord is a public-facing snapshot of your server that can be embedded or accessed externally without needing to join the server
    """
    id: str
    name: str
    instant_invite: str | None = None
    channels: list['Channel'] = msgspec.field(default_factory=list)
    members: list['User'] = msgspec.field(default_factory=list)
    presence_count: int

class GuildMember(msgspec.Struct, kw_only=True):
    """
    GuildMember is a User which is a member of a Guild.
    """
    user : 'User' | None = None
    nick : str | None = None
    avatar : str | None = None
    banner : str | None = None
    roles : list[int]
    joined_at : datetime | None = None
    premium_since : datetime | None = None
    deaf : bool
    mute : bool
    flags : int = 0
    pending : bool | None = None
    permissions : str | None = None
    communication_disabled_until : datetime | None = None
    avatar_decoration_data : 'AvatarDecoration' | None = None

class Integration(msgspec.Struct, kw_only=True):
    """
    Integration Object in Discord represents a link between a guild (server) and an external service, such as:

    Twitch (for streamers/subscriber perks)

    YouTube (for channel membership perks)

    Discord Applications (bots with special integrations)

    Guild Subscriptions (for paid memberships)
    """
    id: str
    name: str
    type: str
    enabled: bool
    syncing: bool | None = None
    role_id: str | None = None
    enable_emoticons: bool | None = None
    expire_behavior: 'IntegrationExpireBehaviors' | None = None
    expire_grace_period: int | None = None
    user: "User" | None = None
    account: "IntegrationAccount"
    synced_at: datetime | None = None
    subscriber_count: int | None = None
    revoked: bool | None = None
    application: "IntegrationApplication" | None = None 
    scopes: list['OAuth2Scopes'] = msgspec.field(default_factory=list)

class IntegrationAccount(msgspec.Struct, kw_only=True):
    id: str
    name: str

class IntegrationApplication(msgspec.Struct, kw_only=True):
    id: str
    name: str
    icon: str | None = None
    description: str
    bot: "User" | None = None

class Ban(msgspec.Struct, kw_only=True):
    reason: str | None = None
    user: "User" 

class WelcomeScreen(msgspec.Struct, kw_only=True):
    """
    Welcome Screen object is part of the Guild object and appears for new members when they join a server that has Community features enabled. 
    It usually highlights a few important channels and contains short descriptions and optional emojis to guide new members.
    """
    description : str | None = None
    welcome_channels : list['WelcomeScreenChannel'] 

class WelcomeScreenChannel(msgspec.Struct, kw_only=True):
    """
    WelcomeScreenChannel is part of the WelcomeScreen object.
    """
    channel_id : str
    description : str
    emoji_id : str | None = None
    emoji_name : str | None = None

class GuildOnboarding(msgspec.Struct, kw_only=True):
    guild_id: str
    prompts: list["OnboardingPrompt"] 
    default_channel_ids: list[str]
    enabled: bool
    mode: "OnboardingModes"

class OnboardingPrompt(msgspec.Struct, kw_only=True):
    id: str
    type: "PromptTypes"
    options: list["PromptOption"] 
    title: str
    single_select: bool
    required: bool
    in_onboarding: bool

class PromptOption(msgspec.Struct, kw_only=True):
    id: str
    channel_ids: list[str]
    role_ids: list[str]
    emoji: "Emoji" | None = None
    emoji_id: str | None = None
    emoji_name: str | None = None
    emoji_animated: bool | None = None
    title: str
    description: str | None = None

#Invite-
class InviteTypes(enum.IntEnum):
    GUILD = 0
    GROUP_DM = 1
    FRIEND = 2

class InviteTargetTypes(enum.IntEnum):
    STREAM = 1
    EMBEDDED_APPLICATION = 2

class GuildInviteFlags(enum.IntFlag):
    IS_GUEST_INVITE = 1 << 0

class Invite(msgspec.Struct, kw_only=True):
    """
    Represents a code that when used, adds a user to a guild or group DM channel.
    """
    type: 'InviteTypes'
    code: str
    guild: "Guild" | None = None
    channel: "Channel" | None = None
    inviter: "User" | None = None
    target_type: int | None = None
    target_user: "User" | None = None
    target_application: "Application" | None = None
    approximate_presence_count: int | None = None
    approximate_member_count: int | None = None
    expires_at: datetime | None = None
    stage_instance: "InviteStageInstance" | None = None  # deprecated
    guild_scheduled_event: "GuildScheduledEvent" | None = None
    flags: 'GuildInviteFlags' | None = None

class InviteMetadata(msgspec.Struct, kw_only=True):
    """
    Extra information about an invite, will extend the invite object.
    """
    uses: int
    max_uses: int
    max_age: int
    temporary: bool
    created_at: datetime

class InviteStageInstance(msgspec.Struct, kw_only=True):
    members: list['GuildMember']
    participant_count: int
    speaker_count: int
    topic: str

#Lobby-
class LobbyMemberFlags(enum.IntEnum):
    CAN_LINK_LOBBY = 1 << 0  # user can link a text channel to a lobby

class Lobby(msgspec.Struct, kw_only=True):
    """
    Represents a lobby within Discord. See Managing Lobbies for more information.
    """
    id: str  # snowflake
    application_id: str  # snowflake
    metadata: dict[str, str] = msgspec.field(default_factory=dict)
    members: list['LobbyMember']
    linked_channel: 'Channel' | None = None

class LobbyMember(msgspec.Struct, kw_only=True):
    """
    Represents a member of a lobby, including optional metadata and flags
    """
    id: str  # snowflake
    metadata: dict[str, str] = msgspec.field(default_factory=dict)
    flags: int | None = None

#Message-
class MessageTypes(msgspec.Struct, kw_only=True):
    DEFAULT = 0
    RECIPIENT_ADD = 1
    RECIPIENT_REMOVE = 2
    CALL = 3
    CHANNEL_NAME_CHANGE = 4
    CHANNEL_ICON_CHANGE = 5
    CHANNEL_PINNED_MESSAGE = 6
    USER_JOIN = 7
    GUILD_BOOST = 8
    GUILD_BOOST_TIER_1 = 9
    GUILD_BOOST_TIER_2 = 10
    GUILD_BOOST_TIER_3	 = 11
    CHANNEL_FOLLOW_ADD = 12
    GUILD_DISCOVERY_DISQUALIFIED = 14
    GUILD_DISCOVERY_REQUALIFIED = 15
    GUILD_DISCOVERY_GRACE_PERIOD_INITIAL_WARNING = 16
    GUILD_DISCOVERY_GRACE_PERIOD_FINAL_WARNING = 17
    THREAD_CREATED = 18
    REPLY = 19
    CHAT_INPUT_COMMAND = 20
    THREAD_STARTER_MESSAGE = 21
    GUILD_INVITE_REMINDER = 22
    CONTEXT_MENU_COMMAND = 23
    AUTO_MODERATION_ACTION = 24
    ROLE_SUBSCRIPTION_PURCHASE = 25
    INTERACTION_PREMIUM_UPSELL = 26
    STAGE_START = 27
    STAGE_END = 28
    STAGE_SPEAKER = 29
    STAGE_TOPIC = 31
    GUILD_APPLICATION_PREMIUM_SUBSCRIPTION = 32
    GUILD_INCIDENT_ALERT_MODE_ENABLED = 36
    GUILD_INCIDENT_ALERT_MODE_DISABLED = 37
    GUILD_INCIDENT_REPORT_RAID = 38
    GUILD_INCIDENT_REPORT_FALSE_ALARM = 39
    PURCHASE_NOTIFICATION = 44
    POLL_RESULT = 46

class MessageActivityTypes(enum.IntEnum):
    JOIN = 1
    SPECTATE = 2
    LISTEN = 3
    JOIN_REQUEST = 5

class MessageFlags(enum.IntEnum):
    CROSSPOSTED	= 1 << 0
    IS_CROSSPOST = 1 << 1
    SUPPRESS_EMBEDS = 1 << 2
    SOURCE_MESSAGE_DELETED = 1 << 3
    URGENT = 1 << 4
    HAS_THREAD = 1 << 5
    EPHEMERAL = 1 << 6
    LOADING = 1 << 7
    FAILED_TO_MENTION_SOME_ROLES_IN_THREAD = 1 << 8
    SUPPRESS_NOTIFICATIONS = 1 << 12
    IS_VOICE_MESSAGE = 1 << 13
    HAS_SNAPSHOT = 1 << 14
    IS_COMPONENTS_V2 = 1 << 15

class MessageReferenceTypes(enum.IntEnum):
    DEFAULT = 0
    FORWARD = 1

class EmbedTypes(enum.StrEnum):
    RICH = "rich"
    IMAGE = "image"
    VIDEO = "video"
    GIFV = "gifv"
    ARTICLE = "article"
    LINK = "link"
    POLL_RESULT = "poll_result"

class AttachmentFlags(enum.IntFlag):
    IS_REMIX = 1 << 2

class AllowedMentionTypes(enum.StrEnum):
    ROLES = "roles"          # Controls role mentions
    USERS = "users"          # Controls user mentions
    EVERYONE = "everyone"    # Controls @everyone and @here mentions

class Message(msgspec.Struct, kw_only=True):
    """
    Represents a message sent in a channel within Discord.
    """
    id : str
    channel_id : str
    author : 'User'
    content : str
    timestamp : datetime
    edited_timestamp : datetime | None = None
    tts : bool
    mention_everyone : bool
    mentions : list['User']
    mention_roles : list['Role']
    mention_channels : 'ChannelMention' | None = None
    attachments : 'Attachment'
    embeds : list['Embed']
    reactions : list['Reaction'] = msgspec.field(default_factory=list)
    nonce : int | str | None = None
    pinned : bool
    webhook_id : str | None = None
    type : 'MessageTypes'
    activity : 'MessageActivity' | None = None
    application : 'Application' | None = None
    application_id : str | None = None
    flags : int | None = None
    message_reference : 'MessageReference' | None = None
    message_snapshots : list['MessageSnapshot'] = msgspec.field(default_factory=list)
    referenced_message : 'Message' | None = None
    interaction_metadata : 'MessageInteractionMetadata' | None = None
    interaction : 'MessageInteraction' | None = None
    thread : 'Channel' | None = None
    components : list['Component'] = msgspec.field(default_factory=list)
    sticker_items : list['StickerItem'] = msgspec.field(default_factory=list)
    stickers : list['Sticker'] = msgspec.field(default_factory=list)
    position : int | None = None
    role_subscription_data : 'RoleSubscriptionData' | None = None
    resolved : 'Resolved' | None = None
    poll : 'Poll' | None = None
    call : 'MessageCall' | None = None

class MessageActivity(msgspec.Struct, kw_only=True):
    """
    Message Activity is a small metadata object that can be attached to a message when it relates to certain platform events.
    """
    type : 'MessageActivityTypes'
    party_id : str | None = None

class MessageInteractionMetadata(msgspec.Struct, kw_only=True):
    """
    Message Interaction Metadata represents metadata about the interaction, including the source of the interaction and relevant server and user IDs.
    One of Application Command Interaction Metadata, Message Component Interaction Metadata, or Modal Submit Interaction Metadata.
    """
    id : str
    type : 'InteractionTypes'
    user : 'User'
    authorizing_integration_owners : dict['ApplicationIntegrationTypes', int]
    original_response_message_id : str | None = None
    target_user : 'User' | None = None
    target_message_id : str | None = None
    interacted_message_id : str | None = None
    triggering_interaction_metadata	 : 'MessageInteractionMetadata' | None = None

class MessageCall(msgspec.Struct, kw_only=True):
    """
    MessageCall represents a voice or video call event that occurred in a private channel (either a direct message (DM) or group DM).
    """
    participants : list[str]
    ended_timestamp : datetime | None = None

class MessageReference(msgspec.Struct, kw_only=True):
    """
    Message Reference is part of the message structure that indicates a message is a reply to another message
    """
    type : 'MessageReferenceTypes' | None = None
    message_id : str | None = None
    channel_id : str | None = None
    guild_id : str | None = None
    fail_if_not_exists : bool | None = None

class MessageSnapshot(msgspec.Struct, kw_only=True):
    """
    Message Snapshot Object represents a lightweight, static copy of a message captured when a message is referenced or replied to.
    """
    message : 'Message' | None = None

class Reaction(msgspec.Struct, kw_only=True):
    """
    Reaction object represents a reaction (emoji) that a user has added to a message.
    """
    count : int
    count_details : 'ReactionCountDetails'
    me : bool
    me_burst : bool
    emoji : 'Emoji'
    burst_colors : list[str]

class ReactionCountDetails(msgspec.Struct, kw_only=True):
    """
    Reaction count details object contains a breakdown of normal and super reaction counts for the associated emoji.
    """
    burst : int
    normal : int

class Embed(msgspec.Struct, kw_only=True):
    """
    Embed is a rich structured content message format in discord.
    """
    title : str | None = None
    type : 'EmbedTypes' | None = None
    description : str | None = None
    url : str | None = None
    timestamp : datetime | None = None
    color : int | None = None
    footer : 'EmbedFooter' | None = None
    image : 'EmbedImage' | None = None
    thumbnail : 'EmbedThumbnail' | None = None
    video : 'EmbedVideo' | None = None
    provider : 'EmbedProvider' | None = None
    author : 'EmbedAuthor' | None = None
    fields : list['EmbedField'] = msgspec.field(default_factory=list)

class EmbedThumbnail(msgspec.Struct, kw_only=True):
    """
    EmbedThumbnail is an object part of the Embed object .
    """
    url : str
    proxy_url : str | None = None 
    height : int | None = None 
    width : int | None = None 

class EmbedVideo(msgspec.Struct, kw_only=True):
    """
    EmbedVideo is an object part of the Embed object .
    """
    url : str | None = None 
    proxy_url : str | None = None 
    height : int | None = None 
    width : int | None = None 

class EmbedImage(msgspec.Struct, kw_only=True):
    """
    EmbedImage is an object part of the Embed object .
    """
    url : str
    proxy_url : str | None = None 
    height : int | None = None 
    width : int | None = None 

class EmbedProvider(msgspec.Struct, kw_only=True):
    """
    EmbedProvider is an object part of the Embed object .
    """
    name : str | None = None
    url : str | None = None

class EmbedAuthor(msgspec.Struct, kw_only=True):
    """
    EmbedAuthor is an object part of the Embed object.
    """
    name : str
    url : str | None = None
    icon_url : str | None = None
    proxy_icon_url : str | None = None

class EmbedFooter(msgspec.Struct, kw_only=True):
    """
    EmbedFooter is an object part of the Embed object .
    """
    text : str
    icon_url : str | None = None 
    proxy_icon_url : str | None = None 

class EmbedField(msgspec.Struct, kw_only=True):
    """
    EmbedField is an object part of the Embed object.
    """
    name : str
    value : str
    inline : bool | None = None

class Attachment(msgspec.Struct, kw_only=True):
    """
    Attachment object represents files like images, videos or documents which are attached to messages.
    """
    id : str
    filename : str
    title : str | None = None
    description : str | None = None
    content_type : str | None = None
    size : int
    url : str
    proxy_url : str
    height : int | None = None
    width : int | None = None
    ephemeral : bool | None = None
    duration_secs : float | None = None
    waveform : str | None = None
    flags : int | None = None

class ChannelMention(msgspec.Struct, kw_only=True):
    id : str
    guild_id : str
    type : 'ChannelTypes'
    name : str

class AllowedMentions(msgspec.Struct, kw_only=True):
    """
    Represents the allowed mentions object for controlling which mentions 
    (users, roles, @everyone) trigger notifications in a message.
    """
    parse: list['AllowedMentionTypes'] = msgspec.field(default_factory=list)  # List of mention types to parse from the content
    roles: list[str] = msgspec.field(default_factory=list)                    # Role IDs allowed to be mentioned
    users: list[str] = msgspec.field(default_factory=list)                    # User IDs allowed to be mentioned
    replied_user: bool | None = None                  # Whether to mention the author in replies

class RoleSubscriptionData(msgspec.Struct, kw_only=True):
    """
    Role Subscription Data represents metadata about a user's paid role subscription.
    Typically used when receiving interaction events (like messages or webhook events) related to subscriptions to premium roles in a server.
    """
    role_subscription_listing_id : str
    tier_name : str
    total_months_subscribed : int
    is_renewal : bool

class MessagePin(msgspec.Struct, kw_only=True):
    """
    Represents a pinned message object.
    """
    pinned_at: datetime       # The time the message was pinned
    message: 'Message'        # The pinned message object

#Poll-
class PollLayoutTypes(enum.IntEnum):
    DEFAULT = 1  # The default layout type

class Poll(msgspec.Struct, kw_only=True):
    """
    The poll object has a lot of levels and nested structures. It was also designed to support future extensibilit
    """
    question : 'PollMedia'
    answers	: list['PollAnswer']
    expiry : datetime | None = None
    allow_multiselect : bool
    layout_type : 'PollLayoutTypes'
    results : 'PollResults' | None = None

class PollCreateRequest(msgspec.Struct, kw_only=True):
    """
    Request object for creating a poll. Similar to the main poll object but
    includes `duration` instead of `expiry`.
    """
    question: 'PollMedia'                        # The question of the poll (text only)
    answers: list['PollAnswer']                  # Available answers (up to 10)
    duration: int | None = None                   # Duration in hours (max 32 days, default 24)
    allow_multiselect: bool | None = None         # Whether multiple answers can be selected
    layout_type: 'PollLayoutTypes' | None = None                # Layout type of the poll (default is DEFAULT)

class PollMedia(msgspec.Struct, kw_only=True):
    """
    Poll media object is a common object that backs both the question and answers. 
    The intention is that it allows discord to extensibly add new ways to display things in the future. For now, question only supports text, while answers can have an optional emoji.
    """
    text : str | None = None
    emoji : 'Emoji' | None = None

class PollAnswer(msgspec.Struct, kw_only=True):
    """
    PollAnswer is the an answer to a Poll.
    """
    answer_id : int
    poll_media : 'PollMedia'

class PollResults(msgspec.Struct, kw_only=True):
    """
    PollResults represents the counts for each answer and a final confirmation on the count.
    """
    is_finalized : bool
    answer_counts : list['PollAnswerCount']

class PollAnswerCount(msgspec.Struct, kw_only=True):
    """
    Poll Answer Count counts the number of votes for an answer.
    """
    id : int
    count : int
    me_voted : bool

#SKU-
class SKUTypes(enum.IntEnum):
    DURABLE = 2               # Durable one-time purchase
    CONSUMABLE = 3            # Consumable one-time purchase
    SUBSCRIPTION = 5          # Recurring subscription
    SUBSCRIPTION_GROUP = 6    # System-generated group for each subscription SKU

class SKUFlags(enum.IntFlag):
    AVAILABLE = 1 << 2              # SKU is available for purchase
    GUILD_SUBSCRIPTION = 1 << 7     # Recurring SKU for a single server
    USER_SUBSCRIPTION = 1 << 8      # Recurring SKU for an individual user

class SKU(msgspec.Struct, kw_only=True):
    """
    SKU represents a premium offering available to a user or guild in your application.
    """
    id: str  # snowflake
    type: 'SKUTypes'
    application_id: str  # snowflake
    name: str
    slug: str
    flags: 'SKUFlags'

#SoundBoard-
class SoundboardSound(msgspec.Struct, kw_only=True):
    """Represents a soundboard sound in Discord."""
    name: str                                   # The name of this sound
    sound_id: str                               # The id of this sound (snowflake)
    volume: float                               # The volume of this sound, from 0 to 1
    emoji_id: str | None = None                 # The id of this sound's custom emoji (snowflake)
    emoji_name: str | None = None               # The unicode character of this sound's standard emoji
    guild_id: str | None = None                 # The id of the guild this sound is in (snowflake)
    available: bool                             # Whether this sound can be used
    user: "User" | None = None                  # The user who created this sound

#StageInstance-
class PrivacyLevels(enum.IntEnum):
    PUBLIC = 1       # The Stage instance is visible publicly (deprecated)
    GUILD_ONLY = 2   # The Stage instance is visible to only guild members

class StageInstance(msgspec.Struct, kw_only=True):
    """Represents a Stage instance in Discord."""
    id: str                                 # The id of this Stage instance (snowflake)
    guild_id: str                           # The guild id of the associated Stage channel (snowflake)
    channel_id: str                         # The id of the associated Stage channel (snowflake)
    topic: str                              # The topic of the Stage instance (1-120 characters)
    privacy_level: 'PrivacyLevels'                    # The privacy level of the Stage instance
    discoverable_disabled: bool             # Whether or not Stage Discovery is disabled (deprecated)
    guild_scheduled_event_id: str | None = None  # The id of the scheduled event for this Stage instance (snowflake)

#Sticker
class StickerTypes(enum.IntEnum):
    STANDARD = 1  # an official sticker in a pack
    GUILD = 2     # a sticker uploaded to a guild for the guild's members

class StickerFormats(enum.IntEnum):
    PNG = 1
    APNG = 2
    LOTTIE = 3
    GIF = 4

class Sticker(msgspec.Struct, kw_only=True, kw_only=True):
    """
    Sticker objects represents an animated or custom emoji in discord.
    """
    id: str  # snowflake - id of the sticker
    pack_id: str | None = None  # snowflake - id of the pack the sticker is from (standard stickers)
    name: str  # name of the sticker
    description: str | None = None  # description of the sticker
    tags: str  # autocomplete/suggestion tags for the sticker (max 200 characters)
    type: 'StickerTypes'  # type of sticker
    format_type: 'StickerFormats'  # type of sticker format
    available: bool | None = None  # whether this guild sticker can be used
    guild_id: str | None = None  # snowflake - id of the guild that owns the sticker
    user: "User" | None = None  # user object - the user who uploaded the sticker
    sort_value: int | None = None  # standard sticker's sort order within its pack

class StickerItem(msgspec.Struct, kw_only=True):
    """
    Sticker Item represents the smallest amount of data required to render a sticker. A partial sticker object.
    """
    id : str
    name : str
    format_type : 'StickerFormats'

class StickerPack(msgspec.Struct, kw_only=True):
    """
    Represents a pack of standard stickers.
    """
    id: str
    stickers: list['Sticker']
    name: str
    sku_id: str
    cover_sticker_id: str | None = None
    description: str
    banner_asset_id: str | None = None

#Subscription-
class SubscriptionStatus(enum.IntEnum):
    ACTIVE = 0      # Subscription is active and scheduled to renew.
    ENDING = 1      # Subscription is active but will not renew.
    INACTIVE = 2    # Subscription is inactive and not being charged.

class Subscription(msgspec.Struct, kw_only=True):
    """
    Represents a subscription object.
    """
    id: str
    user_id: str
    sku_ids: list[str]
    entitlement_ids: list[str]
    renewal_sku_ids: list[str] = msgspec.field(default_factory=list)
    current_period_start: datetime
    current_period_end: datetime
    status: 'SubscriptionStatus'
    canceled_at: datetime | None = None
    country: str | None = None

#User-
class UserFlags(enum.IntFlag):
    STAFF = 1 << 0
    PARTNER = 1 << 1
    HYPESQUAD = 1 << 2
    BUG_HUNTER_LEVEL_1 = 1 << 3
    HYPESQUAD_ONLINE_HOUSE_1 = 1 << 6
    HYPESQUAD_ONLINE_HOUSE_2 = 1 << 7
    HYPESQUAD_ONLINE_HOUSE_3 = 1 << 8
    PREMIUM_EARLY_SUPPORTER = 1 << 9
    TEAM_PSEUDO_USER = 1 << 10
    BUG_HUNTER_LEVEL_2 = 1 << 14
    VERIFIED_BOT = 1 << 16
    VERIFIED_DEVELOPER = 1 << 17
    CERTIFIED_MODERATOR = 1 << 18
    BOT_HTTP_INTERACTIONS = 1 << 19
    ACTIVE_DEVELOPER = 1 << 22

class PremiumTypes(enum.IntEnum):
    NONE = 0
    NITRO_CLASSIC = 1
    NITRO = 2
    NITRO_BASIC = 3

class ConnectionServices(enum.StrEnum):
    AMAZON_MUSIC = "amazon-music"
    BATTLENET = "battlenet"
    BUNGIE = "bungie"
    BLUESKY = "bluesky"
    CRUNCHYROLL = "crunchyroll"
    DOMAIN = "domain"
    EBAY = "ebay"
    EPICGAMES = "epicgames"
    FACEBOOK = "facebook"
    GITHUB = "github"
    INSTAGRAM = "instagram"
    LEAGUEOFLEGENDS = "leagueoflegends"
    MASTODON = "mastodon"
    PAYPAL = "paypal"
    PLAYSTATION = "playstation"
    REDDIT = "reddit"
    RIOTGAMES = "riotgames"
    ROBLOX = "roblox"
    SPOTIFY = "spotify"
    SKYPE = "skype"
    STEAM = "steam"
    TIKTOK = "tiktok"
    TWITCH = "twitch"
    TWITTER = "twitter"
    XBOX = "xbox"
    YOUTUBE = "youtube"

class VisibilityTypes(enum.IntEnum):
    NONE = 0          # Invisible to everyone except the user themselves
    EVERYONE = 1      # Visible to everyone

class User(msgspec.Struct, kw_only=True):
    """
    User represents a User on the discord application.
    """
    id : str
    username : str
    discriminator : str
    global_name : str | None = None 
    avatar : str | None = None 
    bot : bool | None = None 
    system : bool | None = None 
    mfa_enabled : bool | None = None 
    banner : str | None = None 
    accent_color : int | None = None 
    locale : 'Locales' | None = None 
    verified : bool | None = None 
    email : str | None = None 
    flags : 'UserFlags' | None = None 
    premium_type : 'PremiumTypes' | None = None 
    public_flags : 'UserFlags' | None = None 
    avatar_decoration_data : 'AvatarDecoration' | None = None 
    collectibles : 'Collectible' | None = None 
    primary_guild : 'UserPrimaryGuild' | None = None 

class AvatarDecoration(msgspec.Struct, kw_only=True):
    """
    The data for the user's avatar decoration.
    """
    asset : str 
    sku_id : str 

class Collectible(msgspec.Struct, kw_only=True):
    """
    The collectibles the user has, excluding Avatar Decorations and Profile Effects.
    """
    nameplate : 'Nameplate' | None = None

class Nameplate(msgspec.Struct, kw_only=True):
    """
    The nameplate the user has.
    """
    sku_id : str
    asset : str
    label : str
    palette : str

class UserPrimaryGuild(msgspec.Struct, kw_only=True):
    """
    User Primary Guild Object in Discord represents information about a user's primary server identity, especially in contexts where a user chooses to represent a specific server (guild) across Discord using a server tag and badge.
    """
    identity_guild_id : str | None
    identity_enabled : bool | None
    tag : str | None
    badge : str | None

class Connection(msgspec.Struct, kw_only=True):
    """
    Represents a user's connected account (e.g., Twitch, Steam, etc.).
    """
    id: str
    name: str
    type: 'ConnectionServices'
    revoked: bool | None = None
    integrations: list['Integration'] = msgspec.field(default_factory=list)  # Replace Any with a specific Integration type if you define one
    verified: bool
    friend_sync: bool
    show_activity: bool
    two_way_link: bool
    visibility: 'VisibilityTypes'

class ApplicationRoleConnection(msgspec.Struct, kw_only=True):
    """
    The role connection object that an application has attached to a user.
    Used to update the custom linked role metadata structure already defined for a user.
    """
    platform_name: str | None = None
    platform_username: str | None = None
    metadata: dict[str, str]

#Voice-
class VoiceState(msgspec.Struct, kw_only=True):
    """
    Represents a user's voice connection status in a guild.
    """
    guild_id: str | None = None
    channel_id: str | None = None
    user_id: str
    member: "GuildMember" | None = None
    session_id: str
    deaf: bool
    mute: bool
    self_deaf: bool
    self_mute: bool
    self_stream: bool | None = None
    self_video: bool
    suppress: bool
    request_to_speak_timestamp: datetime | None = None

class VoiceRegion(msgspec.Struct, kw_only=True):
    """
    Represents a Discord voice region.
    """
    id: str
    name: str
    optimal: bool
    deprecated: bool
    custom: bool

#Webhook-
class WebhookTypes(enum.IntEnum):
    Incoming = 1
    ChannelFollower = 2
    Application = 3

class WebhookEventTypes(enum.StrEnum):
    ApplicationAuthorized = "APPLICATION_AUTHORIZED"
    ApplicationDeauthorized = "APPLICATION_DEAUTHORIZED"
    EntitlementCreate = "ENTITLEMENT_CREATE"
    QuestUserEnrollment = "QUEST_USER_ENROLLMENT"

class Webhook(msgspec.Struct, kw_only=True):
    class WebhookUrls(enum.StrEnum):

        #These URL's require only the Webhook class alone to resolve
        GET_WEBHOOK = "/webhooks/{webhook.id}"
        GET_WEBHOOK_WITH_TOKEN = "/webhooks/{webhook.id}/{webhook.token}"
        MODIFY_WEBHOOK = GET_WEBHOOK
        MODIFY_WEBHOOK_WITH_TOKEN = GET_WEBHOOK_WITH_TOKEN
        DELETE_WEBHOOK = GET_WEBHOOK
        DELETE_WEBHOOK_WITH_TOKEN = GET_WEBHOOK_WITH_TOKEN
        EXECUTE_WEBHOOK = GET_WEBHOOK_WITH_TOKEN #returns Message

        #These URL's do not have routes, they are generated using the APX Discord Support
        EXECUTE_SLACK_COMPATIBLE_WEBHOOK = "/webhooks/{webhook.id}/{webhook.token}/slack"
        EXECUTE_GITHUB_COMPATIBLE_WEBHOOK = "/webhooks/{webhook.id}/{webhook.token}/github"

        #These URL's require more than the Webhook msgspec class to resolve
        GET_WEBHOOK_MESSAGE = "/webhooks/{webhook.id}/{webhook.token}/messages/{message.id}" #returns Message
        EDIT_WEBHOOK_MESSAGE = GET_WEBHOOK_MESSAGE #returns Message
        DELETE_WEBHOOK_MESSAGE = GET_WEBHOOK_MESSAGE

    #QUERY PARAMS FOR WEBHOOK ENDPOINTS
    class ExecuteWebhookQueryParams(msgspec.Struct, kw_only=True, omit_defaults=True):
        """
        Query string parameters for the Execute Webhook endpoint.
        """
        wait: bool | None = None               # waits for server confirmation of message send
        thread_id: str | None = None           # snowflake: target thread ID
        with_components: bool | None = None    # whether to respect components in the request

    class GetWebhookMessageQueryParams(msgspec.Struct, kw_only=True, omit_defaults=True):
        """
        Query string parameters for GET /webhooks/{webhook.id}/{token}/messages/{message.id}
        """
        thread_id: str | None = None  # Snowflake ID of the thread the message is in

    class EditWebhookMessageQueryParams(msgspec.Struct, kw_only=True, omit_defaults=True):
        thread_id: str | None = None  # snowflake id as string
        with_components: bool | None = None

    class DeleteWebhookMessageQueryParams(msgspec.Struct, kw_only=True, omit_defaults=True):
        """
        Query parameters for deleting a webhook message.
        """
        thread_id: str | None = None  # ID of the thread the message is in (snowflake)

    #JSON PARAMS FOR WEBHOOK ENDPOINTS
    class ModifyWebhookJSONParams(msgspec.Struct, kw_only=True, omit_defaults=True):
        """
        JSON body for PATCH /webhooks/{webhook.id}
        """
        name: str | None = None
        avatar: str | None = None  # image data (base64-encoded)
        channel_id: str | None = None  # snowflake (channel ID)

    class ModifyWebhookWithTokenJSONParams(msgspec.Struct, kw_only=True):
        """
        JSON parameters for creating a Discord webhook.
        """
        name: str                   # required: 1-80 characters
        avatar: str | None = None   # optional: base64 image data

    class ExecuteWebhookJSONParams(msgspec.Struct, kw_only=True, omit_defaults=True):
        """
        JSON/Form body parameters for the Execute Webhook endpoint.
        """
        # Core fields (must provide one of: content, embeds, components, file, poll)
        content: str | None = None
        username: str | None = None
        avatar_url: str | None = None
        tts: bool | None = None
        embeds: list["Embed"] | None = None
        allowed_mentions: "AllowedMentions" | None = None
        components: list["Component"] | None = None
        file_locations: list[str] | None = None
        attachments: list["Attachment"] | None = None
        flags: int | None = None
        # Forum/media specific
        thread_name: str | None = None
        applied_tags: list[str] | None = None # list of snowflakes
        # Special cases
        poll: "Poll" | None = None

    class EditWebhookMessageJSONParams(msgspec.Struct, kw_only=True, omit_defaults=True):
        content: str | None = None
        embeds: list["Embed"] | None = None
        flags: int | None = None  # class MessageFlags
        allowed_mentions: "AllowedMentions" | None = None
        components: list["Component"] | None = None
        file_locations: list[str] | None = None
        attachments: list["Attachment"] | None = None
        poll: "Poll" | None = None

    GetWebhookMessageQueryParams = GetWebhookMessageQueryParams

    __RELATED_ROUTES : ClassVar[tuple] = ()

    @classmethod
    def init_related_routes(cls):
        if(cls.__RELATED_ROUTES == ()):
            cls.__RELATED_ROUTES = (
                {
                    cls.Urls.GET_WEBHOOK : {
                        HttpMethods.GET : {
                            "url_params": ("webhook"),
                            "query_params": None,
                            "payload" : None,
                            "additional_optional_headers": [],
                            "return_type" : Webhook
                            }
                    },
                    cls.Urls.GET_WEBHOOK_WITH_TOKEN : {
                        HttpMethods.GET : {
                            "url_params": ("webhook"),
                            "query_params": None,
                            "payload" : None,
                            "additional_optional_headers": [],
                            "return_type" : Webhook
                            }
                    },
                    cls.Urls.MODIFY_WEBHOOK : {
                        HttpMethods.PATCH : {
                            "url_params": ("webhook"),
                            "query_params": None,
                            "payload" : cls.ModifyWebhookJSONParams,
                            "additional_optional_headers": ["X-Audit-Log-Reason"],
                            "return_type" : Webhook
                            }
                    },
                    cls.Urls.MODIFY_WEBHOOK_WITH_TOKEN : {
                        HttpMethods.PATCH : {
                            "url_params": ("webhook"),
                            "query_params": None,
                            "payload" : cls.ModifyWebhookWithTokenJSONParams,
                            "additional_optional_headers": ["X-Audit-Log-Reason"],
                            "return_type" : Webhook
                            }
                    },
                    cls.Urls.DELETE_WEBHOOK : {
                        HttpMethods.DELETE : {
                            "url_params": ("webhook"),
                            "query_params": None,
                            "payload" : None,
                            "additional_optional_headers": ["X-Audit-Log-Reason"],
                            "return_type" : 204
                            }
                    },
                    cls.Urls.DELETE_WEBHOOK_WITH_TOKEN: {
                        HttpMethods.DELETE: {
                            "url_params": ("webhook"),
                            "query_params": None,
                            "payload": None,
                            "additional_optional_headers": ["X-Audit-Log-Reason"],
                            "return_type": 204
                            }
                    },
                    cls.Urls.EXECUTE_WEBHOOK: {
                        HttpMethods.POST: {
                            "url_params": ("webhook"),
                            "query_params": ExecuteWebhookQueryParams,
                            "payload": ExecuteWebhookJSONParams,
                            "additional_optional_headers": [],
                            "return_type": Message | 204
                            }
                    },
                    cls.Urls.GET_WEBHOOK_MESSAGE: {
                        HttpMethods.GET: {
                            "url_params": ("webhook", "message"),
                            "query_params": GetWebhookMessageQueryParams,
                            "payload": None,
                            "additional_optional_headers": [],
                            "return_type": Message
                            }
                    },
                    cls.Urls.EDIT_WEBHOOK_MESSAGE: {
                        HttpMethods.PATCH: {
                            "url_params": ("webhook", "message"),
                            "query_params": EditWebhookMessageQueryParams,
                            "payload": EditWebhookMessageJSONParams,
                            "additional_optional_headers": [],
                            "return_type": Message
                            }
                    },
                    cls.Urls.DELETE_WEBHOOK_MESSAGE: {
                        HttpMethods.DELETE: {
                            "url_params": ("webhook", "message"),
                            "query_params": DeleteWebhookMessageQueryParams,
                            "payload": None,
                            "additional_optional_headers": [],
                            "return_type": 204
                            }
                    },
                }
            )
        return cls.__RELATED_ROUTES

    @classmethod
    def get_related_routes(cls):  # class-level access
        return cls.init_related_routes()

    @property
    def RELATED_ROUTES(self):   # instance-level access
        return self.init_related_routes()

    id: str  # snowflake, webhook id
    type: 'WebhookTypes'
    guild_id: str | None = None  # snowflake
    channel_id: str | None = None  # snowflake
    user: 'User' | None = None
    name: str | None = None
    avatar: str | None = None
    token: str | None = None
    application_id: str | None = None  # snowflake
    source_guild: 'Guild' | None = None
    source_channel: 'Channel' | None = None
    url: str | None = None

############### End of Discord Resources data models

####Topics
#Certified devices-
class DeviceTypes(enum.StrEnum):
    AUDIO_INPUT = "audioinput"
    AUDIO_OUTPUT = "audiooutput"
    VIDEO_INPUT = "videoinput"

class VoiceConnectionState(enum.StrEnum):
    DISCONNECTED = "DISCONNECTED"          # TCP disconnected
    AWAITING_ENDPOINT = "AWAITING_ENDPOINT"  # Waiting for voice endpoint
    AUTHENTICATING = "AUTHENTICATING"      # TCP authenticating
    CONNECTING = "CONNECTING"              # TCP connecting
    CONNECTED = "CONNECTED"                # TCP connected
    VOICE_DISCONNECTED = "VOICE_DISCONNECTED"  # TCP connected, Voice disconnected
    VOICE_CONNECTING = "VOICE_CONNECTING"      # TCP connected, Voice connecting
    VOICE_CONNECTED = "VOICE_CONNECTED"        # TCP connected, Voice connected
    NO_ROUTE = "NO_ROUTE"                  # No route to host
    ICE_CHECKING = "ICE_CHECKING"          # WebRTC ice checking

class Device(msgspec.Struct, kw_only=True):
    """
    Represents a hardware device (e.g., microphone, speakers) in Discord.
    """

    type: 'DeviceTypes'  # The type of device (input, output, etc.)
    id: str  # The device's Windows UUID
    vendor: 'Vendor'  # Hardware vendor information
    model: 'Model'  # Model of the device
    related: list[str]  # UUIDs of related devices

    # Optional native processing features
    echo_cancellation: bool | None = None  # Native echo cancellation enabled
    noise_suppression: bool | None = None  # Native noise suppression enabled
    automatic_gain_control: bool | None = None  # Native AGC enabled
    hardware_mute: bool | None = None  # True if device is hardware muted

class Vendor(msgspec.Struct, kw_only=True):
    name: str
    url: str

class Model(msgspec.Struct, kw_only=True):
    name: str
    url: str

#OAuth2-
class OAuth2Scopes(enum.StrEnum):
    activities_read = "activities.read"
    activities_write = "activities.write"
    applications_builds_read = "applications.builds.read"
    applications_builds_upload = "applications.builds.upload"
    applications_commands = "applications.commands"
    applications_commands_update = "applications.commands.update"
    applications_commands_permissions_update = "applications.commands.permissions.update"
    applications_entitlements = "applications.entitlements"
    applications_store_update = "applications.store.update"
    bot = "bot"
    connections = "connections"
    dm_channels_read = "dm_channels.read"
    email = "email"
    gdm_join = "gdm.join"
    guilds = "guilds"
    guilds_join = "guilds.join"
    guilds_members_read = "guilds.members.read"
    identify = "identify"
    messages_read = "messages.read"
    relationships_read = "relationships.read"
    role_connections_write = "role_connections.write"
    rpc = "rpc"
    rpc_activities_write = "rpc.activities.write"
    rpc_notifications_read = "rpc.notifications.read"
    rpc_voice_read = "rpc.voice.read"
    rpc_voice_write = "rpc.voice.write"
    voice = "voice"
    webhook_incoming = "webhook.incoming"

#Opcodes and statuses-
class GatewayOpcodes(enum.IntEnum):
    DISPATCH = 0                 # Receive: An event was dispatched.
    HEARTBEAT = 1                # Send/Receive: Fired periodically by the client to keep the connection alive.
    IDENTIFY = 2                 # Send: Starts a new session during the initial handshake.
    PRESENCE_UPDATE = 3          # Send: Update the client's presence.
    VOICE_STATE_UPDATE = 4       # Send: Used to join/leave or move between voice channels.
    RESUME = 6                   # Send: Resume a previous session that was disconnected.
    RECONNECT = 7                # Receive: You should attempt to reconnect and resume immediately.
    REQUEST_GUILD_MEMBERS = 8    # Send: Request information about offline guild members in a large guild.
    INVALID_SESSION = 9          # Receive: The session has been invalidated. You should reconnect and identify/resume accordingly.
    HELLO = 10                   # Receive: Sent immediately after connecting, contains the heartbeat_interval to use.
    HEARTBEAT_ACK = 11           # Receive: Sent in response to receiving a heartbeat to acknowledge that it has been received.
    REQUEST_SOUNDBOARD_SOUNDS = 31  # Send: Request information about soundboard sounds in a set of guilds.

class GatewayCloseEventCodes(enum.IntEnum):
    UNKNOWN_ERROR = 4000            # Description: Unknown error; Explanation: We're not sure what went wrong. Try reconnecting?; Reconnect: True
    UNKNOWN_OPCODE = 4001           # Description: Unknown opcode; Explanation: You sent an invalid Gateway opcode or an invalid payload for an opcode. Don't do that!; Reconnect: True
    DECODE_ERROR = 4002             # Description: Decode error; Explanation: You sent an invalid payload to Discord. Don't do that!; Reconnect: True
    NOT_AUTHENTICATED = 4003        # Description: Not authenticated; Explanation: You sent us a payload prior to identifying, or this session has been invalidated.; Reconnect: True
    AUTHENTICATION_FAILED = 4004    # Description: Authentication failed; Explanation: The account token sent with your identify payload is incorrect.; Reconnect: False
    ALREADY_AUTHENTICATED = 4005    # Description: Already authenticated; Explanation: You sent more than one identify payload. Don't do that!; Reconnect: True
    INVALID_SEQ = 4007              # Description: Invalid seq; Explanation: The sequence sent when resuming the session was invalid. Reconnect and start a new session.; Reconnect: True
    RATE_LIMITED = 4008             # Description: Rate limited; Explanation: You're sending payloads to us too quickly. Slow it down! You will be disconnected on receiving this.; Reconnect: True
    SESSION_TIMED_OUT = 4009        # Description: Session timed out; Explanation: Your session timed out. Reconnect and start a new one.; Reconnect: True
    INVALID_SHARD = 4010            # Description: Invalid shard; Explanation: You sent us an invalid shard when identifying.; Reconnect: False
    SHARDING_REQUIRED = 4011        # Description: Sharding required; Explanation: The session would have handled too many guilds - you are required to shard your connection in order to connect.; Reconnect: False
    INVALID_API_VERSION = 4012      # Description: Invalid API version; Explanation: You sent an invalid version for the gateway.; Reconnect: False
    INVALID_INTENTS = 4013          # Description: Invalid intent(s); Explanation: You sent an invalid intent for a Gateway Intent. You may have incorrectly calculated the bitwise value.; Reconnect: False
    DISALLOWED_INTENTS = 4014       # Desc

class VoiceOpcodes(enum.IntEnum):
    IDENTIFY = 0                # Sent by: client; Description: Begin a voice websocket connection.
    SELECT_PROTOCOL = 1         # Sent by: client; Description: Select the voice protocol.
    READY = 2                   # Sent by: server; Description: Complete the websocket handshake.
    HEARTBEAT = 3               # Sent by: client; Description: Keep the websocket connection alive.
    SESSION_DESCRIPTION = 4     # Sent by: server; Description: Describe the session.
    SPEAKING = 5                # Sent by: client and server; Description: Indicate which users are speaking.
    HEARTBEAT_ACK = 6           # Sent by: server; Description: Sent to acknowledge a received client heartbeat.
    RESUME = 7                  # Sent by: client; Description: Resume a connection.
    HELLO = 8                   # Sent by: server; Description: Time to wait between sending heartbeats in milliseconds.
    RESUMED = 9                 # Sent by: server; Description: Acknowledge a successful session resume.
    CLIENTS_CONNECT = 11        # Sent by: server; Description: One or more clients have connected to the voice channel.
    CLIENT_DISCONNECT = 13      # Sent by: server; Description: A client has disconnected from the voice channel.
    DAVE_PREPARE_TRANSITION = 21 # Sent by: server; Description: A downgrade from the DAVE protocol is upcoming.
    DAVE_EXECUTE_TRANSITION = 22  # Sent by: server; Description: Execute a previously announced protocol transition.
    DAVE_TRANSITION_READY = 23     # Sent by: client; Description: Acknowledge readiness of previously announced transition.
    DAVE_PREPARE_EPOCH = 24        # Sent by: server; Description: A DAVE protocol version or group change is upcoming.
    DAVE_MLS_EXTERNAL_SENDER = 25  # Sent by: server; Description: Credential and public key for MLS external sender.
    DAVE_MLS_KEY_PACKAGE = 26      # Sent by: client; Description: MLS Key Package for pending group member.
    DAVE_MLS_PROPOSALS = 27        # Sent by: server; Description: MLS Proposals to be appended or revoked.
    DAVE_MLS_COMMIT_WELCOME = 28   # Sent by: client; Description: MLS Commit with optional MLS Welcome messages.
    DAVE_MLS_ANNOUNCE_COMMIT_TRANSITION = 29 # Sent by: server; Description: MLS Commit to be processed for upcoming transition.
    DAVE_MLS_WELCOME = 30          # Sent by: server; Description: MLS Welcome to group for upcoming transition.
    DAVE_MLS_INVALID_COMMIT_WELCOME = 31 # Sent by: client; Description: Flag invalid commit or welcome, request re-add.

class VoiceCloseEventCodes(enum.IntEnum):
    UNKNOWN_OPCODE = 4001                # Description: Unknown opcode; Explanation: You sent an invalid opcode.
    FAILED_TO_DECODE_PAYLOAD = 4002     # Description: Failed to decode payload; Explanation: You sent an invalid payload in your identifying to the Gateway.
    NOT_AUTHENTICATED = 4003            # Description: Not authenticated; Explanation: You sent a payload before identifying with the Gateway.
    AUTHENTICATION_FAILED = 4004        # Description: Authentication failed; Explanation: The token you sent in your identify payload is incorrect.
    ALREADY_AUTHENTICATED = 4005        # Description: Already authenticated; Explanation: You sent more than one identify payload. Stahp.
    SESSION_NO_LONGER_VALID = 4006      # Description: Session no longer valid; Explanation: Your session is no longer valid.
    SESSION_TIMEOUT = 4009              # Description: Session timeout; Explanation: Your session has timed out.
    SERVER_NOT_FOUND = 4011             # Description: Server not found; Explanation: We can't find the server you're trying to connect to.
    UNKNOWN_PROTOCOL = 4012             # Description: Unknown protocol; Explanation: We didn't recognize the protocol you sent.
    DISCONNECTED = 4014                 # Description: Disconnected; Explanation: Disconnect individual client (you were kicked, the main gateway session was dropped, etc.). Should not reconnect.
    VOICE_SERVER_CRASHED = 4015         # Description: Voice server crashed; Explanation: The server crashed. Our bad! Try resuming.
    UNKNOWN_ENCRYPTION_MODE = 4016      # Description: Unknown encryption mode; Explanation: We didn't recognize your encryption.
    BAD_REQUEST = 4020                 # Description: Bad request; Explanation: You sent a malformed request.
    DISCONNECTED_RATE_LIMITED = 4021   # Description: Disconnected: Rate Limited; Explanation: Disconnect due to rate limit exceeded. Should not reconnect.
    DISCONNECTED_CALL_TERMINATED = 4022 # Description: Disconnected: Call Terminated; Explanation: Disconnect all clients due to call terminated (channel deleted, voice server changed, etc.). Should not reconnect.

class HTTPResponseCodes(enum.IntEnum):
    OK = 200                # The request completed successfully.
    CREATED = 201           # The entity was created successfully.
    NO_CONTENT = 204        # The request completed successfully but returned no content.
    NOT_MODIFIED = 304      # The entity was not modified (no action was taken).
    BAD_REQUEST = 400       # The request was improperly formatted, or the server couldn't understand it.
    UNAUTHORIZED = 401      # The Authorization header was missing or invalid.
    FORBIDDEN = 403         # The Authorization token you passed did not have permission to the resource.
    NOT_FOUND = 404         # The resource at the location specified doesn't exist.
    METHOD_NOT_ALLOWED = 405# The HTTP method used is not valid for the location specified.
    TOO_MANY_REQUESTS = 429 # You are being rate limited, see Rate Limits.
    GATEWAY_UNAVAILABLE = 502 # There was not a gateway available to process your request. Wait a bit and retry.
    SERVER_ERROR = 500      # The server had an error processing your request (these are rare).

class JSONErrorCodes(enum.IntEnum):
    GENERAL_ERROR = 0                                 # General error (such as a malformed request body, amongst other things)
    UNKNOWN_ACCOUNT = 10001                           # Unknown account
    UNKNOWN_APPLICATION = 10002                       # Unknown application
    UNKNOWN_CHANNEL = 10003                           # Unknown channel
    UNKNOWN_GUILD = 10004                             # Unknown guild
    UNKNOWN_INTEGRATION = 10005                       # Unknown integration
    UNKNOWN_INVITE = 10006                            # Unknown invite
    UNKNOWN_MEMBER = 10007                            # Unknown member
    UNKNOWN_MESSAGE = 10008                           # Unknown message
    UNKNOWN_PERMISSION_OVERWRITE = 10009             # Unknown permission overwrite
    UNKNOWN_PROVIDER = 10010                          # Unknown provider
    UNKNOWN_ROLE = 10011                              # Unknown role
    UNKNOWN_TOKEN = 10012                             # Unknown token
    UNKNOWN_USER = 10013                              # Unknown user
    UNKNOWN_EMOJI = 10014                             # Unknown emoji
    UNKNOWN_WEBHOOK = 10015                           # Unknown webhook
    UNKNOWN_WEBHOOK_SERVICE = 10016                   # Unknown webhook service
    UNKNOWN_SESSION = 10020                           # Unknown session
    UNKNOWN_ASSET = 10021                             # Unknown Asset
    UNKNOWN_BAN = 10026                               # Unknown ban
    UNKNOWN_SKU = 10027                               # Unknown SKU
    UNKNOWN_STORE_LISTING = 10028                     # Unknown Store Listing
    UNKNOWN_ENTITLEMENT = 10029                       # Unknown entitlement
    UNKNOWN_BUILD = 10030                             # Unknown build
    UNKNOWN_LOBBY = 10031                             # Unknown lobby
    UNKNOWN_BRANCH = 10032                            # Unknown branch
    UNKNOWN_STORE_DIRECTORY_LAYOUT = 10033           # Unknown store directory layout
    UNKNOWN_REDISTRIBUTABLE = 10036                   # Unknown redistributable
    UNKNOWN_GIFT_CODE = 10038                         # Unknown gift code
    UNKNOWN_STREAM = 10049                            # Unknown stream
    UNKNOWN_PREMIUM_SERVER_SUBSCRIBE_COOLDOWN = 10050 # Unknown premium server subscribe cooldown
    UNKNOWN_GUILD_TEMPLATE = 10057                    # Unknown guild template
    UNKNOWN_DISCOVERABLE_SERVER_CATEGORY = 10059     # Unknown discoverable server category
    UNKNOWN_STICKER = 10060                           # Unknown sticker
    UNKNOWN_STICKER_PACK = 10061                      # Unknown sticker pack
    UNKNOWN_INTERACTION = 10062                       # Unknown interaction
    UNKNOWN_APPLICATION_COMMAND = 10063               # Unknown application command
    UNKNOWN_VOICE_STATE = 10065                       # Unknown voice state
    UNKNOWN_APPLICATION_COMMAND_PERMISSIONS = 10066  # Unknown application command permissions
    UNKNOWN_STAGE_INSTANCE = 10067                    # Unknown Stage Instance
    UNKNOWN_GUILD_MEMBER_VERIFICATION_FORM = 10068   # Unknown Guild Member Verification Form
    UNKNOWN_GUILD_WELCOME_SCREEN = 10069              # Unknown Guild Welcome Screen
    UNKNOWN_GUILD_SCHEDULED_EVENT = 10070             # Unknown Guild Scheduled Event
    UNKNOWN_GUILD_SCHEDULED_EVENT_USER = 10071        # Unknown Guild Scheduled Event User
    UNKNOWN_TAG = 10087                               # Unknown Tag
    UNKNOWN_SOUND = 10097                             # Unknown sound
    BOTS_CANNOT_USE_ENDPOINT = 20001                  # Bots cannot use this endpoint
    ONLY_BOTS_CAN_USE_ENDPOINT = 20002                # Only bots can use this endpoint
    EXPLICIT_CONTENT_CANNOT_BE_SENT = 20009           # Explicit content cannot be sent to the desired recipient(s)
    NOT_AUTHORIZED_FOR_APPLICATION = 20012            # You are not authorized to perform this action on this application
    SLOWMODE_RATE_LIMIT = 20016                        # This action cannot be performed due to slowmode rate limit
    ONLY_OWNER_CAN_PERFORM = 20018                     # Only the owner of this account can perform this action
    ANNOUNCEMENT_RATE_LIMIT_EDIT = 20022               # This message cannot be edited due to announcement rate limits
    UNDER_MINIMUM_AGE = 20024                          # Under minimum age
    CHANNEL_WRITE_RATE_LIMIT_HIT = 20028              # The channel you are writing has hit the write rate limit
    SERVER_WRITE_RATE_LIMIT_HIT = 20029               # The write action you are performing on the server has hit the write rate limit
    CONTENT_NOT_ALLOWED = 20031                        # Your Stage topic, server name, server description, or channel names contain words that are not allowed
    GUILD_PREMIUM_SUBSCRIPTION_LEVEL_TOO_LOW = 20035  # Guild premium subscription level too low
    MAX_GUILDS_REACHED = 30001                         # Maximum number of guilds reached (100)
    MAX_FRIENDS_REACHED = 30002                        # Maximum number of friends reached (1000)
    MAX_PINS_REACHED = 30003                           # Maximum number of pins reached for the channel (50)
    MAX_RECIPIENTS_REACHED = 30004                     # Maximum number of recipients reached (10)
    MAX_GUILD_ROLES_REACHED = 30005                    # Maximum number of guild roles reached (250)
    MAX_WEBHOOKS_REACHED = 30007                        # Maximum number of webhooks reached (15)
    MAX_EMOJIS_REACHED = 30008                         # Maximum number of emojis reached
    MAX_REACTIONS_REACHED = 30010                      # Maximum number of reactions reached (20)
    MAX_GROUP_DMS_REACHED = 30011                      # Maximum number of group DMs reached (10)
    MAX_GUILD_CHANNELS_REACHED = 30013                 # Maximum number of guild channels reached (500)
    MAX_ATTACHMENTS_PER_MESSAGE_REACHED = 30015       # Maximum number of attachments in a message reached (10)
    MAX_INVITES_REACHED = 30016                         # Maximum number of invites reached (1000)
    MAX_ANIMATED_EMOJIS_REACHED = 30018                # Maximum number of animated emojis reached
    MAX_SERVER_MEMBERS_REACHED = 30019                 # Maximum number of server members reached
    MAX_SERVER_CATEGORIES_REACHED = 30030              # Maximum number of server categories has been reached (5)
    GUILD_ALREADY_HAS_TEMPLATE = 30031                 # Guild already has a template
    MAX_APPLICATION_COMMANDS_REACHED = 30032           # Maximum number of application commands reached
    MAX_THREAD_PARTICIPANTS_REACHED = 30033            # Maximum number of thread participants has been reached (1000)
    MAX_DAILY_APPLICATION_COMMAND_CREATES_REACHED = 30034 # Maximum number of daily application command creates has been reached (200)
    MAX_BANS_NON_GUILD_MEMBERS_EXCEEDED = 30035        # Maximum number of bans for non-guild members have been exceeded
    MAX_BANS_FETCHES_REACHED = 30037                    # Maximum number of bans fetches has been reached
    MAX_UNCOMPLETED_GUILD_SCHEDULED_EVENTS_REACHED = 30038 # Maximum number of uncompleted guild scheduled events reached (100)
    MAX_STICKERS_REACHED = 30039                        # Maximum number of stickers reached
    MAX_PRUNE_REQUESTS_REACHED = 30040                  # Maximum number of prune requests has been reached. Try again later
    MAX_GUILD_WIDGET_SETTINGS_UPDATES_REACHED = 30042  # Maximum number of guild widget settings updates has been reached. Try again later
    MAX_SOUNDBOARD_SOUNDS_REACHED = 30045               # Maximum number of soundboard sounds reached
    MAX_EDITS_TO_OLD_MESSAGES_REACHED = 30046           # Maximum number of edits to messages older than 1 hour reached. Try again later
    MAX_PINNED_THREADS_IN_FORUM_REACHED = 30047         # Maximum number of pinned threads in a forum channel has been reached
    MAX_TAGS_IN_FORUM_CHANNEL_REACHED = 30048           # Maximum number of tags in a forum channel has been reached
    BITRATE_TOO_HIGH_FOR_CHANNEL_TYPE = 30052           # Bitrate is too high for channel of this type
    MAX_PREMIUM_EMOJIS_REACHED = 30056                   # Maximum number of premium emojis reached (25)
    MAX_WEBHOOKS_PER_GUILD_REACHED = 30058              # Maximum number of webhooks per guild reached (1000)
    MAX_CHANNEL_PERMISSION_OVERWRITES_REACHED = 30060   # Maximum number of channel permission overwrites reached (1000)
    CHANNELS_FOR_GUILD_TOO_LARGE = 30061                 # The channels for this guild are too large
    UNAUTHORIZED = 40001                                 # Unauthorized. Provide a valid token and try again
    NEED_VERIFY_ACCOUNT = 40002                          # You need to verify your account in order to perform this action
    OPENING_DMS_TOO_FAST = 40003                         # You are opening direct messages too fast
    SEND_MESSAGES_DISABLED = 40004                       # Send messages has been temporarily disabled
    REQUEST_ENTITY_TOO_LARGE = 40005                     # Request entity too large. Try sending something smaller in size
    FEATURE_TEMP_DISABLED_SERVER_SIDE = 40006           # This feature has been temporarily disabled server-side
    USER_BANNED_FROM_GUILD = 40007                       # The user is banned from this guild
    CONNECTION_REVOKED = 40012                           # Connection has been revoked
    CONSUMABLE_SKUS_ONLY = 40018                         # Only consumable SKUs can be consumed
    DELETE_SANDBOX_ENTITLEMENTS_ONLY = 40019            # You can only delete sandbox entitlements.
    TARGET_USER_NOT_CONNECTED_TO_VOICE = 40032          # Target user is not connected to voice
    MESSAGE_ALREADY_CROSSPOSTED = 40033                  # This message has already been crossposted
    COMMAND_NAME_ALREADY_EXISTS = 40041                  # An application command with that name already exists
    APPLICATION_INTERACTION_FAILED = 40043               # Application interaction failed to send
    CANNOT_SEND_MESSAGE_IN_FORUM_CHANNEL = 40058        # Cannot send a message in a forum channel
    INTERACTION_ALREADY_ACKNOWLEDGED = 40060             # Interaction has already been acknowledged
    TAG_NAMES_MUST_BE_UNIQUE = 40061                      # Tag names must be unique
    SERVICE_RESOURCE_RATE_LIMITED = 40062                 # Service resource is being rate limited
    NO_TAGS_FOR_NON_MODERATORS = 40066                    # There are no tags available that can be set by non-moderators
    TAG_REQUIRED_FOR_FORUM_POST = 40067                   # A tag is required to create a forum post in this channel
    ENTITLEMENT_ALREADY_GRANTED = 40074                   # An entitlement has already been granted for this resource
    MAX_FOLLOWUP_MESSAGES_HIT = 40094                      # This interaction has hit the maximum number of follow up messages
    CLOUDFLARE_BLOCKING_REQUEST = 40333                    # Cloudflare is blocking your request. This can often be resolved by setting a proper User Agent
    MISSING_ACCESS = 50001                                 # Missing access
    INVALID_ACCOUNT_TYPE = 50002                           # Invalid account type
    CANNOT_EXECUTE_ACTION_ON_DM_CHANNEL = 50003           # Cannot execute action on a DM channel
    GUILD_WIDGET_DISABLED = 50004                          # Guild widget disabled
    CANNOT_EDIT_ANOTHER_USERS_MESSAGE = 50005             # Cannot edit a message authored by another user
    CANNOT_SEND_EMPTY_MESSAGE = 50006                      # Cannot send an empty message
    CANNOT_SEND_MESSAGES_TO_USER = 50007                  # Cannot send messages to this user
    CANNOT_SEND_MESSAGES_IN_NON_TEXT_CHANNEL = 50008      # Cannot send messages in a non-text channel
    CHANNEL_VERIFICATION_LEVEL_TOO_HIGH = 50009           # Channel verification level is too high for you to gain access
    OAUTH2_APPLICATION_DOES_NOT_HAVE_BOT = 50010          # OAuth2 application does not have a bot
    OAUTH2_APPLICATION_LIMIT_REACHED = 50011              # OAuth2 application limit reached
    INVALID_OAUTH2_STATE = 50012                            # Invalid OAuth2 state
    LACK_PERMISSIONS = 50013                                # You lack permissions to perform that action
    INVALID_AUTH_TOKEN = 50014                              # Invalid authentication token provided
    NOTE_TOO_LONG = 50015                                   # Note was too long
    INVALID_MESSAGES_TO_DELETE_COUNT = 50016               # Provided too few or too many messages to delete. Must provide at least 2 and fewer than 100 messages to delete
    INVALID_MFA_LEVEL = 50017                               # Invalid MFA Level
    MESSAGE_CAN_ONLY_BE_PINNED_TO_CHANNEL_IT_WAS_SENT_IN = 50019 # A message can only be pinned to the channel it was sent in
    INVALID_OR_TAKEN_INVITE_CODE = 50020                    # Invite code was either invalid or taken
    CANNOT_EXECUTE_ACTION_ON_SYSTEM_MESSAGE = 50021        # Cannot execute action on a system message
    CANNOT_EXECUTE_ACTION_ON_CHANNEL_TYPE = 50024          # Cannot execute action on this channel type
    INVALID_OAUTH2_ACCESS_TOKEN = 50025                     # Invalid OAuth2 access token provided
    MISSING_OAUTH2_SCOPE = 50026                             # Missing required OAuth2 scope
    INVALID_WEBHOOK_TOKEN = 50027                            # Invalid webhook token provided
    INVALID_ROLE = 50028                                     # Invalid role
    INVALID_RECIPIENTS = 50033                               # Invalid Recipient(s)
    MESSAGE_TOO_OLD_TO_BULK_DELETE = 50034                  # A message provided was too old to bulk delete
    INVALID_FORM_BODY_OR_CONTENT_TYPE = 50035               # Invalid form body (returned for both application/json and multipart/form-data bodies), or invalid Content-Type provided
    INVITE_ACCEPTED_FOR_BOT_NOT_IN_GUILD = 50036            # An invite was accepted to a guild the application's bot is not in
    INVALID_ACTIVITY_ACTION = 50039                          # Invalid Activity Action
    INVALID_API_VERSION = 50041                              # Invalid API version provided
    FILE_UPLOAD_EXCEEDS_MAX_SIZE = 50045                     # File uploaded exceeds the maximum size
    INVALID_FILE_UPLOADED = 50046                            # Invalid file uploaded
    CANNOT_SELF_REDEEM_GIFT = 50054                          # Cannot self-redeem this gift
    INVALID_GUILD = 50055                                    # Invalid Guild
    INVALID_SKU = 50057                                      # Invalid SKU
    INVALID_REQUEST_ORIGIN = 50067                           # Invalid request origin
    INVALID_MESSAGE_TYPE = 50068                             # Invalid message type
    PAYMENT_SOURCE_REQUIRED_TO_REDEEM_GIFT = 50070          # Payment source required to redeem gift
    CANNOT_MODIFY_SYSTEM_WEBHOOK = 50073                     # Cannot modify a system webhook
    CANNOT_DELETE_CHANNEL_REQUIRED_FOR_COMMUNITY_GUILD = 50074 # Cannot delete a channel required for Community guilds
    CANNOT_EDIT_STICKERS_WITHIN_MESSAGE = 50080             # Cannot edit stickers within a message
    INVALID_STICKER_SENT = 50081                             # Invalid sticker sent
    OPERATION_ON_ARCHIVED_THREAD_NOT_ALLOWED = 50083        # Tried to perform an operation on an archived thread, such as editing a message or adding a user to the thread
    INVALID_THREAD_NOTIFICATION_SETTINGS = 50084            # Invalid thread notification settings
    BEFORE_VALUE_EARLIER_THAN_THREAD_CREATION_DATE = 50085  # before value is earlier than the thread creation date
    COMMUNITY_SERVER_CHANNELS_MUST_BE_TEXT_CHANNELS = 50086 # Community server channels must be text channels
    EVENT_ENTITY_TYPE_MISMATCH = 50091                       # The entity type of the event is different from the entity you are trying to start the event for
    SERVER_NOT_AVAILABLE_IN_LOCATION = 50095                 # This server is not available in your location
    SERVER_NEEDS_MONETIZATION_ENABLED = 50097                # This server needs monetization enabled in order to perform this action
    SERVER_NEEDS_MORE_BOOSTS = 50101                         # This server needs more boosts to perform this action
    INVALID_JSON_BODY = 50109                                 # The request body contains invalid JSON.
    INVALID_FILE = 50110                                      # The provided file is invalid.
    INVALID_FILE_TYPE = 50123                                 # The provided file type is invalid.
    FILE_DURATION_EXCEEDS_MAX = 50124                         # The provided file duration exceeds maximum of 5.2 seconds.
    OWNER_CANNOT_BE_PENDING_MEMBER = 50131                    # Owner cannot be pending member
    OWNERSHIP_CANNOT_BE_TRANSFERRED_TO_BOT = 50132           # Ownership cannot be transferred to a bot user
    FAILED_TO_RESIZE_ASSET = 50138                            # Failed to resize asset below the maximum size: 262144
    CANNOT_MIX_SUBSCRIPTION_AND_NON_SUBSCRIPTION_ROLES = 50144 # Cannot mix subscription and non subscription roles for an emoji
    CANNOT_CONVERT_BETWEEN_PREMIUM_AND_NORMAL_EMOJI = 50145  # Cannot convert between premium emoji and normal emoji
    UPLOADED_FILE_NOT_FOUND = 50146                           # Uploaded file not found.
    SPECIFIED_EMOJI_INVALID = 50151                           # The specified emoji is invalid
    VOICE_MESSAGES_NO_ADDITIONAL_CONTENT = 50159             # Voice messages do not support additional content.
    VOICE_MESSAGES_MUST_HAVE_SINGLE_AUDIO_ATTACHMENT = 50160 # Voice messages must have a single audio attachment.
    VOICE_MESSAGES_MUST_HAVE_METADATA = 50161                # Voice messages must have supporting metadata.
    VOICE_MESSAGES_CANNOT_BE_EDITED = 50162                   # Voice messages cannot be edited.
    CANNOT_DELETE_GUILD_SUBSCRIPTION_INTEGRATION = 50163     # Cannot delete guild subscription integration
    CANNOT_SEND_VOICE_MESSAGES_IN_CHANNEL = 50173            # You cannot send voice messages in this channel.
    USER_ACCOUNT_MUST_BE_VERIFIED = 50178                     # The user account must first be verified
    FILE_DOES_NOT_HAVE_VALID_DURATION = 50192                 # The provided file does not have a valid duration.
    PERMISSION_TO_SEND_STICKER_DENIED = 50600                 # You do not have permission to send this sticker.
    TWO_FACTOR_REQUIRED = 60003                                # Two factor is required for this operation
    NO_USERS_WITH_DISCORDTAG_EXIST = 80004                    # No users with DiscordTag exist
    REACTION_WAS_BLOCKED = 90001                               # Reaction was blocked
    USER_CANNOT_USE_BURST_REACTIONS = 90002                   # User cannot use burst reactions
    APPLICATION_NOT_YET_AVAILABLE = 110001                     # Application not yet available. Try again later
    API_RESOURCE_OVERLOADED = 130000                            # API resource is currently overloaded. Try again a little later
    STAGE_ALREADY_OPEN = 150006                                 # The Stage is already open
    CANNOT_REPLY_WITHOUT_READ_MESSAGE_HISTORY_PERMISSION = 160002 # Cannot reply without permission to read message history
    THREAD_ALREADY_CREATED_FOR_MESSAGE = 160004                # A thread has already been created for this message
    THREAD_IS_LOCKED = 160005                                   # Thread is locked
    MAX_ACTIVE_THREADS_REACHED = 160006                         # Maximum number of active threads reached
    MAX_ACTIVE_ANNOUNCEMENT_THREADS_REACHED = 160007           # Maximum number of active announcement threads reached
    INVALID_JSON_UPLOADED_LOTTIE_FILE = 170001                  # Invalid JSON for uploaded Lottie file
    UPLOADED_LOTTIES_CANNOT_CONTAIN_RASTER_IMAGES = 170002     # Uploaded Lotties cannot contain rasterized images such as PNG or JPEG
    STICKER_MAX_FRAMERATE_EXCEEDED = 170003                     # Sticker maximum framerate exceeded
    STICKER_FRAME_COUNT_EXCEEDS_MAX = 170004                    # Sticker frame count exceeds maximum of 1000 frames
    LOTTIE_ANIMATION_MAX_DIMENSIONS_EXCEEDED = 170005           # Lottie animation maximum dimensions exceeded
    STICKER_FRAME_RATE_TOO_SMALL_OR_LARGE = 170006              # Sticker frame rate is either too small or too large
    STICKER_ANIMATION_DURATION_EXCEEDS_MAX = 170007             # Sticker animation duration exceeds maximum of 5 seconds
    CANNOT_UPDATE_FINISHED_EVENT = 180000                        # Cannot update a finished event
    FAILED_TO_CREATE_STAGE_NEEDED_FOR_STAGE_EVENT = 180002      # Failed to create stage needed for stage event
    MESSAGE_BLOCKED_BY_AUTOMATIC_MODERATION = 200000             # Message was blocked by automatic moderation
    TITLE_BLOCKED_BY_AUTOMATIC_MODERATION = 200001               # Title was blocked by automatic moderation
    WEBHOOKS_POSTED_TO_FORUM_MUST_HAVE_THREAD_NAME_OR_ID = 220001 # Webhooks posted to forum channels must have a thread_name or thread_id
    WEBHOOKS_POSTED_TO_FORUM_CANNOT_HAVE_BOTH_THREAD_NAME_AND_ID = 220002 # Webhooks posted to forum channels cannot have both a thread_name and thread_id
    WEBHOOKS_CAN_ONLY_CREATE_THREADS_IN_FORUM = 220003           # Webhooks can only create threads in forum channels
    WEBHOOK_SERVICES_CANNOT_BE_USED_IN_FORUM = 220004            # Webhook services cannot be used in forum channels
    MESSAGE_BLOCKED_BY_HARMFUL_LINKS_FILTER = 240000             # Message blocked by harmful links filter
    CANNOT_ENABLE_ONBOARDING_REQUIREMENTS_NOT_MET = 350000       # Cannot enable onboarding, requirements are not met
    CANNOT_UPDATE_ONBOARDING_BELOW_REQUIREMENTS = 350001         # Cannot update onboarding while below requirements
    FAILED_TO_BAN_USERS = 500000                                 # Failed to ban users
    POLL_VOTING_BLOCKED = 520000                                 # Poll voting blocked
    POLL_EXPIRED = 520001                                        # Poll expired
    INVALID_CHANNEL_TYPE_FOR_POLL_CREATION = 520002             # Invalid channel type for poll creation
    CANNOT_EDIT_POLL_MESSAGE = 520003                            # Cannot edit a poll message
    CANNOT_USE_EMOJI_INCLUDED_WITH_POLL = 520004                # Cannot use an emoji included with the poll
    CANNOT_EXPIRE_NON_POLL_MESSAGE = 520006                      # Cannot expire a non-poll message

class RPCErrorCodes(enum.IntEnum):
    UNKNOWN_ERROR = 1000                # An unknown error occurred.
    INVALID_PAYLOAD = 4000              # You sent an invalid payload.
    INVALID_COMMAND = 4002              # Invalid command name specified.
    INVALID_GUILD = 4003                # Invalid guild ID specified.
    INVALID_EVENT = 4004                # Invalid event name specified.
    INVALID_CHANNEL = 4005              # Invalid channel ID specified.
    INVALID_PERMISSIONS = 4006          # You lack permissions to access the given resource.
    INVALID_CLIENT_ID = 4007            # An invalid OAuth2 application ID was used to authorize or authenticate with.
    INVALID_ORIGIN = 4008               # An invalid OAuth2 application origin was used to authorize or authenticate with.
    INVALID_TOKEN = 4009                # An invalid OAuth2 token was used to authorize or authenticate with.
    INVALID_USER = 4010                 # The specified user ID was invalid.
    OAUTH2_ERROR = 5000                 # A standard OAuth2 error occurred; check the data object for details.
    SELECT_CHANNEL_TIMED_OUT = 5001    # An asynchronous SELECT_TEXT_CHANNEL/SELECT_VOICE_CHANNEL command timed out.
    GET_GUILD_TIMED_OUT = 5002          # An asynchronous GET_GUILD command timed out.
    SELECT_VOICE_FORCE_REQUIRED = 5003 # Tried to join a user to a voice channel but the user was already in one.
    CAPTURE_SHORTCUT_ALREADY_LISTENING = 5004  # Tried to capture more than one shortcut key at once.

class RPCCloseEventCodes(enum.IntEnum):
    INVALID_CLIENT_ID = 4000    # You connected to the RPC server with an invalid client ID.
    INVALID_ORIGIN = 4001       # You connected to the RPC server with an invalid origin.
    RATE_LIMITED = 4002         # You are being rate limited.
    TOKEN_REVOKED = 4003        # The OAuth2 token associated with a connection was revoked, get a new one!
    INVALID_VERSION = 4004      # The RPC Server version specified in the connection string was not valid.
    INVALID_ENCODING = 4005     # The encoding specified in the connection string was not valid.

#Permissions-
class BitwisePermissionFlags(enum.IntFlag):
    CREATE_INSTANT_INVITE = 1 << 0
    KICK_MEMBERS = 1 << 1
    BAN_MEMBERS = 1 << 2
    ADMINISTRATOR = 1 << 3
    MANAGE_CHANNELS = 1 << 4
    MANAGE_GUILD = 1 << 5
    ADD_REACTIONS = 1 << 6
    VIEW_AUDIT_LOG = 1 << 7
    PRIORITY_SPEAKER = 1 << 8
    STREAM = 1 << 9
    VIEW_CHANNEL = 1 << 10
    SEND_MESSAGES = 1 << 11
    SEND_TTS_MESSAGES = 1 << 12
    MANAGE_MESSAGES = 1 << 13
    EMBED_LINKS = 1 << 14
    ATTACH_FILES = 1 << 15
    READ_MESSAGE_HISTORY = 1 << 16
    MENTION_EVERYONE = 1 << 17
    USE_EXTERNAL_EMOJIS = 1 << 18
    VIEW_GUILD_INSIGHTS = 1 << 19
    CONNECT = 1 << 20
    SPEAK = 1 << 21
    MUTE_MEMBERS = 1 << 22
    DEAFEN_MEMBERS = 1 << 23
    MOVE_MEMBERS = 1 << 24
    USE_VAD = 1 << 25
    CHANGE_NICKNAME = 1 << 26
    MANAGE_NICKNAMES = 1 << 27
    MANAGE_ROLES = 1 << 28
    MANAGE_WEBHOOKS = 1 << 29
    MANAGE_GUILD_EXPRESSIONS = 1 << 30
    USE_APPLICATION_COMMANDS = 1 << 31
    REQUEST_TO_SPEAK = 1 << 32
    MANAGE_EVENTS = 1 << 33
    MANAGE_THREADS = 1 << 34
    CREATE_PUBLIC_THREADS = 1 << 35
    CREATE_PRIVATE_THREADS = 1 << 36
    USE_EXTERNAL_STICKERS = 1 << 37
    SEND_MESSAGES_IN_THREADS = 1 << 38
    USE_EMBEDDED_ACTIVITIES = 1 << 39 
    MODERATE_MEMBERS = 1 << 40
    VIEW_CREATOR_MONETIZATION_ANALYTICS = 1 << 41
    USE_SOUNDBOARD = 1 << 42
    CREATE_GUILD_EXPRESSIONS = 1 << 43
    CREATE_EVENTS = 1 << 44
    USE_EXTERNAL_SOUNDS = 1 << 45
    SEND_VOICE_MESSAGES = 1 << 46
    SEND_POLLS = 1 << 49
    USE_EXTERNAL_APPS = 1 << 50

class RoleFlags(enum.IntFlag):
    IN_PROMPT = 1 << 0

class Role(msgspec.Struct, kw_only=True):
    """
    Role represents a set of permissions attached to a group of users.
    """
    id : str
    name : str
    color : int | None = None
    colors : 'RoleColor'
    hoist : bool
    icon : str | None = None
    unicode_emoji : str | None = None
    position : int
    permissions : str
    managed : bool
    mentionable : bool
    tags : 'RoleTags' | None = None
    flags : int

class RoleColor(msgspec.Struct, kw_only=True):
    primary_color : int
    secondary_color : int | None = None
    tertiary_color : int | None = None

class RoleTags(msgspec.Struct, kw_only=True):
    """
    Note: for premium_subscriber, available_for_purchase and guild_connections fields, null is sent if the field is true and will not be included if false.
    """
    bot_id : str
    integration_id : str
    premium_subscriber : None | bool = False
    subscription_listing_id : str
    available_for_purchase : None | bool = False
    guild_connections : None | bool = False

#Rate limits-
class RateLimitResponse(msgspec.Struct, kw_only=True):
    message: str           # A message saying you are being rate limited.
    retry_after: float     # Number of seconds to wait before retrying.
    global_limit: bool     # Indicates if rate limit is global.
    code: 'JSONErrorCodes' | None = None  # Optional error code.

#RPC-
class RPCCommands(enum.StrEnum):
    DISPATCH = "DISPATCH"  # Event dispatch
    AUTHORIZE = "AUTHORIZE"  # Authorize a new client with your app
    AUTHENTICATE = "AUTHENTICATE"  # Authenticate an existing client with your app
    GET_GUILD = "GET_GUILD"  # Retrieve guild information from the client
    GET_GUILDS = "GET_GUILDS"  # Retrieve a list of guilds from the client
    GET_CHANNEL = "GET_CHANNEL"  # Retrieve channel information from the client
    GET_CHANNELS = "GET_CHANNELS"  # Retrieve a list of channels for a guild from the client
    SUBSCRIBE = "SUBSCRIBE"  # Subscribe to an RPC event
    UNSUBSCRIBE = "UNSUBSCRIBE"  # Unsubscribe from an RPC event
    SET_USER_VOICE_SETTINGS = "SET_USER_VOICE_SETTINGS"  # Change voice settings of users in voice channels
    SELECT_VOICE_CHANNEL = "SELECT_VOICE_CHANNEL"  # Join or leave a voice channel, group DM, or DM
    GET_SELECTED_VOICE_CHANNEL = "GET_SELECTED_VOICE_CHANNEL"  # Get the current voice channel the client is in
    SELECT_TEXT_CHANNEL = "SELECT_TEXT_CHANNEL"  # Join or leave a text channel, group DM, or DM
    GET_VOICE_SETTINGS = "GET_VOICE_SETTINGS"  # Retrieve the client's voice settings
    SET_VOICE_SETTINGS = "SET_VOICE_SETTINGS"  # Set the client's voice settings
    SET_CERTIFIED_DEVICES = "SET_CERTIFIED_DEVICES"  # Send info about certified hardware devices
    SET_ACTIVITY = "SET_ACTIVITY"  # Update a user's Rich Presence
    SEND_ACTIVITY_JOIN_INVITE = "SEND_ACTIVITY_JOIN_INVITE"  # Consent to a Rich Presence Ask to Join request
    CLOSE_ACTIVITY_REQUEST = "CLOSE_ACTIVITY_REQUEST"  # Reject a Rich Presence Ask to Join request

class RPCEvents(enum.StrEnum):
    READY = "READY"  # Non-subscription event sent immediately after connecting, contains server information
    ERROR = "ERROR"  # Non-subscription event sent when there is an error, including command responses
    GUILD_STATUS = "GUILD_STATUS"  # Sent when a subscribed server's state changes
    GUILD_CREATE = "GUILD_CREATE"  # Sent when a guild is created/joined on the client
    CHANNEL_CREATE = "CHANNEL_CREATE"  # Sent when a channel is created/joined on the client
    VOICE_CHANNEL_SELECT = "VOICE_CHANNEL_SELECT"  # Sent when the client joins a voice channel
    VOICE_STATE_CREATE = "VOICE_STATE_CREATE"  # Sent when a user joins a subscribed voice channel
    VOICE_STATE_UPDATE = "VOICE_STATE_UPDATE"  # Sent when a user's voice state changes in a subscribed voice channel (mute, volume, etc.)
    VOICE_STATE_DELETE = "VOICE_STATE_DELETE"  # Sent when a user parts a subscribed voice channel
    VOICE_SETTINGS_UPDATE = "VOICE_SETTINGS_UPDATE"  # Sent when the client's voice settings update
    VOICE_CONNECTION_STATUS = "VOICE_CONNECTION_STATUS"  # Sent when the client's voice connection status changes
    SPEAKING_START = "SPEAKING_START"  # Sent when a user in a subscribed voice channel speaks
    SPEAKING_STOP = "SPEAKING_STOP"  # Sent when a user in a subscribed voice channel stops speaking
    MESSAGE_CREATE = "MESSAGE_CREATE"  # Sent when a message is created in a subscribed text channel
    MESSAGE_UPDATE = "MESSAGE_UPDATE"  # Sent when a message is updated in a subscribed text channel
    MESSAGE_DELETE = "MESSAGE_DELETE"  # Sent when a message is deleted in a subscribed text channel
    NOTIFICATION_CREATE = "NOTIFICATION_CREATE"  # Sent when the client receives a notification (mention or new message in eligible channels)
    ACTIVITY_JOIN = "ACTIVITY_JOIN"  # Sent when the user clicks a Rich Presence join invite in chat to join a game
    ACTIVITY_SPECTATE = "ACTIVITY_SPECTATE"  # Sent when the user clicks a Rich Presence spectate invite in chat to spectate a game
    ACTIVITY_JOIN_REQUEST = "ACTIVITY_JOIN_REQUEST"  # Sent when the user receives a Rich Presence Ask to Join request

class KeyTypes(enum.IntEnum):
    KEYBOARD_KEY = 0  # Keyboard key
    MOUSE_BUTTON = 1  # Mouse button
    KEYBOARD_MODIFIER_KEY = 2  # Keyboard modifier key
    GAMEPAD_BUTTON = 3  # Gamepad button

class Payload(msgspec.Struct, kw_only=True):
    cmd: 'RPCCommands'                 # Always present - payload command
    nonce: str | None = None               # Unique string for replies from server
    evt: 'RPCEvents' | None = None        # Subscription event name
    data: dict | None = None               # Event data from server
    args: dict | None = None               # Command arguments sent to server

class AuthorizeArgument(msgspec.Struct, kw_only=True):
    scopes: list['OAuth2Scopes']  # Scopes to authorize (array of OAuth2 scopes)
    client_id: str  # OAuth2 application ID
    rpc_token: str  # One-time use RPC token
    username: str  # Username to create a guest account if the user does not have Discord

class AuthorizeResponse(msgspec.Struct, kw_only=True):
    code: str  # OAuth2 authorization code

class AuthenticateArgument(msgspec.Struct, kw_only=True):
    access_token: str  # OAuth2 access token

class AuthenticateResponse(msgspec.Struct, kw_only=True):
    user: 'User'  # partial user object (structure depends on Discord's User Object)
    scopes: list['OAuth2Scopes']  # authorized scopes
    expires: datetime  # expiration date of OAuth2 token
    application: 'OAuth2Application'  # application the user authorized

class OAuth2Application(msgspec.Struct, kw_only=True):
    description: str  # application description
    icon: str  # hash of the icon
    id: str  # application client id (snowflake)
    rpc_origins: list[str]  # array of rpc origin urls
    name: str  # application name

class GetGuildsResponse(msgspec.Struct, kw_only=True):
    guilds: list['Guild']  # array of partial guild objects

class GetGuildArgument(msgspec.Struct, kw_only=True):
    guild_id: str  # id of the guild to get
    timeout: int   # time to wait before timing out

class GetGuildResponse(msgspec.Struct, kw_only=True):
    id: str                    # guild id
    name: str                  # guild name
    icon_url: str              # guild icon url
    members: list['GuildMember']        # members of the guild (deprecated; always empty array)

class GetChannelArgument(msgspec.Struct, kw_only=True):
    channel_id: str  # id of the channel to get

class GetChannelResponse(msgspec.Struct, kw_only=True):
    id: str                         # channel id
    guild_id: str                   # channel's guild id
    name: str                       # channel name
    type: 'ChannelTypes'                       # channel type (guild text: 0, guild voice: 2, dm: 1, group dm: 3)
    topic: str                      # (text) channel topic
    bitrate: int                    # (voice) bitrate of voice channel
    user_limit: int                 # (voice) user limit of voice channel (0 for none)
    position: int                   # position of channel in channel list
    voice_states: list['VoiceState']        # (voice) channel's voice states
    messages: list['Message']            # (text) channel's messages

class GetChannelsArgument(msgspec.Struct, kw_only=True):
    guild_id: str  # id of the guild to get channels for

class GetChannelsResponse(msgspec.Struct, kw_only=True):
    channels: list['Channel']  # guild channels the user is in (partial channel objects)

class SetUserVoiceSettings(msgspec.Struct, kw_only=True):
    user_id: str  # user id
    pan: 'Pan' | None = None  # set the pan of the user
    volume: int | None = None  # set the volume of user (defaults to 100, min 0, max 200)
    mute: bool | None = None  # set the mute state of the user

class Pan(msgspec.Struct, kw_only=True):
    left: float  # pan left value
    right: float  # pan right value

class SelectVoiceChannelArgument(msgspec.Struct, kw_only=True):
    channel_id: str | None  # channel id to join (or None to leave)
    timeout: int  # asynchronously join channel with time to wait before timing out
    force: bool  # forces a user to join a voice channel
    navigate: bool  # after joining the voice channel, navigate to it in the client

class SelectTextChannelArgument(msgspec.Struct, kw_only=True):
    channel_id: str | None  # channel id to join (or None to leave)
    timeout: int  # asynchronously join channel with time to wait before timing out

class GetVoiceSettingsResponse(msgspec.Struct, kw_only=True):
    input: 'VoiceSettingsInput'  # voice settings input object
    output: 'VoiceSettingsOutput'  # voice settings output object
    mode: 'VoiceSettingsMode'  # voice settings mode object
    automatic_gain_control: bool  # state of automatic gain control
    echo_cancellation: bool  # state of echo cancellation
    noise_suppression: bool  # state of noise suppression
    qos: bool  # state of voice quality of service
    silence_warning: bool  # state of silence warning notice
    deaf: bool  # state of self-deafen
    mute: bool  # state of self-mute

class VoiceSettingsInput(msgspec.Struct, kw_only=True):
    device_id: str  # device id
    volume: float  # input voice level (min: 0, max: 100)
    available_devices: list['RPCDevice']  # read-only devices list

class VoiceSettingsOutput(msgspec.Struct, kw_only=True):
    device_id: str  # device id
    volume: float  # output voice level (min: 0, max: 200)
    available_devices: list['RPCDevice']  # read-only devices list

class VoiceSettingsMode(msgspec.Struct, kw_only=True):
    type: str  # PUSH_TO_TALK or VOICE_ACTIVITY
    auto_threshold: bool  # auto threshold enabled
    threshold: float  # voice activity threshold (in dB)
    shortcut: 'ShortcutKeyCombo'  # shortcut for PTT
    delay: float  # PTT release delay (in ms)

class RPCDevice(msgspec.Struct, kw_only=True):
    id: str  # device id
    name: str  # device name

class ShortcutKeyCombo(msgspec.Struct, kw_only=True):
    type: 'KeyTypes'  # type of key combo (e.g., "KEYBOARD")
    code: str  # key code or identifier
    name : str

class SetVoiceSettings(msgspec.Struct, kw_only=True):
    input: "VoiceSettingsInput"  # input settings
    output: "VoiceSettingsOutput"  # output settings
    mode: "VoiceSettingsMode"  # voice mode settings
    automatic_gain_control: bool  # state of automatic gain control
    echo_cancellation: bool  # state of echo cancellation
    noise_suppression: bool  # state of noise suppression
    qos: bool  # state of voice quality of service
    silence_warning: bool  # state of silence warning notice
    deaf: bool  # state of self-deafen
    mute: bool  # state of self-mute

class SubscribeResponse(msgspec.Struct, kw_only=True):
    evt: str  # event name now subscribed to

class UnsubscribeResponse(msgspec.Struct, kw_only=True):
    evt: str  # event name now unsubscribed from

class SetCertifiedDevicesArgument(msgspec.Struct, kw_only=True):
    devices: list['Device']  # list of devices for your manufacturer, in order of priority

#The Activity class is not included in this package because its part of the discord gateway websocket
class SetActivityArgument(msgspec.Struct, kw_only=True):
    pid: int  # application's process id
    activity: 'Activity'  # rich presence to assign to the user (limited to Playing, Listening, Watching, or Competing)

class SendActivityJoinInviteArgument(msgspec.Struct, kw_only=True):
    user_id: str  # snowflake - the id of the requesting user

class CloseActivityRequestArgument(msgspec.Struct, kw_only=True):
    user_id: str  # snowflake - the id of the requesting user

class ReadyDispatchData(msgspec.Struct, kw_only=True):
    v: int  # RPC version
    config: 'RPCServerConfiguration'  # server configuration
    user: 'User'  # the user to whom you are connected

class RPCServerConfiguration(msgspec.Struct, kw_only=True):
    cdn_host: str  # server's cdn
    api_endpoint: str  # server's api endpoint
    environment: str  # server's environment

class ErrorData(msgspec.Struct, kw_only=True):
    code: int  # RPC Error Code
    message: str  # Error description

class GuildStatusArgument(msgspec.Struct, kw_only=True):
    guild_id: str  # id of guild to listen to updates of

class GuildStatusDispatchData(msgspec.Struct, kw_only=True):
    guild: "Guild"  # guild with requested id
    online: int  # number of online users in guild (deprecated; always 0)

class GuildCreateDispatchData(msgspec.Struct, kw_only=True):
    id: str  # guild id
    name: str  # name of the guild

class ChannelCreateDispatchData(msgspec.Struct, kw_only=True):
    id: str  # channel id
    name: str  # name of the channel
    type: 'ChannelTypes'  # channel type (guild text: 0, guild voice: 2, dm: 1, group dm: 3)

class VoiceChannelSelectDispatchData(msgspec.Struct, kw_only=True):
    channel_id: str | None  # id of channel (null if none)
    guild_id: str | None    # id of guild (null if none)

class VoiceStateArgument(msgspec.Struct, kw_only=True):
    channel_id: str  # id of channel to listen to updates of

class VoiceConnectionStatus(msgspec.Struct, kw_only=True):
    state: str  # one of the voice connection states
    hostname: str  # hostname of the connected voice server
    pings: list[int]  # last 20 pings (in ms)
    average_ping: int  # average ping (in ms)
    last_ping: int  # last ping (in ms)

class MessageArgument(msgspec.Struct, kw_only=True):
    channel_id: str  # id of channel to listen to updates of

class SpeakingArgument(msgspec.Struct, kw_only=True):
    channel_id: str  # id of channel to listen to updates of

class SpeakingDispatch(msgspec.Struct, kw_only=True):
    user_id: str  # id of user who started/stopped speaking

class NotificationCreateDispatch(msgspec.Struct, kw_only=True):
    channel_id: str  # id of channel where notification occurred
    message: "Message"  # message object that generated this notification
    icon_url: str  # icon url of the notification
    title: str  # title of the notification
    body: str  # body of the notification

class ActivityJoinDispatch(msgspec.Struct, kw_only=True):
    secret: str  # the join_secret for the given invite

class ActivitySpectateDispatch(msgspec.Struct, kw_only=True):
    secret: str  # the spectate_secret for the given invite

class ActivityJoinRequestData(msgspec.Struct, kw_only=True):
    user: 'User'  # information about the user requesting to join

#Teams-
class TeamMemberRoleTypes(enum.StrEnum):
    ADMIN = "Admin"
    DEVELOPER = "Developer"
    READ_ONLY = "Read_only"

class MembershipStates(enum.IntEnum):
    INVITED = 1
    ACCEPTED = 2

class Team(msgspec.Struct, kw_only=True):
    """
    Team Object represents a group of developers who collaboratively manage an application—primarily used in the context of bots, integrations, and game SDKs
    """
    icon : str
    id : str
    members : list['TeamMember']
    name : str
    owner_user_id : str

class TeamMember(msgspec.Struct, kw_only=True):
    """
    TeamMember represents a member of a Team object.
    """
    membership_state : 'MembershipStates'
    team_id : str
    user : 'User'
    role : 'TeamMemberRoleTypes' | str = ""

try:
    rcd = msgspec.json.decode(
    b'{"burst": 8, "normal": 88, "test": {"name": "Michael", "age": null, "nested_object": {"nested": true}}}',
    type=ReactionCountDetails
    )
    print(rcd)
except Exception as e:
    print(e)