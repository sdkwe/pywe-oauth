# -*- coding: utf-8 -*-

import shortuuid
from pywe_base import BaseWechat
from six.moves import urllib_parse


class Oauth(BaseWechat):
    def __init__(self):
        super(Oauth, self).__init__()
        # 网页授权获取用户基本信息, Refer: http://mp.weixin.qq.com/wiki/17/c0f37d5704f0b64713d5d2c37b468d75.html
        # 移动应用微信登录开发指南, Refer: https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&t=resource/res_list&verify=1&id=open1419317851&token=&lang=zh_CN
        self.WECHAT_OAUTH2_AUTHORIZE = self.OPEN_DOMAIN + '/connect/oauth2/authorize?appid={appid}&redirect_uri={redirect_uri}&response_type=code&scope={scope}&state={state}&forcePopup={forcePopup}#wechat_redirect'
        self.WECHAT_OAUTH2_ACCESS_TOKEN = self.API_DOMAIN + '/sns/oauth2/access_token?appid={appid}&secret={secret}&code={code}&grant_type=authorization_code'
        self.WECHAT_OAUTH2_USERINFO = self.API_DOMAIN + '/sns/userinfo?access_token={access_token}&openid={openid}'
        # 第三方平台代公众号发起网页授权, https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&t=resource/res_list&verify=1&id=open1419318590&token=&lang=zh_CN
        self.WECHAT_COMPONENT_OAUTH2_AUTHORIZE = self.OPEN_DOMAIN + '/connect/oauth2/authorize?appid={appid}&redirect_uri={redirect_uri}&response_type=code&scope={scope}&state={state}&component_appid={component_appid}#wechat_redirect'
        self.WECHAT_COMPONENT_OAUTH2_ACCESS_TOKEN = self.API_DOMAIN + '/sns/oauth2/component/access_token?appid={appid}&code={code}&grant_type=authorization_code&component_appid={component_appid}&component_access_token={component_access_token}'
        self.WECHAT_COMPONENT_OAUTH2_USERINFO = self.API_DOMAIN + '/sns/userinfo?access_token={access_token}&openid={openid}&lang=zh_CN'

    def get_oauth_code_url(self, appid=None, redirect_uri=None, scope='snsapi_base', redirect_url=None, component=False, component_appid=None, force_popup=False):
        if component:
            return self.get_component_oauth_code_url(appid=appid, redirect_uri=redirect_uri, scope=scope, redirect_url=redirect_url, component_appid=component_appid)
        return self.WECHAT_OAUTH2_AUTHORIZE.format(
            appid=appid,
            redirect_uri=urllib_parse.quote_plus(redirect_uri),
            scope=scope,
            state=urllib_parse.quote_plus(redirect_url),
            forcePopup='true' if force_popup else 'false',
        )

    def get_access_info(self, appid=None, secret=None, code=None, component=False, component_appid=None, component_access_token=None):
        if component:
            return self.get_component_access_info(appid=appid, code=code, component_appid=component_appid, component_access_token=component_access_token)
        return self.get(self.WECHAT_OAUTH2_ACCESS_TOKEN, appid=appid, secret=secret, code=code)

    def get_userinfo(self, access_token=None, openid=None, component=False):
        if component:
            return self.get_component_userinfo(access_token=access_token, openid=openid)
        return self.get(self.WECHAT_OAUTH2_USERINFO, access_token=access_token, openid=openid)

    def get_component_oauth_code_url(self, appid=None, redirect_uri=None, scope='snsapi_base', redirect_url=None, component_appid=None):
        return self.WECHAT_COMPONENT_OAUTH2_AUTHORIZE.format(
            appid=appid,
            redirect_uri=urllib_parse.quote_plus(redirect_uri),
            scope=scope,
            state=urllib_parse.quote_plus(redirect_url),
            component_appid=component_appid,
        )

    def get_component_access_info(self, appid=None, code=None, component_appid=None, component_access_token=None):
        return self.get(self.WECHAT_COMPONENT_OAUTH2_ACCESS_TOKEN, appid=appid, code=code, component_appid=component_appid, component_access_token=component_access_token)

    def get_component_userinfo(self, access_token=None, openid=None):
        return self.get(self.WECHAT_COMPONENT_OAUTH2_USERINFO, access_token=access_token, openid=openid)

    def get_oauth_redirect_url(self, oauth_uri, scope='snsapi_base', redirect_url=None, default_url=None, direct_redirect=None, force_popup=None, random_str=True):
        """
        # https://a.com/wx/oauth2?redirect_url=redirect_url
        # https://a.com/wx/oauth2?redirect_url=redirect_url&default_url=default_url
        # https://a.com/wx/oauth2?scope=snsapi_base&redirect_url=redirect_url
        # https://a.com/wx/oauth2?scope=snsapi_base&redirect_url=redirect_url&default_url=default_url
        # https://a.com/wx/oauth2?scope=snsapi_base&redirect_url=redirect_url&default_url=default_url&direct_redirect=true
        # https://a.com/wx/oauth2?scope=snsapi_base&redirect_url=redirect_url&default_url=default_url&direct_redirect=true&force_popup=true

        # https://a.com/wx/o?r=redirect_url
        # https://a.com/wx/o?r=redirect_url&d=default_url
        # https://a.com/wx/o?s=snsapi_base&r=redirect_url
        # https://a.com/wx/o?s=snsapi_base&r=redirect_url&d=default_url
        # https://a.com/wx/o?s=snsapi_base&r=redirect_url&d=default_url&dr=true
        # https://a.com/wx/o?s=snsapi_base&r=redirect_url&d=default_url&dr=true&fp=true
        """
        oauth_url = oauth_uri.format(scope, urllib_parse.quote_plus(redirect_url), urllib_parse.quote_plus(default_url)) if default_url else oauth_uri.format(scope, urllib_parse.quote_plus(redirect_url))
        oauth_url = '{0}&dr=true'.format(oauth_url) if direct_redirect else oauth_url
        oauth_url = '{0}&fp=true'.format(oauth_url) if force_popup else oauth_url
        oauth_url = '{0}&rs={1}'.format(oauth_url, shortuuid.uuid()) if random_str else oauth_url
        return oauth_url


oauth = Oauth()
get_oauth_code_url = oauth.get_oauth_code_url
get_access_info = oauth.get_access_info
get_userinfo = oauth.get_userinfo
get_component_oauth_code_url = oauth.get_component_oauth_code_url
get_component_access_info = oauth.get_component_access_info
get_component_userinfo = oauth.get_component_userinfo
get_oauth_redirect_url = oauth.get_oauth_redirect_url
