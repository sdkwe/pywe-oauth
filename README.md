# pywe-oauth

Wechat Oauth Module for Python.

# Installation

```shell
pip install pywe-oauth
```

# Usage

```python
from pywe_oauth import get_access_info, get_oauth_code_url, get_userinfo
```

# Method

```python
def get_oauth_code_url(self, appid=None, redirect_uri=None, scope='snsapi_base', redirect_url=None):

def get_access_info(self, appid=None, secret=None, code=None):

def get_userinfo(self, access_token=None, openid=None):
```

# Examples

* Django

  * settings.py
    ```python
    # Wechat Settings
    WECHAT = {
        'JSAPI': {
            'token': '5201314',
            'appID': '',
            'appsecret': '',
            'mchID': '',
            'apiKey': '',
            'mch_cert': '',
            'mch_key': '',
            'redpacket': {
                'SEND_NAME': '',
                'NICK_NAME': '',
                'ACT_NAME': '',
                'WISHING': '',
                'REMARK': '',
            }
        },
    }

    WECHAT_BASE_REDIRECT_URI = 'https://wx.com/base_redirect'
    WECHAT_USERINFO_REDIRECT_URI = 'https://wx.com/userinfo_redirect'
    WECHAT_OAUTH2_RETRY_REDIRECT_URI = 'https://wx.com/wx_oauth2?redirect_url={}'
    ```

  * views.py
    ```python
    # -*- coding: utf-8 -*-

    from django.conf import settings
    from django.shortcuts import redirect
    from furl import furl
    from pywe_oauth import get_access_info, get_oauth_code_url, get_userinfo


    JSAPI = settings.WECHAT.get('JSAPI', {})


    def wx_oauth2(request):
        scope = request.GET.get('scope', 'snsapi_userinfo')
        redirect_url = request.GET.get('redirect_url', '')
        default_url = request.GET.get('default_url', '')

        if request.weixin:
            redirect_uri = settings.WECHAT_USERINFO_REDIRECT_URI if scope == 'snsapi_userinfo' else settings.WECHAT_BASE_REDIRECT_URI
            return redirect(get_oauth_code_url(JSAPI['appID'], redirect_uri, scope, redirect_url))

        return redirect(default_url or redirect_url)


    def base_redirect(request):
        """ snsapi_base cannot get unionid and userinfo """
        code = request.GET.get('code', '')
        state = request.GET.get('state', '')

        access_info = get_access_info(JSAPI['appID'], JSAPI['appsecret'], code)
        if 'errcode' in access_info:
            return redirect(settings.WECHAT_OAUTH2_RETRY_REDIRECT_URI.format(state))

        return redirect(furl(state).add(access_info).url)


    def userinfo_redirect(request):
        code = request.GET.get('code', '')
        state = request.GET.get('state', '')

        access_info = get_access_info(JSAPI['appID'], JSAPI['appsecret'], code)
        if 'errcode' in access_info:
            return redirect(settings.WECHAT_OAUTH2_RETRY_REDIRECT_URI.format(state))

        userinfo = get_userinfo(access_info.get('access_token', ''), access_info.get('openid', ''))
        if 'openid' not in userinfo:
            return redirect(settings.WECHAT_OAUTH2_RETRY_REDIRECT_URI.format(state))

        return redirect(furl(state).add(userinfo).url)
    ```
