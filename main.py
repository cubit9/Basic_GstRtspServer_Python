import sys
import gi

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GLib

loop = GLib.MainLoop()
Gst.init(None)


class MyFactory(GstRtspServer.RTSPMediaFactory):
    def __init__(self):
        GstRtspServer.RTSPMediaFactory.__init__(self)

    def do_create_element(self, url):
        return Gst.parse_launch("( videotestsrc is-live=1 ! x264enc ! rtph264pay name=pay0 pt=96 )")


class GstServer:
    def __init__(self):
        self.server = GstRtspServer.RTSPServer()
        f = MyFactory()
        f.set_shared(True)
        self.server.get_mount_points().add_factory("/test", f)
        self.server.attach(None)


rtsp_server = GstServer()
loop.run()
