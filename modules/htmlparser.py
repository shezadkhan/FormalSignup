import datetime
import copy

class MyHTMLParser():
    def GetTime(self,st):
        x =st[210:]
        y=x[:20]
        h,m,s = y.strip().split(':')
        print h,m,s
        nw = datetime.datetime.now()
        nw_server=nw.replace(hour=int(h),minute=int(m),second=int(s))
        return nw_server,nw
