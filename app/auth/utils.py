import ssl
from urllib.parse import urlparse

from flask import current_app
from ldap3 import Connection, Server, Tls
from app.utils.onelogin.saml2.auth import OneLogin_Saml2_Auth
from app.utils.onelogin.saml2.utils import OneLogin_Saml2_Utils


def ldap_authentication(email, password):
    """
    Authenticate the provided user with an LDAP Server.
    :param email: Users username
    :param password: Users password
    :return: Boolean
    """
    conn = _ldap_server_connect()

    users = conn.search(search_base=current_app.config['LDAP_BASE_DN'],
                        search_filter='(mail={email})'.format(email=email), attributes='dn')

    if users and len(conn.entries) >= 1:
        return conn.rebind(conn.entries[0].entry_dn, password)


def _ldap_server_connect():
    """
    Connect to an LDAP server
    :return: LDAP Connection
    """
    ldap_server = current_app.config['LDAP_SERVER']
    ldap_port = int(current_app.config['LDAP_PORT'])
    ldap_use_tls = current_app.config['LDAP_USE_TLS']
    ldap_key_path = current_app.config['LDAP_KEY_PATH']
    ldap_sa_bind_dn = current_app.config['LDAP_SA_BIND_DN']
    ldap_sa_password = current_app.config['LDAP_SA_PASSWORD']

    tls = Tls(validate=ssl.CERT_NONE, local_private_key_file=ldap_key_path)

    if ldap_use_tls:
        server = Server(ldap_server, ldap_port, tls=tls, use_ssl=True)
    else:
        server = Server(ldap_server, ldap_port)

    conn = Connection(server, ldap_sa_bind_dn, ldap_sa_password, auto_bind=True)

    return conn


def prepare_saml_request(request):
    """
    Prepare a Flask request to be processed by the OneLogin SAML Toolkit.

    Source: https://github.com/onelogin/python3-saml/blob/master/demo-flask/index.py#L22

    :param request: Flask HTTP Request
    :return: JSON Object for OneLogin
    """
    url_data = urlparse(request.url)
    return {
        'https': 'on' if request.scheme == 'https' else 'off',
        'http_host': request.host,
        'server_port': url_data.port,
        'script_name': request.path,
        'get_data': request.args.copy(),
        'post_data': request.form.copy()
    }


def init_saml_auth(onelogin_request):
    """
    Initialize a OneLoginSaml2 Auth Object from a Flask Request

    Source: https://github.com/onelogin/python3-saml/blob/master/demo-flask/index.py#L17

    :param onelogin_request: JSON Object with Request Details
    :return: OneLogin_Saml2_Auth object
    """
    onelogin_auth = OneLogin_Saml2_Auth(onelogin_request, custom_base_path=current_app.config['SAML_PATH'])
    return onelogin_auth


def get_self_url(onelogin_request):
    """

    :param onelogin_request:
    :return:
    """
    return OneLogin_Saml2_Utils.get_self_url(onelogin_request)