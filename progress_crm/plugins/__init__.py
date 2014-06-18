from admin_tools.dashboard import modules

class CRMDashboardRegister(type):
    REGISTRY = {}

    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)
        cls.REGISTRY[name] = new_cls
        return new_cls

class CRMDashboardModule(modules.DashboardModule):
    __metaclass__ = CRMDashboardRegister