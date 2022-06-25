from nameko.web.handlers import http
from werkzeug.wrappers import Response
import uuid

from gateway.dependencies.session import SessionProvider

class Service:
    name = "gateway_service"

    session_provider = SessionProvider()
    
    @http('GET', '/login')
    def login(self, request):
        user_data = {
            'id': 1,
            'username': 'User'
        }
        
        session_id = self.session_provider.set_session(user_data)
        response = Response(str(user_data))
        response.set_cookie('SESSID', session_id)
        return response

    @http('GET', '/prime/<Input>')
    def prima(self, request, Input):
        print("Input : "+ str(Input))
        
        total = -1
        countPrime = 0
        count = 2

        Input = int(Input)
        
        while (total == -1):
            if (self.Check_prime(count)) :
                print(str(countPrime) + ":" + str(Input) + ":" + str(count))
                if (countPrime == Input) :
                    total = count
                countPrime = countPrime + 1
            count = count + 1
            
        response = Response("Prime : " + str(total))
        return response
    
    def Check_prime(self,j):
        for i in range(2,j):
            if (j%i) == 0:
                return False
        return True

    @http('GET', '/primepalindrome/<Input>')
    def PrimePalindrome(self, request, Input):
        print("Input : " + str(Input))
        
        total = -1
        countPrime = 0
        count = 2
        
        Input = int(Input)
        
        while (total == -1):
            if (self.Prime(count)) :
                if (countPrime == Input) :
                    total = count
                countPrime = countPrime+1
            count = count+1
            
        response = Response("Prime Palindrome is : " + str(total))
        return response
    
    def Check_PrimePalindrome(self, Input):
        turn = int(str(Input)[::-1])
        
        if Input == turn:
            if Input > 1:
                for i in range(2,Input):
                    if Input % i == 0:
                        return False
        else:
            return True
        
    def Prime(self,Input):
        Prime = True
        for i in range(2,Input):
            if (Input % i) == 0:
                 Prime = False
                 #return False
        
        if(str(Input) != str(Input)[::-1]):
            Prime = False
        
        return Prime