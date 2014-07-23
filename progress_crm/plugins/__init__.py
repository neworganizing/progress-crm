from admin_tools.dashboard import modules

class CRMDashboardRegister(type):
    REGISTRY = {}

    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)
        cls.REGISTRY[name] = new_cls
        return new_cls

class CRMDashboardModule(modules.DashboardModule):
    __metaclass__ = CRMDashboardRegister

    def __init__(self, **kwargs):
    	self.template = self.__module__.split(".")[0]+"/dashboard.html"
    	super(CRMDashboardModule, self).__init__(**kwargs)

    #template = "dashboard.html"