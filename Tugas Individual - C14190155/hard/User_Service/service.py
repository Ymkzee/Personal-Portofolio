import gateway.dependencies.dependencies as dependencies

from nameko.rpc import rpc

class UserAccessService:

    name = 'Service'

    Db = dependencies.Database()

    @rpc
    def add_user(self, nrp, Acc, email, Password):
        user = self.Db.add_user(nrp, Acc, email, Password)
        return user

    @rpc
    def get_user(self, email, Password):
        user = self.Db.get_user(email, Password)
        return user
    
    @rpc
    def add_file(self, Acc, file):
        self.Db.add_file(Acc, file)