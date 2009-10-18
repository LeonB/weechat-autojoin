import weechat as w

SCRIPT_NAME    = "sessions"
SCRIPT_AUTHOR  = "Leon Bogaert <leon@tim-online.nl>"
SCRIPT_VERSION = "0.1"
SCRIPT_LICENSE = "GPL2"
SCRIPT_DESC    = "Firefox-like sessions: configure autojoin for all channels \n\
                  It does not set autoconnection for servers!"
SCRIPT_COMMAND = "write_autojoin_channels"

def write_autojoin_channels(data, buffer, args):
    """Stolen from autojoin.py (written by xt)"""
    items = {}
    infolist = w.infolist_get('irc_server', '', '')
    # populate servers
    while w.infolist_next(infolist):
        items[w.infolist_string(infolist, 'name')] = ''

    w.infolist_free(infolist)

    # populate channels per server
    for server in items.keys():
        infolist = w.infolist_get('irc_channel', '',  server)
        while w.infolist_next(infolist):
            if w.infolist_integer(infolist, 'type') == 0:
                channel = w.infolist_string(infolist, "buffer_short_name")
                items[server] += '%s,' %channel
        w.infolist_free(infolist)

    # print/execute commands
    for server, channels in items.iteritems():
        channels = channels.rstrip(',')
        #if not channels: # empty channel list
            #continue
        command = "/set irc.server.%s.autojoin '%s'" % (server, channels)
        w.command('', command)

    return w.WEECHAT_RC_OK

w.register(
    SCRIPT_NAME, 
    SCRIPT_AUTHOR, 
    SCRIPT_VERSION, 
    SCRIPT_LICENSE, 
    SCRIPT_DESC, 
    "", #??
    "" #??
)

w.hook_signal('*,irc_in2_join',  'write_autojoin_channels', '')
w.hook_signal('*,irc_in2_part',  'write_autojoin_channels', '')
w.hook_signal('quit',  'write_autojoin_channels', '')

w.hook_command(SCRIPT_COMMAND,
               SCRIPT_DESC,
               "",
               "",
               "",
               "write_autojoin_channels",
               ""
              )
