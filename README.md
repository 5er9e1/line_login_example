# Line login example

### OAuth v2.1 2022/04/08

### Related links:

- [Line login flow and explanation](https://developers.line.biz/en/docs/line-login/integrate-line-login/)
- [How to get profile information](https://developers.line.biz/en/docs/line-login/verify-id-token)
- [Profile information payload explanation](https://developers.line.biz/en/docs/line-login/verify-id-token/#payload) 

### Environment variables

|Name|Explanation|
|--|--|
|`CHANNEL_ID`|[Line App](https://developers.line.biz/en/docs/messaging-api/getting-started/) channel id|
|`CHANNEL_SECRET`|Line App channel secret|
|`CALLBACK_URL`|Callback URL for your web service (also redirect URL)|
|`LINE_LOGIN_URL`|URL to redirect user request to Line login page|
|`AUTH_TOKEN_URL`|URL to get token to be able get profile data|
|`LINE_PROFILE_URL`|URL to get user profile data|
|`SCOPE`|Determines [what profile data](https://developers.line.biz/en/docs/line-login/integrate-line-login/#scopes) allowed to be taken|