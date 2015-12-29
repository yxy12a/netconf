from ncclient import manager
import h3ctemplates as template

SSH_PORT = 830

def h3c_unknown_host_cb(host, fingerprint):
    """An unknown host callback.

    Returns `True` if it finds the key acceptable,
    and `False` if not. This default callback for NOS always returns 'True'
    (i.e. trusts all hosts for now).
    """
    return True

class H3Cdriver(object):
    """H3C 6800 switch
    """
    def __init__(self):
        self.mgr = None

    def connect(self, host, username, password):
        """Connect via SSH and initialize the NETCONF session."""
        # Use the persisted NETCONF connection
        if self.mgr and self.mgr.connected:
            return self.mgr

        # Open new NETCONF connection
        try:
            self.mgr = manager.connect(host=host, port=SSH_PORT,
                                       username=username, password=password,
                                       unknown_host_cb=h3c_unknown_host_cb, device_params={'name': "h3c"})
        except Exception as e:
            print("failed to connect to H3C switch")
            print e
            return None

        print("Connect success to host %(host)s:%(ssh_port)d",
                  dict(host=host, ssh_port=SSH_PORT))
        return self.mgr

    def close_session(self):
        """Close NETCONF session."""
        if self.mgr:
            self.mgr.close_session()
            self.mgr = None

    def create_acl(self, mgr, acl_number):
        """Configures a VLAN interface."""

        confstr = template.CREATE_ACL.format(acl_num=acl_number)
        print confstr
        print mgr.edit_config(target='running', config=confstr)
    
    def modify_syslog(self, mgr):
	confstr = template.SYSLOG_BUFFERSIZE.format(buffer_size=120)
        print mgr.edit_config(target='running', config=confstr)

def testnetconf(host, username, password):
    h3c_switch = H3Cdriver()
    mgr = h3c_switch.connect(host, username, password) 
    if mgr:
    	h3c_switch.create_acl(mgr, "2003") 
    	h3c_switch.close_session()

if __name__ == '__main__':
    host = "172.11.0.246"
    usr_name = "tcl"
    pwd = "tcl"
    testnetconf(host, usr_name, pwd)
    #with manager.connect(host="172.11.0.246", port=830, username="tcl", password="tcl", hostkey_verify=False, device_params={'name': "h3c"}) as m:
    #	j=m.get_config('running')
    #    print j
