# -*- coding: UTF-8 -*-

class PackagesGenerator:
    def FileNotFound(Msg='File Not Found.'):
        Package = {
            'Code' : '404',
            'Message' : Msg
             }
        return Package

    def Forbidden(Msg='Forbidden!'):
        Package = {
            'Code' : '403',
            'Message' : Msg
            }
        return Package
    
    def InternalServerError(Msg='Sorry, this request is invaild!!'):
        Package = {
            'Code' : '500',
            'Title' : 'Internal Server Error',
            'Message' : Msg
            }
        return Package

    def LoginRequired():
        Package = {
            'Code' : '10',
            'Message' : 'LoginRequired'
            }
        return Package

    def Message(Title, Msg):
        Package = {
            'Code' : '200',
            'Title' : Title,
            'Message' : Msg
                }
        return Package

    def Custom(Msg):
        pass
