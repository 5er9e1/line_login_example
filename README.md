# Line login example

### OAuth v2.1 2022/04/08

This WEB app using Line login system and print out Line profile information after successfull login

### Related links:

- [Line login flow and explanation](https://developers.line.biz/en/docs/line-login/integrate-line-login/)
- [How to get profile information](https://developers.line.biz/en/docs/line-login/verify-id-token)
- [Profile information payload explanation](https://developers.line.biz/en/docs/line-login/verify-id-token/#payload) 

### Environment variables

|Name|Default|Explanation|
|--|--|--|
|`CHANNEL_ID`|Must be set|[Line App](https://developers.line.biz/en/docs/messaging-api/getting-started/) channel id|
|`CHANNEL_SECRET`|Must be set|Line App channel secret|x|
|`CALLBACK_URL`|`http://localhost:8080/callback`|Callback URL for your web service (also redirect URL)|v|
|`LINE_LOGIN_URL`|`https://access.line.me/oauth2/v2.1/authorize`|URL to redirect user request to Line login page|v|
|`AUTH_TOKEN_URL`|`https://api.line.me/oauth2/v2.1/token`|URL to get token to be able get profile data|v|
|`LINE_PROFILE_URL`|`https://api.line.me/oauth2/v2.1/verify`|URL to get user profile data|v|
|`SCOPE`|`openid`|Determines [what profile data](https://developers.line.biz/en/docs/line-login/integrate-line-login/#scopes) allowed to be taken|
|`APP_SECRET`|random UUID|Application secret key to be able generate sessions|