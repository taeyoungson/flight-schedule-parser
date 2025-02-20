# Flight schedule parser

## Set environment variables
Put the following in one of the [`.env`, `.env.dev`] file in the root directory.

Kakao API,
```bash
KAKAO_API_KEY=Your-Kakao-REST-Api-Key
KAKAO_REDIRECT_URI=Your-Kakao-Redirect-URI
KAKAO_AUTH_CODE=Your-Kakao-Auth-Code
```

for KAKAO_AUTH_CODE, set kakao_api_key and redirect_uri first,

then you can get it by running the following from command line.

```bash
make get-kakao-auth-code
```


for Google API,
```bash
GOOGLE_EMAIL=Your-Google-Email
GOOGLE_CALENDAR_ID=Your-Google-Calendar-ID
GOOGLE_TOKEN=Your-Google-Token
GOOGLE_TOKEN_URI=Your-Google-Token-URI
GOOGLE_CLIENT_ID=Your-Google-Client-ID
GOOGLE_CLIENT_SECRET=Your-Google-Client-Secret
GOOGLE_REFRESH_TOKEN=Your-Google-Refresh-Token
```
