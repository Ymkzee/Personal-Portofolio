import json
from nameko.web.handlers import http
from werkzeug.wrappers import Response

import requests
import uuid

from nameko.rpc import RpcProxy

from gateway.dependencies.session import SessionProvider
from gateway.dependencies.dependencies import Database,DatabaseWrapper

class Service:
    name = "gateway_Service"
    
    User_Service = RpcProxy('Service')

    session_provider = SessionProvider()
    
    #register
    @http('POST', '/register')
    def register(self, request):
        Register = request.json
        response = self.User_Service.add_user(Register['nrp'],Register['name'],Register['email'],Register['password'])
        
        return response
    
    #login
    @http('POST', '/login')
    def login(self, request):
        Login = request.json
        temp = self.User_Service.get_user(Login['email'],Login['password'])
        
        if temp and len(temp)>0 :
            temp = temp[0]
            session_id = self.session_provider.set_session(temp)
            temp['session_id'] = session_id
            response = Response(str(temp))
            response.set_cookie('SESSID', session_id)
            return response
        else :
            response = Response("Login Failed!")
            return response
        
    @http('POST', '/logout')
    def logout(self, request):
        cookies = request.cookies
        
        if cookies:
            session_data = self.session_provider.delete_session(cookies['SESSID'])
            
            response = Response('Logout Success!')
            return response
        else:
            response = Response('Logout Failed!')
            return response
    
    @http("POST", "/upload")
    def save_file(self, request):
        cookies = request.cookies
        session_data = None
        if cookies:
            print("checkuser : "+cookies["SESSID"])
            session_data = self.session_provider.get_session(str(cookies['SESSID']))  
            
        if (session_data!=None):
            for file in request.files.items():
                _, file_storage = file
                file_str = uuid.uuid4().hex  
                new_file_name = file_str + file_storage.filename
                file_name = "upload/" + new_file_name
                self.User_Service.add_file(session_data['id'],file_name)
                
                file_storage.save(f"{file_name}")
            return json.dumps({"ok": True})
        else :
            return "Failed to Save File !!"
    
    # belum memenuhi kriteria 

    @http('GET', "/download")
    def files(self,request):  # pragma: no cover
        Link = "http://google.com/favicon.ico"
        r = requests.get(Link, allow_redirects=True)
        #print(r.status)
        open("google.ico", "wb").write(r.content)
        return r
        #u"received: {}".format(request.get_data(as_text=True))
        
    @http('GET', "/search")
    def search(self,request):  # pragma: no cover
        cookies = request.cookies
        session_data = None
        
        if cookies:
            print("checkuser "+cookies["SESSID"])
            session_data = self.session_provider.get_session(str(cookies['SESSID']))  
        
    
    
        
    
    