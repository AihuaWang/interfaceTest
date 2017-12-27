# -*- coding:utf-8 -*-  
import requests, xlrd, MySQLdb, time, sys ,logging ,json,ast
#导入需要用到的模块  
from xlutils import copy  
#从xlutils模块中导入copy这个函数 
from pylsy import pylsytable
##from __future__ import unicode_literals
######################################################
#定义系统输出码
reload(sys)
sys.setdefaultencoding('utf-8')

#######################################################
#定义日志输入
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',datefmt='%a, %d %b %Y %H:%M:%S',filename='mylog.log',filemode='w')

#######################################################
#定义一个StreamHandler,将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

##########################################################
#处理Excel表格

def readExcel(file_path):  
    ''''' 
    读取excel测试用例的函数 
    :param file_path:传入一个excel文件，或者文件的绝对路径 
    :return:返回这个excel第一个sheet页中的所有测试用例的list 
    '''  
    try:  
        book = xlrd.open_workbook(file_path)#打开excel  
        logging.info("打开%s excel表格成功"%file_path)
    except Exception,e:   
        logging.error("路径不在或者excel不正确%s"%e)
    else:  
        sheet = book.sheet_by_index(0)#取第一个sheet页 
        logging.info("打开%s表成功"%sheet) 
        rows= sheet.nrows#取这个sheet页的所有行数 
        numCases=rows-1
        logging.info("表中有%s条测试用例："%numCases) 
        case_list = []#保存每一条case 
        logging.info("开始添加测试用例") 
        for i in range(rows):  
            if i !=0:  
                #把每一条测试用例添加到case_list中  
                case_list.append(sheet.row_values(i))  
        #调用接口测试的函数，把存所有case的list和excel的路径传进去，因为后面还需要把返回报文和测试结果写到excel中，  
        #所以需要传入excel测试用例的路径，interfaceTest函数在下面有定义 
        logging.info("开始执行测试用例") 
        interfaceTest(case_list,file_path)  
  
def interfaceTest(case_list,file_path):  
    res_flags = []  
    #存测试结果的list  
    request_urls = []  
    #存请求报文的list  
    responses = []  
    #存返回报文的list 
    i=0 #标识测试case第几条
    for case in case_list:  
        ''''' 
        先遍历excel中每一条case的值，然后根据对应的索引取到case中每个字段的值 
        '''  
        i=i+1
        logging.info("开始执行第%s条测试用例"%i)
        try:  
            ''''' 
            这里捕捉一下异常，如果excel格式不正确的话，就返回异常 
            '''  
            #项目，提bug的时候可以根据项目来提  
            product = case[0]  
            #用例id，提bug的时候用  
            case_id = case[1]  
            #接口名称，也是提bug的时候用  
            interface_name = case[2]  
            #用例描述  
            case_detail = case[3]  
            #请求方式  
            method = case[4]  
            #请求url  
            url = case[5]  
            #入参  
            param = case[6]  
            #预期结果  
            res_check = case[7]  
            #测试人员  
            tester = case[10]
            logging.info("项目:%s"%product)  
            logging.info("测试用例id:%s"%case_id)
            logging.info("接口名称:%s"%interface_name)
            logging.info("用例描述:%s"%case_detail)
        except Exception,e:  
            logging.error("测试用例格式不正确！%s"%e)
            #return e 
        
        if method.upper() == 'GET':  
            ###GET方法时是否参数问题
            if param== '':  
                ''''' 
                如果请求参数是空的话，请求报文就是url，然后把请求报文存到请求报文list中 
                '''
                new_url = url #请求报文  
                logging.info("请求报文%s"%url)
                request_urls.append(new_url)  
            else: 
                ''''' 
                如果请求参数不为空的话，请求报文就是url+?+参数，格式和下面一样 
                http://127.0.0.1:8080/rest/login?oper_no=marry&id=100，然后把请求报文存到请求报文list中 
                '''  
                new_url = url+'?'+urlParam(param)#请求报文 
                logging.info("请求路径及参数%s"%new_url) 
                ''''' 
                excel里面的如果有多个入参的话，参数是用;隔开，a=1;b=2这样的，请求的时候多个参数要用&连接， 
                要把;替换成&，所以调用了urlParam这个函数，把参数中的;替换成&，函数在下面定义的 
                ''' 
                request_urls.append(new_url)  

            ########################

            ''''' 
            如果是get请求就调用requests模块的get方法，.text是获取返回报文，保存返回报文， 
            把返回报文存到返回报文的list中 
            '''  
            #print new_url 
            logging.info("请求方法GET") 
            results = requests.get(new_url).text  
            #print results 
            logging.info("返回报文%s"%results)
            logging.info("预期报文%s"%res_check) 

            responses.append(results)  
            ''''' 
            获取到返回报文之后需要根据预期结果去判断测试是否通过，调用查看结果方法 
            把返回报文和预期结果传进去，判断是否通过，readRes方法在下面定义了。 
            '''  
            res = readRes(results,res_check) 
            logging.info("测试结果:%s"%res) 
        else:  
            ''''' 
            如果不是get请求，也就是post请求，就调用requests模块的post方法，.text是获取返回报文， 
            保存返回报文，把返回报文存到返回报文的list中 
            ''' 
            new_url = url
            logging.info("请求路径%s"%url)
            request_urls.append(new_url) 
            logging.info("请求方法POST") 
            headers={'Content-Type':'application/json'}
            logging.info("请求报文%s"%param) 
            #print "param:%s"%param
            #print type(param)
            d=param.encode('utf-8')
            #d=json.dumps(param)
            #print "d:%s"%d
            #print type(d)
            r=requests.post(url,headers=headers,data=d)
            results=r.text
            logging.info("返回报文%s"%results) 
            logging.info("预期报文%s"%res_check)
            responses.append(results)  
            ''''' 
            获取到返回报文之后需要根据预期结果去判断测试是否通过，调用查看结果方法 
            把返回报文和预期结果传进去，判断是否通过，readRes方法会返回测试结果，如果返回pass就 
            说明测试通过了，readRes方法在下面定义了。 
            '''  
            dictresult=json.loads(results)
            dictres_check=json.loads(res_check)
            #print "type dictresult_check%s"%type(dictres_check)
            #print "res_check%s"%type(res_check)
            #print dictresult.get('state')
            #print dictres_check.get('state')
            resResultCode=readRes(dictresult.get('resultCode'),dictres_check.get('resultCode'))
            resState=readRes(dictresult.get('state'),dictres_check.get('state'))
            #res = readRes(results,res_check) 
             
            if(resResultCode and resState):
                res="pass" 
            else:
                res="fail"

            logging.info("测试结果:%s"%res)

            #print res 
        if 'pass' == res:  
            ''''' 
            判断测试结果，然后把通过或者失败插入到测试结果的list中 
            '''  
            res_flags.append('pass')  
        else:  
            res_flags.append('fail')  
    ''''' 
    全部用例执行完之后，会调用copy_excel方法，把测试结果写到excel中， 
    每一条用例的请求报文、返回报文、测试结果，这三个每个我在上面都定义了一个list 
    来存每一条用例执行的结果，把源excel用例的路径和三个list传进去调用即可，copy_excel方 
    法在下面定义了，也加了注释 
    ''' 
    copy_excel(file_path,res_flags,request_urls,responses) 
  
def readRes(res,res_check):  
     
    res1=json.dumps(res,sort_keys=True) 
    
    res_check1=json.dumps(res_check,sort_keys=True)
    
    result=res1==res_check1
    return result
    #print result
    #if result:
    #   return 'pass'
    #else:
    #   return 'fail'
    
 

def urlParam(param):  
    ''''' 
    参数转换，把参数转换为'xx=11&xx=2这样' 
    '''  
    return param.replace(';','&')  
  
def copy_excel(file_path,res_flags,request_urls,responses):  
    ''''' 
    :param file_path: 测试用例的路径 
    :param res_flags: 测试结果的list 
    :param request_urls: 请求报文的list 
    :param responses: 返回报文的list 
    :return: 
    '''  
    ''''' 
    这个函数的作用是写excel，把请求报文、返回报文和测试结果写到测试用例的excel中 
    因为xlrd模块只能读excel，不能写，所以用xlutils这个模块，但是python中没有一个模块能 
    直接操作已经写好的excel，所以只能用xlutils模块中的copy方法，copy一个新的excel，才能操作 
    '''  
    logging.info("测试结果写入") 
    #打开原来的excel，获取到这个book对象  
    book = xlrd.open_workbook(file_path)
    #logging.info("打开原来的excel%s"%book)  
    #复制一个new_book  
    new_book = copy.copy(book) 
    #logging.info("复制新的excel%s"%new_book) 
    #然后获取到这个复制的excel的第一个sheet页  
    sheet = new_book.get_sheet(0) 
    #logging.info("复制新的sheet%s"%sheet) 
    i=1  

    for request_url,response,flag in zip(request_urls,responses,res_flags): 
        ''''' 
        同时遍历请求报文、返回报文和测试结果这3个大的list 
        然后把每一条case执行结果写到excel中，zip函数可以将多个list放在一起遍历 
        因为第一行是表头，所以从第二行开始写，也就是索引位1的位置，i代表行 
        所以i赋值为1，然后每写一条，然后i+1， i+=1同等于i=i+1 
        请求报文、返回报文、测试结果分别在excel的8、9、11列，列是固定的，所以就给写死了 
        后面跟上要写的值，因为excel用的是Unicode字符编码，所以前面带个u表示用Unicode编码 
        否则会有乱码 
        '''   
        sheet.write(i,8,u'%s'%request_url)  
        sheet.write(i,9,u'%s'%response)  
        sheet.write(i,11,u'%s'%flag)  
        i+=1  
        #print i
    #写完之后在当前目录下(可以自己指定一个目录)保存一个以当前时间命名的测试结果，time.strftime()是格式化日期  
    new_book.save('%s_测试结果.xls'%time.strftime('%Y%m%d%H%M%S')) 


if __name__ == '__main__':  
    ''''' 
    然后进行调用，调用的时候需要传入一个excel，调用方式是 python test.py test_case.xls 
    sys.argv[1]的意思是取传入的第二个参数，也就是索引是1的， 
    第一个是这个python文件的文件名，如果不传入参数运行的话，会提示错误，如果正确的话， 
    会调用读excel的程序，执行用例，运行完成后，会打印Done 
    '''  
    try:  
        filename = sys.argv[1]  
    except IndexError,e:  
        print 'Please enter a correct testcase! \n e.x: python gkk.py test_case.xls'  
    else:  
        readExcel(filename)  
    print 'Done!'  