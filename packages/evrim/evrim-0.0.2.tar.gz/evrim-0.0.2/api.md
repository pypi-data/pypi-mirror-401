# Evrim

Methods:

- <code title="get /">client.<a href="./src/evrim/_client.py">welcome</a>() -> object</code>

# Chat

Types:

```python
from evrim.types import Response
```

Methods:

- <code title="get /chat/responses/{id}">client.chat.<a href="./src/evrim/resources/chat/chat.py">get_response</a>(id) -> <a href="./src/evrim/types/response.py">Response</a></code>

## Sessions

Types:

```python
from evrim.types.chat import ChatUser, Session, SessionListResponse, SessionGetMessagesResponse
```

Methods:

- <code title="get /chat/sessions/{id}">client.chat.sessions.<a href="./src/evrim/resources/chat/sessions.py">retrieve</a>(id) -> <a href="./src/evrim/types/chat/session.py">Session</a></code>
- <code title="get /chat/sessions">client.chat.sessions.<a href="./src/evrim/resources/chat/sessions.py">list</a>(\*\*<a href="src/evrim/types/chat/session_list_params.py">params</a>) -> <a href="./src/evrim/types/chat/session_list_response.py">SessionListResponse</a></code>
- <code title="delete /chat/sessions/{id}">client.chat.sessions.<a href="./src/evrim/resources/chat/sessions.py">delete</a>(id) -> object</code>
- <code title="get /chat/sessions/{session_id}/messages">client.chat.sessions.<a href="./src/evrim/resources/chat/sessions.py">get_messages</a>(session_id, \*\*<a href="src/evrim/types/chat/session_get_messages_params.py">params</a>) -> <a href="./src/evrim/types/chat/session_get_messages_response.py">SessionGetMessagesResponse</a></code>

## Messages

Types:

```python
from evrim.types.chat import Message
```

Methods:

- <code title="get /chat/messages/{id}">client.chat.messages.<a href="./src/evrim/resources/chat/messages.py">retrieve</a>(id) -> <a href="./src/evrim/types/chat/message.py">Message</a></code>
- <code title="post /chat/messages">client.chat.messages.<a href="./src/evrim/resources/chat/messages.py">send</a>(\*\*<a href="src/evrim/types/chat/message_send_params.py">params</a>) -> <a href="./src/evrim/types/chat/message.py">Message</a></code>

# Sources

Types:

```python
from evrim.types import Source, SourceListResponse
```

Methods:

- <code title="get /sources/{id}">client.sources.<a href="./src/evrim/resources/sources.py">retrieve</a>(id) -> <a href="./src/evrim/types/source.py">Source</a></code>
- <code title="get /sources">client.sources.<a href="./src/evrim/resources/sources.py">list</a>(\*\*<a href="src/evrim/types/source_list_params.py">params</a>) -> <a href="./src/evrim/types/source_list_response.py">SourceListResponse</a></code>

# Meetings

Types:

```python
from evrim.types import (
    MeetingDetails,
    MeetingSortField,
    OrganizationSnippet,
    ParticipantSnippet,
    SortOrder,
    SourceSnippet,
    MeetingListResponse,
)
```

Methods:

- <code title="get /meetings/{id}">client.meetings.<a href="./src/evrim/resources/meetings.py">retrieve</a>(id, \*\*<a href="src/evrim/types/meeting_retrieve_params.py">params</a>) -> <a href="./src/evrim/types/meeting_details.py">MeetingDetails</a></code>
- <code title="get /meetings">client.meetings.<a href="./src/evrim/resources/meetings.py">list</a>(\*\*<a href="src/evrim/types/meeting_list_params.py">params</a>) -> <a href="./src/evrim/types/meeting_list_response.py">MeetingListResponse</a></code>

# Participants

Types:

```python
from evrim.types import (
    Participant,
    ParticipantSortField,
    ParticipantListResponse,
    ParticipantListMeetingsResponse,
)
```

Methods:

- <code title="get /participants/{id}">client.participants.<a href="./src/evrim/resources/participants.py">retrieve</a>(id) -> <a href="./src/evrim/types/participant.py">Participant</a></code>
- <code title="get /participants">client.participants.<a href="./src/evrim/resources/participants.py">list</a>(\*\*<a href="src/evrim/types/participant_list_params.py">params</a>) -> <a href="./src/evrim/types/participant_list_response.py">ParticipantListResponse</a></code>
- <code title="get /participants/{id}/meetings">client.participants.<a href="./src/evrim/resources/participants.py">list_meetings</a>(id, \*\*<a href="src/evrim/types/participant_list_meetings_params.py">params</a>) -> <a href="./src/evrim/types/participant_list_meetings_response.py">ParticipantListMeetingsResponse</a></code>

# Organizations

Types:

```python
from evrim.types import (
    Organization,
    OrganizationSortField,
    OrganizationListResponse,
    OrganizationListMeetingsResponse,
)
```

Methods:

- <code title="get /organizations/{id}">client.organizations.<a href="./src/evrim/resources/organizations.py">retrieve</a>(id) -> <a href="./src/evrim/types/organization.py">Organization</a></code>
- <code title="get /organizations">client.organizations.<a href="./src/evrim/resources/organizations.py">list</a>(\*\*<a href="src/evrim/types/organization_list_params.py">params</a>) -> <a href="./src/evrim/types/organization_list_response.py">OrganizationListResponse</a></code>
- <code title="get /organizations/{id}/meetings">client.organizations.<a href="./src/evrim/resources/organizations.py">list_meetings</a>(id, \*\*<a href="src/evrim/types/organization_list_meetings_params.py">params</a>) -> <a href="./src/evrim/types/organization_list_meetings_response.py">OrganizationListMeetingsResponse</a></code>

# Locations

Types:

```python
from evrim.types import Location, LocationListResponse, LocationRetrieveMeetingsResponse
```

Methods:

- <code title="get /locations/{id}">client.locations.<a href="./src/evrim/resources/locations/locations.py">retrieve</a>(id) -> <a href="./src/evrim/types/location.py">Location</a></code>
- <code title="get /locations">client.locations.<a href="./src/evrim/resources/locations/locations.py">list</a>(\*\*<a href="src/evrim/types/location_list_params.py">params</a>) -> <a href="./src/evrim/types/location_list_response.py">LocationListResponse</a></code>
- <code title="get /locations/{id}/meetings">client.locations.<a href="./src/evrim/resources/locations/locations.py">retrieve_meetings</a>(id, \*\*<a href="src/evrim/types/location_retrieve_meetings_params.py">params</a>) -> <a href="./src/evrim/types/location_retrieve_meetings_response.py">LocationRetrieveMeetingsResponse</a></code>

## Search

Types:

```python
from evrim.types.locations import SearchByBboxResponse, SearchByRadiusResponse
```

Methods:

- <code title="get /locations/search/bbox">client.locations.search.<a href="./src/evrim/resources/locations/search/search.py">by_bbox</a>(\*\*<a href="src/evrim/types/locations/search_by_bbox_params.py">params</a>) -> <a href="./src/evrim/types/locations/search_by_bbox_response.py">SearchByBboxResponse</a></code>
- <code title="get /locations/search/radius">client.locations.search.<a href="./src/evrim/resources/locations/search/search.py">by_radius</a>(\*\*<a href="src/evrim/types/locations/search_by_radius_params.py">params</a>) -> <a href="./src/evrim/types/locations/search_by_radius_response.py">SearchByRadiusResponse</a></code>

### Admin1

Types:

```python
from evrim.types.locations.search import Admin1ListMeetingsResponse
```

Methods:

- <code title="get /locations/search/admin1/meetings">client.locations.search.admin1.<a href="./src/evrim/resources/locations/search/admin1.py">list_meetings</a>(\*\*<a href="src/evrim/types/locations/search/admin1_list_meetings_params.py">params</a>) -> <a href="./src/evrim/types/locations/search/admin1_list_meetings_response.py">Admin1ListMeetingsResponse</a></code>

# Documents

## Markdown

Types:

```python
from evrim.types.documents import Document, MarkdownListResponse
```

Methods:

- <code title="get /documents/markdown">client.documents.markdown.<a href="./src/evrim/resources/documents/markdown.py">list</a>(\*\*<a href="src/evrim/types/documents/markdown_list_params.py">params</a>) -> <a href="./src/evrim/types/documents/markdown_list_response.py">MarkdownListResponse</a></code>
- <code title="get /documents/markdown/by-url/{url}">client.documents.markdown.<a href="./src/evrim/resources/documents/markdown.py">retrieve_by_url</a>(url) -> <a href="./src/evrim/types/documents/document.py">Document</a></code>

## HTML

Types:

```python
from evrim.types.documents import HTMLDocument, HTMLListResponse
```

Methods:

- <code title="get /documents/html">client.documents.html.<a href="./src/evrim/resources/documents/html.py">list</a>(\*\*<a href="src/evrim/types/documents/html_list_params.py">params</a>) -> <a href="./src/evrim/types/documents/html_list_response.py">HTMLListResponse</a></code>
- <code title="get /documents/html/by-url/{url}">client.documents.html.<a href="./src/evrim/resources/documents/html.py">retrieve_by_url</a>(url) -> <a href="./src/evrim/types/documents/html_document.py">HTMLDocument</a></code>

# Relationships

Types:

```python
from evrim.types import Relationship, RelationshipListResponse
```

Methods:

- <code title="get /relationships/{id}">client.relationships.<a href="./src/evrim/resources/relationships.py">retrieve</a>(id) -> <a href="./src/evrim/types/relationship.py">Relationship</a></code>
- <code title="get /relationships">client.relationships.<a href="./src/evrim/resources/relationships.py">list</a>(\*\*<a href="src/evrim/types/relationship_list_params.py">params</a>) -> <a href="./src/evrim/types/relationship_list_response.py">RelationshipListResponse</a></code>

# Search

## Documents

Types:

```python
from evrim.types.search import DocumentSearchMarkdownResponse, DocumentSearchSemanticResponse
```

Methods:

- <code title="get /search/documents/markdown">client.search.documents.<a href="./src/evrim/resources/search/documents/documents.py">search_markdown</a>(\*\*<a href="src/evrim/types/search/document_search_markdown_params.py">params</a>) -> <a href="./src/evrim/types/search/document_search_markdown_response.py">DocumentSearchMarkdownResponse</a></code>
- <code title="get /search/documents/semantic">client.search.documents.<a href="./src/evrim/resources/search/documents/documents.py">search_semantic</a>(\*\*<a href="src/evrim/types/search/document_search_semantic_params.py">params</a>) -> <a href="./src/evrim/types/search/document_search_semantic_response.py">DocumentSearchSemanticResponse</a></code>

### HTML

Types:

```python
from evrim.types.search.documents import (
    HTMLSearchResponse,
    HTMLSearchByDomainResponse,
    HTMLSearchByURLResponse,
)
```

Methods:

- <code title="get /search/documents/html">client.search.documents.html.<a href="./src/evrim/resources/search/documents/html.py">search</a>(\*\*<a href="src/evrim/types/search/documents/html_search_params.py">params</a>) -> <a href="./src/evrim/types/search/documents/html_search_response.py">HTMLSearchResponse</a></code>
- <code title="get /search/documents/html/by-domain">client.search.documents.html.<a href="./src/evrim/resources/search/documents/html.py">search_by_domain</a>(\*\*<a href="src/evrim/types/search/documents/html_search_by_domain_params.py">params</a>) -> <a href="./src/evrim/types/search/documents/html_search_by_domain_response.py">HTMLSearchByDomainResponse</a></code>
- <code title="get /search/documents/html/by-url">client.search.documents.html.<a href="./src/evrim/resources/search/documents/html.py">search_by_url</a>(\*\*<a href="src/evrim/types/search/documents/html_search_by_url_params.py">params</a>) -> <a href="./src/evrim/types/search/documents/html_search_by_url_response.py">HTMLSearchByURLResponse</a></code>

## Organizations

Types:

```python
from evrim.types.search import OrganizationSearchResponse, OrganizationSearchSemanticResponse
```

Methods:

- <code title="get /search/organizations">client.search.organizations.<a href="./src/evrim/resources/search/organizations.py">search</a>(\*\*<a href="src/evrim/types/search/organization_search_params.py">params</a>) -> <a href="./src/evrim/types/search/organization_search_response.py">OrganizationSearchResponse</a></code>
- <code title="get /search/organizations/semantic">client.search.organizations.<a href="./src/evrim/resources/search/organizations.py">search_semantic</a>(\*\*<a href="src/evrim/types/search/organization_search_semantic_params.py">params</a>) -> <a href="./src/evrim/types/search/organization_search_semantic_response.py">OrganizationSearchSemanticResponse</a></code>

## Participants

Types:

```python
from evrim.types.search import ParticipantSearchResponse, ParticipantSearchSemanticResponse
```

Methods:

- <code title="get /search/participants">client.search.participants.<a href="./src/evrim/resources/search/participants.py">search</a>(\*\*<a href="src/evrim/types/search/participant_search_params.py">params</a>) -> <a href="./src/evrim/types/search/participant_search_response.py">ParticipantSearchResponse</a></code>
- <code title="get /search/participants/semantic">client.search.participants.<a href="./src/evrim/resources/search/participants.py">search_semantic</a>(\*\*<a href="src/evrim/types/search/participant_search_semantic_params.py">params</a>) -> <a href="./src/evrim/types/search/participant_search_semantic_response.py">ParticipantSearchSemanticResponse</a></code>

## Meetings

### Topic

Types:

```python
from evrim.types.search.meetings import (
    SemanticMeetingSearchResult,
    TopicSearchResponse,
    TopicSearchSemanticResponse,
)
```

Methods:

- <code title="get /search/meetings/topic">client.search.meetings.topic.<a href="./src/evrim/resources/search/meetings/topic.py">search</a>(\*\*<a href="src/evrim/types/search/meetings/topic_search_params.py">params</a>) -> <a href="./src/evrim/types/search/meetings/topic_search_response.py">TopicSearchResponse</a></code>
- <code title="get /search/meetings/topic/semantic">client.search.meetings.topic.<a href="./src/evrim/resources/search/meetings/topic.py">search_semantic</a>(\*\*<a href="src/evrim/types/search/meetings/topic_search_semantic_params.py">params</a>) -> <a href="./src/evrim/types/search/meetings/topic_search_semantic_response.py">TopicSearchSemanticResponse</a></code>

### Summary

Types:

```python
from evrim.types.search.meetings import SummarySearchResponse, SummarySearchSemanticResponse
```

Methods:

- <code title="get /search/meetings/summary">client.search.meetings.summary.<a href="./src/evrim/resources/search/meetings/summary.py">search</a>(\*\*<a href="src/evrim/types/search/meetings/summary_search_params.py">params</a>) -> <a href="./src/evrim/types/search/meetings/summary_search_response.py">SummarySearchResponse</a></code>
- <code title="get /search/meetings/summary/semantic">client.search.meetings.summary.<a href="./src/evrim/resources/search/meetings/summary.py">search_semantic</a>(\*\*<a href="src/evrim/types/search/meetings/summary_search_semantic_params.py">params</a>) -> <a href="./src/evrim/types/search/meetings/summary_search_semantic_response.py">SummarySearchSemanticResponse</a></code>

# Emails

Types:

```python
from evrim.types import Email, EmailListResponse
```

Methods:

- <code title="get /emails/{id}">client.emails.<a href="./src/evrim/resources/emails/emails.py">retrieve</a>(id) -> <a href="./src/evrim/types/email.py">Email</a></code>
- <code title="get /emails">client.emails.<a href="./src/evrim/resources/emails/emails.py">list</a>(\*\*<a href="src/evrim/types/email_list_params.py">params</a>) -> <a href="./src/evrim/types/email_list_response.py">EmailListResponse</a></code>

## Search

Types:

```python
from evrim.types.emails import (
    SearchByDomainResponse,
    SearchBySlugResponse,
    SearchBySourceDomainResponse,
)
```

Methods:

- <code title="get /emails/search/domain">client.emails.search.<a href="./src/evrim/resources/emails/search.py">by_domain</a>(\*\*<a href="src/evrim/types/emails/search_by_domain_params.py">params</a>) -> <a href="./src/evrim/types/emails/search_by_domain_response.py">SearchByDomainResponse</a></code>
- <code title="get /emails/search/slug">client.emails.search.<a href="./src/evrim/resources/emails/search.py">by_slug</a>(\*\*<a href="src/evrim/types/emails/search_by_slug_params.py">params</a>) -> <a href="./src/evrim/types/emails/search_by_slug_response.py">SearchBySlugResponse</a></code>
- <code title="get /emails/search/source-domain">client.emails.search.<a href="./src/evrim/resources/emails/search.py">by_source_domain</a>(\*\*<a href="src/evrim/types/emails/search_by_source_domain_params.py">params</a>) -> <a href="./src/evrim/types/emails/search_by_source_domain_response.py">SearchBySourceDomainResponse</a></code>

# Phones

Types:

```python
from evrim.types import Phone, PhoneListResponse
```

Methods:

- <code title="get /phones/{id}">client.phones.<a href="./src/evrim/resources/phones/phones.py">retrieve</a>(id) -> <a href="./src/evrim/types/phone.py">Phone</a></code>
- <code title="get /phones">client.phones.<a href="./src/evrim/resources/phones/phones.py">list</a>(\*\*<a href="src/evrim/types/phone_list_params.py">params</a>) -> <a href="./src/evrim/types/phone_list_response.py">PhoneListResponse</a></code>

## Search

Types:

```python
from evrim.types.phones import SearchByDomainResponse, SearchQueryResponse
```

Methods:

- <code title="get /phones/search/source-domain">client.phones.search.<a href="./src/evrim/resources/phones/search.py">by_domain</a>(\*\*<a href="src/evrim/types/phones/search_by_domain_params.py">params</a>) -> <a href="./src/evrim/types/phones/search_by_domain_response.py">SearchByDomainResponse</a></code>
- <code title="get /phones/search">client.phones.search.<a href="./src/evrim/resources/phones/search.py">query</a>(\*\*<a href="src/evrim/types/phones/search_query_params.py">params</a>) -> <a href="./src/evrim/types/phones/search_query_response.py">SearchQueryResponse</a></code>

# Wechat

Types:

```python
from evrim.types import Wechat, WechatListResponse
```

Methods:

- <code title="get /wechat/{id}">client.wechat.<a href="./src/evrim/resources/wechat/wechat.py">retrieve</a>(id) -> <a href="./src/evrim/types/wechat/wechat.py">Wechat</a></code>
- <code title="get /wechat">client.wechat.<a href="./src/evrim/resources/wechat/wechat.py">list</a>(\*\*<a href="src/evrim/types/wechat_list_params.py">params</a>) -> <a href="./src/evrim/types/wechat_list_response.py">WechatListResponse</a></code>

## Search

Types:

```python
from evrim.types.wechat import SearchBySourceDomainResponse
```

Methods:

- <code title="get /wechat/search/source-domain">client.wechat.search.<a href="./src/evrim/resources/wechat/search.py">by_source_domain</a>(\*\*<a href="src/evrim/types/wechat/search_by_source_domain_params.py">params</a>) -> <a href="./src/evrim/types/wechat/search_by_source_domain_response.py">SearchBySourceDomainResponse</a></code>

# Weibo

Types:

```python
from evrim.types import Weibo, WeiboListResponse
```

Methods:

- <code title="get /weibo/{id}">client.weibo.<a href="./src/evrim/resources/weibo/weibo.py">retrieve</a>(id) -> <a href="./src/evrim/types/weibo/weibo.py">Weibo</a></code>
- <code title="get /weibo">client.weibo.<a href="./src/evrim/resources/weibo/weibo.py">list</a>(\*\*<a href="src/evrim/types/weibo_list_params.py">params</a>) -> <a href="./src/evrim/types/weibo_list_response.py">WeiboListResponse</a></code>

## Search

Types:

```python
from evrim.types.weibo import SearchBySourceDomainResponse
```

Methods:

- <code title="get /weibo/search/source-domain">client.weibo.search.<a href="./src/evrim/resources/weibo/search.py">by_source_domain</a>(\*\*<a href="src/evrim/types/weibo/search_by_source_domain_params.py">params</a>) -> <a href="./src/evrim/types/weibo/search_by_source_domain_response.py">SearchBySourceDomainResponse</a></code>

# Douyin

Types:

```python
from evrim.types import Douyin, DouyinListResponse
```

Methods:

- <code title="get /douyin/{id}">client.douyin.<a href="./src/evrim/resources/douyin/douyin.py">retrieve</a>(id) -> <a href="./src/evrim/types/douyin/douyin.py">Douyin</a></code>
- <code title="get /douyin">client.douyin.<a href="./src/evrim/resources/douyin/douyin.py">list</a>(\*\*<a href="src/evrim/types/douyin_list_params.py">params</a>) -> <a href="./src/evrim/types/douyin_list_response.py">DouyinListResponse</a></code>

## Search

Types:

```python
from evrim.types.douyin import SearchBySourceDomainResponse
```

Methods:

- <code title="get /douyin/search/source-domain">client.douyin.search.<a href="./src/evrim/resources/douyin/search.py">by_source_domain</a>(\*\*<a href="src/evrim/types/douyin/search_by_source_domain_params.py">params</a>) -> <a href="./src/evrim/types/douyin/search_by_source_domain_response.py">SearchBySourceDomainResponse</a></code>

# Bilibili

Types:

```python
from evrim.types import Bilibili, BilibiliListResponse
```

Methods:

- <code title="get /bilibili/{id}">client.bilibili.<a href="./src/evrim/resources/bilibili/bilibili.py">retrieve</a>(id) -> <a href="./src/evrim/types/bilibili/bilibili.py">Bilibili</a></code>
- <code title="get /bilibili">client.bilibili.<a href="./src/evrim/resources/bilibili/bilibili.py">list</a>(\*\*<a href="src/evrim/types/bilibili_list_params.py">params</a>) -> <a href="./src/evrim/types/bilibili_list_response.py">BilibiliListResponse</a></code>

## Search

Types:

```python
from evrim.types.bilibili import SearchBySourceDomainResponse
```

Methods:

- <code title="get /bilibili/search/source-domain">client.bilibili.search.<a href="./src/evrim/resources/bilibili/search.py">by_source_domain</a>(\*\*<a href="src/evrim/types/bilibili/search_by_source_domain_params.py">params</a>) -> <a href="./src/evrim/types/bilibili/search_by_source_domain_response.py">SearchBySourceDomainResponse</a></code>

# Zhihu

Types:

```python
from evrim.types import Zhihu, ZhihuListResponse
```

Methods:

- <code title="get /zhihu/{id}">client.zhihu.<a href="./src/evrim/resources/zhihu/zhihu.py">retrieve</a>(id) -> <a href="./src/evrim/types/zhihu/zhihu.py">Zhihu</a></code>
- <code title="get /zhihu">client.zhihu.<a href="./src/evrim/resources/zhihu/zhihu.py">list</a>(\*\*<a href="src/evrim/types/zhihu_list_params.py">params</a>) -> <a href="./src/evrim/types/zhihu_list_response.py">ZhihuListResponse</a></code>

## Search

Types:

```python
from evrim.types.zhihu import SearchBySourceDomainResponse
```

Methods:

- <code title="get /zhihu/search/source-domain">client.zhihu.search.<a href="./src/evrim/resources/zhihu/search.py">by_source_domain</a>(\*\*<a href="src/evrim/types/zhihu/search_by_source_domain_params.py">params</a>) -> <a href="./src/evrim/types/zhihu/search_by_source_domain_response.py">SearchBySourceDomainResponse</a></code>

# Qq

Types:

```python
from evrim.types import Qq, QqListResponse
```

Methods:

- <code title="get /qq/{id}">client.qq.<a href="./src/evrim/resources/qq/qq.py">retrieve</a>(id) -> <a href="./src/evrim/types/qq/qq.py">Qq</a></code>
- <code title="get /qq">client.qq.<a href="./src/evrim/resources/qq/qq.py">list</a>(\*\*<a href="src/evrim/types/qq_list_params.py">params</a>) -> <a href="./src/evrim/types/qq_list_response.py">QqListResponse</a></code>

## Search

Types:

```python
from evrim.types.qq import SearchBySourceDomainResponse
```

Methods:

- <code title="get /qq/search/source-domain">client.qq.search.<a href="./src/evrim/resources/qq/search.py">by_source_domain</a>(\*\*<a href="src/evrim/types/qq/search_by_source_domain_params.py">params</a>) -> <a href="./src/evrim/types/qq/search_by_source_domain_response.py">SearchBySourceDomainResponse</a></code>

# Health

Methods:

- <code title="get /health">client.health.<a href="./src/evrim/resources/health.py">check</a>() -> object</code>

# Auth

Types:

```python
from evrim.types import AuthResponse
```

Methods:

- <code title="post /auth/token">client.auth.<a href="./src/evrim/resources/auth/auth.py">get_token</a>(\*\*<a href="src/evrim/types/auth_get_token_params.py">params</a>) -> <a href="./src/evrim/types/auth_response.py">AuthResponse</a></code>
- <code title="post /auth/refresh">client.auth.<a href="./src/evrim/resources/auth/auth.py">refresh_token</a>(\*\*<a href="src/evrim/types/auth_refresh_token_params.py">params</a>) -> <a href="./src/evrim/types/auth_response.py">AuthResponse</a></code>

## McpTokens

Types:

```python
from evrim.types.auth import McpTokenCreateResponse, McpTokenListResponse
```

Methods:

- <code title="post /auth/mcp-tokens">client.auth.mcp_tokens.<a href="./src/evrim/resources/auth/mcp_tokens.py">create</a>(\*\*<a href="src/evrim/types/auth/mcp_token_create_params.py">params</a>) -> <a href="./src/evrim/types/auth/mcp_token_create_response.py">McpTokenCreateResponse</a></code>
- <code title="get /auth/mcp-tokens">client.auth.mcp_tokens.<a href="./src/evrim/resources/auth/mcp_tokens.py">list</a>(\*\*<a href="src/evrim/types/auth/mcp_token_list_params.py">params</a>) -> <a href="./src/evrim/types/auth/mcp_token_list_response.py">McpTokenListResponse</a></code>
- <code title="delete /auth/mcp-tokens/{token_id}">client.auth.mcp_tokens.<a href="./src/evrim/resources/auth/mcp_tokens.py">revoke</a>(token_id) -> object</code>

# Technology

## Communities

Types:

```python
from evrim.types.technology import (
    CommunitySortField,
    PublicationSortField,
    TechnologyCommunity,
    TechnologyTopic,
    TopicSortField,
    CommunityRetrieveResponse,
    CommunityListResponse,
    CommunityGetMeetingsResponse,
    CommunityGetNeighborsResponse,
    CommunityGetPublicationsResponse,
    CommunityGetTopicsResponse,
    CommunitySearchResponse,
)
```

Methods:

- <code title="get /technology/communities/{community_id}">client.technology.communities.<a href="./src/evrim/resources/technology/communities.py">retrieve</a>(community_id) -> <a href="./src/evrim/types/technology/community_retrieve_response.py">CommunityRetrieveResponse</a></code>
- <code title="get /technology/communities">client.technology.communities.<a href="./src/evrim/resources/technology/communities.py">list</a>(\*\*<a href="src/evrim/types/technology/community_list_params.py">params</a>) -> <a href="./src/evrim/types/technology/community_list_response.py">CommunityListResponse</a></code>
- <code title="get /technology/communities/{community_id}/meetings">client.technology.communities.<a href="./src/evrim/resources/technology/communities.py">get_meetings</a>(community_id, \*\*<a href="src/evrim/types/technology/community_get_meetings_params.py">params</a>) -> <a href="./src/evrim/types/technology/community_get_meetings_response.py">CommunityGetMeetingsResponse</a></code>
- <code title="get /technology/communities/{community_id}/neighbors">client.technology.communities.<a href="./src/evrim/resources/technology/communities.py">get_neighbors</a>(community_id, \*\*<a href="src/evrim/types/technology/community_get_neighbors_params.py">params</a>) -> <a href="./src/evrim/types/technology/community_get_neighbors_response.py">CommunityGetNeighborsResponse</a></code>
- <code title="get /technology/communities/{community_id}/publications">client.technology.communities.<a href="./src/evrim/resources/technology/communities.py">get_publications</a>(community_id, \*\*<a href="src/evrim/types/technology/community_get_publications_params.py">params</a>) -> <a href="./src/evrim/types/technology/community_get_publications_response.py">CommunityGetPublicationsResponse</a></code>
- <code title="get /technology/communities/{community_id}/topics">client.technology.communities.<a href="./src/evrim/resources/technology/communities.py">get_topics</a>(community_id, \*\*<a href="src/evrim/types/technology/community_get_topics_params.py">params</a>) -> <a href="./src/evrim/types/technology/community_get_topics_response.py">CommunityGetTopicsResponse</a></code>
- <code title="get /technology/communities/search">client.technology.communities.<a href="./src/evrim/resources/technology/communities.py">search</a>(\*\*<a href="src/evrim/types/technology/community_search_params.py">params</a>) -> <a href="./src/evrim/types/technology/community_search_response.py">CommunitySearchResponse</a></code>

## Topics

Types:

```python
from evrim.types.technology import (
    TopicRetrieveResponse,
    TopicGetPublicationsResponse,
    TopicGetSimilarTopicsResponse,
    TopicSearchResponse,
)
```

Methods:

- <code title="get /technology/topics/{topic_id}">client.technology.topics.<a href="./src/evrim/resources/technology/topics.py">retrieve</a>(topic_id) -> <a href="./src/evrim/types/technology/topic_retrieve_response.py">TopicRetrieveResponse</a></code>
- <code title="get /technology/topics/{topic_id}/publications">client.technology.topics.<a href="./src/evrim/resources/technology/topics.py">get_publications</a>(topic_id, \*\*<a href="src/evrim/types/technology/topic_get_publications_params.py">params</a>) -> <a href="./src/evrim/types/technology/topic_get_publications_response.py">TopicGetPublicationsResponse</a></code>
- <code title="get /technology/topics/{topic_id}/similar-topics">client.technology.topics.<a href="./src/evrim/resources/technology/topics.py">get_similar_topics</a>(topic_id, \*\*<a href="src/evrim/types/technology/topic_get_similar_topics_params.py">params</a>) -> <a href="./src/evrim/types/technology/topic_get_similar_topics_response.py">TopicGetSimilarTopicsResponse</a></code>
- <code title="get /technology/topics/search">client.technology.topics.<a href="./src/evrim/resources/technology/topics.py">search</a>(\*\*<a href="src/evrim/types/technology/topic_search_params.py">params</a>) -> <a href="./src/evrim/types/technology/topic_search_response.py">TopicSearchResponse</a></code>

## Publications

Types:

```python
from evrim.types.technology import (
    TechnologyPublication,
    PublicationGetTopicsResponse,
    PublicationSearchResponse,
)
```

Methods:

- <code title="get /technology/publications/{publication_id}">client.technology.publications.<a href="./src/evrim/resources/technology/publications.py">retrieve</a>(publication_id) -> <a href="./src/evrim/types/technology/technology_publication.py">TechnologyPublication</a></code>
- <code title="get /technology/publications/{publication_id}/topics">client.technology.publications.<a href="./src/evrim/resources/technology/publications.py">get_topics</a>(publication_id, \*\*<a href="src/evrim/types/technology/publication_get_topics_params.py">params</a>) -> <a href="./src/evrim/types/technology/publication_get_topics_response.py">PublicationGetTopicsResponse</a></code>
- <code title="get /technology/publications/search">client.technology.publications.<a href="./src/evrim/resources/technology/publications.py">search</a>(\*\*<a href="src/evrim/types/technology/publication_search_params.py">params</a>) -> <a href="./src/evrim/types/technology/publication_search_response.py">PublicationSearchResponse</a></code>

## Graph

Types:

```python
from evrim.types.technology import (
    GraphFindPathResponse,
    GraphGetOverlapResponse,
    GraphGetSubgraphResponse,
)
```

Methods:

- <code title="get /technology/graph/path">client.technology.graph.<a href="./src/evrim/resources/technology/graph.py">find_path</a>(\*\*<a href="src/evrim/types/technology/graph_find_path_params.py">params</a>) -> <a href="./src/evrim/types/technology/graph_find_path_response.py">GraphFindPathResponse</a></code>
- <code title="get /technology/graph/overlap">client.technology.graph.<a href="./src/evrim/resources/technology/graph.py">get_overlap</a>(\*\*<a href="src/evrim/types/technology/graph_get_overlap_params.py">params</a>) -> <a href="./src/evrim/types/technology/graph_get_overlap_response.py">GraphGetOverlapResponse</a></code>
- <code title="get /technology/graph/subgraph">client.technology.graph.<a href="./src/evrim/resources/technology/graph.py">get_subgraph</a>(\*\*<a href="src/evrim/types/technology/graph_get_subgraph_params.py">params</a>) -> <a href="./src/evrim/types/technology/graph_get_subgraph_response.py">GraphGetSubgraphResponse</a></code>

## Analytics

Types:

```python
from evrim.types.technology import AnalyticsGetCommunityStatsResponse
```

Methods:

- <code title="get /technology/analytics/community-stats/{community_id}">client.technology.analytics.<a href="./src/evrim/resources/technology/analytics.py">get_community_stats</a>(community_id) -> <a href="./src/evrim/types/technology/analytics_get_community_stats_response.py">AnalyticsGetCommunityStatsResponse</a></code>

## Meetings

Types:

```python
from evrim.types.technology import MeetingGetCommunitiesResponse
```

Methods:

- <code title="get /technology/meetings/{meeting_id}/communities">client.technology.meetings.<a href="./src/evrim/resources/technology/meetings.py">get_communities</a>(meeting_id, \*\*<a href="src/evrim/types/technology/meeting_get_communities_params.py">params</a>) -> <a href="./src/evrim/types/technology/meeting_get_communities_response.py">MeetingGetCommunitiesResponse</a></code>
