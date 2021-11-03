# Load libraries
from ldap3 import Server, Connection, ALL, SAFE_SYNC, ObjectDef, Reader
from typing import Optional

class LdapAuthentication:

    def __init__(self, dominio: str, user: str, password: str, group: Optional[str] = None):
        global authenticate
        global authorized
        self.dominio: str = dominio
        self.user: str = user
        self.password: str = password
        self.group: str = group
        if dominio == '':
            self.server = ''
            self.baseDn = 'dc='',dc='',dc='''
        elif dominio == '':
            self.server = ''
            self.baseDn = 'dc='',dc='',dc='''
        elif dominio == '':
            self.server = ''
            self.baseDn = 'dc='',dc='',dc='''
        elif dominio == '': 
            self.server = ''
            self.baseDn = 'dc='',dc='',dc='''
        elif dominio == '': 
            self.server = ''
            self.baseDn = 'dc='',dc='',dc='''

    def ldap_simple_auth(self):
        authenticate = False
        s = Server(self.server, get_info=ALL)
        c = Connection(s, user=self.user, password=self.password)
        if not c.bind():
            print('error in bind', c.result)
            return authenticate
        #c.unbind()
        authenticate = True
        return authenticate

    def ldap_group_auth(self):
        authenticate = False
        authorized = None
        s = Server(self.server, get_info=ALL)
        c = Connection(s, user=self.user, password=self.password)
        
        if not c.bind():
            print('error in bind', c.result)
            return authenticate, authorized 

        emailsList=[]
        c.search(self.baseDn, '(&(objectclass=group)(cn={}))'.format(self.group), attributes=['member'])

        try:
            for entry in c.entries:
                for member in entry.member.values:
                    c.search(
                        search_base=self.baseDn,
                        search_filter=f'(distinguishedName={member})',
                        attributes=[
                            'userPrincipalName'
                        ]
                    )
                    userEmails = c.entries[0].userPrincipalName.values
                    #print(userEmails)
                    emailsList.extend(userEmails)
        except:
            return authenticate, authorized
  
        authenticate = True

        if (self.user.lower() in (string.lower() for string in emailsList)) == True:
            authorized = True
        else:
            authorized = False

        return authenticate, authorized

