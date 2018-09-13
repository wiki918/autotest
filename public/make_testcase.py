#-*-coding:utf-8-*-
import os,re
from public.request import *

class Make_testcase:
    def __init__(self,testcasedir,case_data):
        self.testcasedir=testcasedir
        self.case_data=case_data
        self.__getAttributes()
        #self.case_name=case_data['case_name']
        self.filename=self.testcasedir+r"/"+self.case_name+".py"
        self.__create_testcase()
    #生成用例
    def __create_testcase(self):
        try:
            with open(self.filename,'w',encoding='utf-8') as self.testcase:
                message=self.__write()
                self.testcase.write(message)
                self.testcase.close()
        except Exception as e:
            raise e
    #编写用例内容
    def __write(self):
        try:
            templatedir=os.path.abspath(os.path.join(self.testcasedir, "../../template"))
            with open(templatedir, 'r',encoding='utf-8') as self.template:
                templatemessage=self.template.read()
                #regex=r"\${.*?}"
                #替换case_name
                regex = r"\${case_name}"
                message=self.__replaceVariable(regex,self.case_name,templatemessage)
                #替换api
                regex = r"\${api}"
                message = self.__replaceVariable(regex, self.api, message)
                #生成步骤和步骤名
                message=self.__replaceStep(message)
                #print (message)
                self.template.close()
                return message
        except Exception as e:
            raise e

    #替换变量
    def __replaceVariable(self,regex,variable,message,count=0):
        try:
            message = re.sub(regex, variable, message,count)
        except:
            raise ("替换变量出错")
            message=None
        return message

    #根据step_list_data的长度创建几个step
    def __replaceStep(self,message):
        # 根据step_list_data的长度创建几个step
        for i in range(self.steplen):
            stepmessage = '''    def test_${step_name}(self):
        step_name="${step_name}"
        makesqldata=None
        newVariableObj={}
        sqlDatalist=${sqlDatalist}
        api_dependency=${api_dependency}
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
        params=${params}
        headers=${headers}
        
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
        responseJson=${method}(url=self.url,params=params,headers=headers)
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
        assert_response=${assert_response}
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
            
        way="${way}"
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
'''
            message += stepmessage
        #替换变量
        regexlist = [r"\${step_name}",r"\${step_name}",r"\${params}",r"\${headers}",r"\${method}",r"\${way}",r"\${assert_response}",r"\${sqlDatalist}",r"\${api_dependency}"]
        for i in range(self.steplen):
            j=0
            # 替换步骤名,替换params和headers
            step_name=self.case_data['step_list_data'][i]['step_name']
            message = self.__replaceVariable(regexlist[j], step_name, message,1)
            # 替换步骤名,替换变量
            j += 1
            message = self.__replaceVariable(regexlist[j], step_name, message, 1)

            #替换params
            j += 1
            params = self.case_data['step_list_data'][i]['params']
            message = self.__replaceVariable(regexlist[j], params, message, 1)
            # 替换headers
            j += 1
            headers = self.case_data['step_list_data'][i]['headers']
            message = self.__replaceVariable(regexlist[j], headers, message, 1)
            # 替换method
            j += 1
            method = self.case_data['step_list_data'][i]['method']
            message = self.__replaceVariable(regexlist[j], method, message, 1)
            # 替换way
            j += 1
            way = method
            message = self.__replaceVariable(regexlist[j], way, message, 1)
            # 替换断言
            j += 1
            if self.case_data['step_list_data'][i]['assert_response']=="":
                message = self.__replaceVariable(regexlist[j], "{}", message, 1)
            else:
                message = self.__replaceVariable(regexlist[j], self.case_data['step_list_data'][i]['assert_response'], message, 1)
            # 替换sql
            j += 1
            if len(self.case_data['step_list_data'][i]['sql_list_data']) == 0:
                message = self.__replaceVariable(regexlist[j], "[]", message, 1)
            else:
                sqlDatalist=[]
                for sqlData in self.case_data['step_list_data'][i]['sql_list_data']:
                    sqlDatalist.append(sqlData)
                message = self.__replaceVariable(regexlist[j],str(sqlDatalist), message, 1)
            # 替换接口依赖
            j += 1
            if self.case_data['step_list_data'][i]['api_dependency'] == "":
                message = self.__replaceVariable(regexlist[j], "{}", message, 1)
            else:
                message = self.__replaceVariable(regexlist[j],
                                                    self.case_data['step_list_data'][i]['api_dependency'], message, 1)
        #print (message)
        return message
    #得到属性
    def __getAttributes(self):
        self.case_name = self.case_data['case_name']
        self.api = self.case_data['api']
        self.steplen=len(self.case_data['step_list_data'])
        #得到每个脚本的sql数
        self.stepSqllen=[]
        for i in range(self.steplen):
            self.stepSqllen.append(len(self.case_data['step_list_data'][i]['sql_list_data']))
        #self.step_name=self.case_data['step_list_data']['step_name']