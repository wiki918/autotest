#!/usr/bin/python
#-*- encoding:UTF-8 -*-

from public.request import *
from public.sqldb import *
from public.log import *
from public.run import *
from public.sqldb import Transferip_db
from public.mongodb import Transferip_mongodb
import unittest,re,json
class signin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.transferlogname=Transferlogname()
        cls.transferip_db=Transferip_db()
        cls.transfermongodb = Transferip_mongodb()
        api="/zhuanle/sign-in"
        cls.url=cls.transferip_db.ip+api
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def getAssertWay(self,assertway):
        if assertway=="assertEqual":
            Assertwaymessage="等于"
        elif assertway=="assertNotEqual":
            Assertwaymessage="不等于"
        elif assertway=="assertRegexpMatches":
            Assertwaymessage="包含"
        elif assertway=="assertNotRegexpMatches":
            Assertwaymessage="不包含"
        elif assertway=="assertGreater":
            Assertwaymessage="大于"
        elif assertway=="assertGreaterEqual":
            Assertwaymessage="大于等于"
        elif assertway=="assertLess":
            Assertwaymessage="小于"
        elif assertway=="assertLessEqual":
            Assertwaymessage="小于等于"
        elif assertway=="assertIn":
            Assertwaymessage="在列表中"
        elif assertway=="assertNotIn":
            Assertwaymessage="不在列表中"
        return Assertwaymessage

    def test_signinstep(self):
        step_name="signinstep"
        makesqldata=None
        newVariableObj={}
        sqlDatalist=[]
        api_dependency={}
        #查找接口依赖数据
        search_mongo_result=self.transfermongodb.mongodb.search_one(self.transferlogname.test_carryid,api_dependency)
        
        for sqlDatalistCount in range(len(sqlDatalist)):
            sqlData=sqlDatalist[sqlDatalistCount]
            if sqlData['sql_condition']==0:
                if sqlData['is_select']!=True:
                    self.transferip_db.db.ExecNoQuery(sqlData['sql'])
                else:
                    makesqldata=MakeSqlData(sqlData['variable'],sqlData['sql'])
                    newVariableObj=dict(newVariableObj,**makesqldata.variableObj)
                if makesqldata:
                    sqlDatalist=json.dumps(sqlDatalist,ensure_ascii = False)
                    for i in makesqldata.variableObj.keys():
                        regex=r"\${"+i+r"}"
                        sqlDatalist = re.sub(regex, str(makesqldata.variableObj[i]), sqlDatalist)
                    sqlDatalist=json.loads(sqlDatalist)
                else:
                    #makesqldata not exist,not sql
                    pass 
        params={"account":"18300005500","password":"ww123456"}
        headers={"X-KJT-Agent":"00000000-0000-0000-0000-000000000000;IMSI;Android7.0;hero2qltechn;UNKNOWN;SM-G9350;android_normal;3.0.0;WIFI;-","X-DEV-Label":"android_eyJvcyI6ImFuZHJvaWQiLCJ2ZXJzaW9uIjoiMy4wLjkiLCJwYWNrYWdlcyI6ImNvbS5oYWllci5oYWlyeV8yLjIuNCIsInByb2ZpbGVfdGltZSI6MjczLCJpbnRlcnZhbF90aW1lIjoyMDkxODMsInRva2VuX2lkIjoid0lCYk1DWk9iMW5reVRUdmlkRVpmU3FLNXdDelUweVwveUFoRFhyQ0JteEFcL0VnNFEwQXpSSmt4TlMzTEpUQldsTUhOMytMZnVjRU1aUVBxME8zbVJodz09In0","Content-Type":"application/json"}
        
        #追加替换变量字典
        newVariableObj.update(search_mongo_result)
        
        #replace variable
        if makesqldata or api_dependency!={}:
            params=json.dumps(params,ensure_ascii = False)
            headers=json.dumps(headers,ensure_ascii = False)
            for i in newVariableObj.keys():
                regex=r"\${"+i+r"}"
                params = re.sub(regex, str(newVariableObj[i]), params)
                headers = re.sub(regex, str(newVariableObj[i]), headers)
            params=json.loads(params)
            headers=json.loads(headers)
        else:
            #makesqldata not exist,not sql
            pass 
        responseJson=postbody(url=self.url,params=params,headers=headers)
        #插入mongodb数据
        document={}
        document['test_carryid'] = self.transferlogname.test_carryid
        document['step_name']=step_name
        document['responseJson'] = responseJson
        self.transfermongodb.mongodb.insert_one(document)
        
        #__init__
        makesqldata=None
        newVariableObj={}
        for sqlDatalistCount in range(len(sqlDatalist)):
            sqlData=sqlDatalist[sqlDatalistCount]
            if sqlData['sql_condition']==1:
                if sqlData['is_select']!=True:
                    self.transferip_db.db.ExecNoQuery(sqlData['sql'])
                else:
                    makesqldata=MakeSqlData(sqlData['variable'],sqlData['sql'])
                    newVariableObj=dict(newVariableObj,**makesqldata.variableObj)
                if makesqldata:
                    sqlDatalist=json.dumps(sqlDatalist,ensure_ascii = False)
                    for i in makesqldata.variableObj.keys():
                        regex=r"\${"+i+r"}"
                        sqlDatalist = re.sub(regex, str(makesqldata.variableObj[i]), sqlDatalist)
                    sqlDatalist=json.loads(sqlDatalist)
                else:
                    #makesqldata not exist,not sql
                    pass 
        assert_response={"['status']":{"assertEqual":"0"}}
        #replace assert_response
        if makesqldata:
            assert_response=json.dumps(assert_response,ensure_ascii = False)
            for i in newVariableObj.keys():
                regex=r"\${"+i+r"}"
                assert_response = re.sub(regex, str(newVariableObj[i]), assert_response)
            assert_response=json.loads(assert_response)
        else:
            #makesqldata not exist,not sql
            pass 
            
        way="postbody"
        for i in assert_response.keys():
            responseJsonAssert=responseJson
            #断言key遍历
            regexkey = r"\[(.+?)\]"
            resultlist = re.findall(regexkey, i)
            regexkey1 = r"'"
            for j in resultlist:
                if len(re.findall(regexkey1, j)) == 0:
                    j = int(j)
                else:
                    j = re.sub(regexkey1, "", j)
                responseJsonAssert = responseJsonAssert[j]
            #断言
            try:
                for k in assert_response[i].keys():
                    self.chooseAssertWay(str(responseJsonAssert),k,assert_response[i][k])
            except:
                @Log(self.transferlogname.Errorlogname, level="ERROR")
                def writeLog(step_name,url, way, header, params,message,assertResult):
                    print("write Errorlogname")
                Assertwaymessage=self.getAssertWay(k)
                #writeLog(step_name,self.url,way,headers,params,responseJson['message'],str(responseJsonAssert)+Assertwaymessage+assert_response[i][k])
                writeLog(step_name,self.url,way,headers,params,"接口测试断言错误",str(responseJsonAssert)+Assertwaymessage+assert_response[i][k])
                self.chooseAssertWay(str(responseJsonAssert), k, assert_response[i][k])
        pass
        @Log(self.transferlogname.Successlogname, level="INFO")
        def writeLog(step_name,url, way, header, params,message):
            print("write Successlogname")
        writeLog(step_name,self.url,way,headers,params,"接口测试通过")
