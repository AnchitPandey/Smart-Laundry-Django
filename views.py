# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse , HttpResponseRedirect
from .models import student,data,Admin
from time import gmtime, strftime
import socket,json,pickle
from django.views.decorators.csrf import csrf_protect
import pandas as pd 
import os
import smtplib
import csv
from django.utils.encoding import smart_str
# Create your views here.

#username =''
#password =''
#stud1 =''
#dat1 = ''
session = 0
#length =''
session_admin = 0
machine_selected = {}
machine_boys_not_functional =[]
machine_girls_not_functional =[]


def one_time_only(request):
  stud = student.objects.all()
  for x in stud:
    x.inactive_status = 'active'
    x.save()
  return HttpResponse('<h3> DONE !!</h3>')



def data_entry(request):
  '''
  print(os.getcwd())
  
  print ("data_entry() called..")
  #print(os.getcwd())
  dataframe_staff  = pd.read_excel(str('laundry/final_password_list_done1.xlsx'))
  
  studentss = student.objects.all()
  email =''
  for stud in studentss:
    print ("student bits id is  "+str(stud.bits_id))
    for index, rows in dataframe_staff.iterrows():
      print ('student row ID is :'+str(rows['ID']))
      if (str(rows['ID']) ==str(stud.bits_id)):
        email = rows['Email']
        print ("MATCH FOUND !!!!!!!")
        break
    print (email)
    stud.email_id = email
    stud.save()
  '''
  ''' 
  for index, rows in dataframe_staff.iterrows():
    name = rows['Name']
    password = rows['Password']
    bits_id  = rows['ID']
    gender = rows['Gen']
    stud  =student(name = name, password =password, bits_id  =bits_id , gender = gender)
    stud.save()
  
  #print (dataframe_staff)
  '''
  return HttpResponse("<h4>done</h4>")

def index(request):
        print ("index() started....")
        return render(request,'laundry/index.html')

@csrf_protect
def validation(request):
        global machine_boys_not_functional
        #print (machine_boys_not_functional)
        #print (type(machine_boys_not_functional))
        print ("validation() started....")
        #global username, password, stud1,dat1,session,length
        stud = student.objects.all()
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
        else:
                ip = request.META.get('REMOTE_ADDR')
        
        ip+="$$"
        print(ip)
        if (ip not in request.session):
                print ("1: I am in ")
                username = request.POST.get('Username')
                password = request.POST.get('Password')
                print(username + ' ' + password)
                for x in stud :
                        if (x.bits_id == username  and x.password == password and x.inactive_status =="active"):
                                username = x.name
                                password = x.password 
                                length = len(data.objects.filter(idd=x.bits_id))
                                print ("useranme is: "+str(username))
                                print ("ID is: "+str(x.bits_id))
                                print ("the length is :")
                                print (length)
                        #request.session[str(stud1.bits_id)] = 1
                                if (length !=0):
                                        dat1 = data.objects.filter(idd=x.bits_id)[length-1]  #Arrange this in decreasing order...getting latest object
                                #dat1 = json.loads(str(dat1))
                                else:
                                        dat1 = data(idd = x.bits_id, count=0)
                                        dat1.save()
                                        #dat1= -1

                                #return render(request,'laundry/validation.html',{'values':username})
                        #session=1
                                dat1 = pickle.dumps(dat1)
                                request.session[str(ip)] = dat1
                                return render(request,'laundry/validation.html',{'data':pickle.loads(dat1),'userinfo':x,'machine_selected':machine_selected})

                        #return HttpResponseRedirect("/laundry/welcome")
                                
                
        
                return HttpResponseRedirect("/laundry")

        else:
                print ("2a: I am in = " + str(ip))
                dat1 = pickle.loads(request.session[str(ip)])
                #print ("2b: I am in = " + str(ip) + " " + request.session[str(ip)])
		print ("2bb: " + dat1.idd)
                #print ("2c:dat1 = " + str(dat1) + " " + type(dat1))

                length = len(data.objects.filter(idd=dat1.idd))
                dat1 = data.objects.filter(idd=dat1.idd)[length-1]
                print ("3: I am in " + str(length))
                for x in stud:
                        if(x.bits_id ==dat1.idd):
                               print ("4: I am in ")
                               return render(request,'laundry/validation.html',{'data':dat1,'userinfo':x,'machine_selected':machine_selected})
                
                print ("5: I am in ")
                return HttpResponseRedirect("/laundry")
                
        
               
def welcome(request):
        print ("welcome() started....")
        global session
        if(session ==0):
           return HttpResponseRedirect("/laundry") 
        
        return render(request,'laundry/validation.html',{'data':dat1,'userinfo':stud1,'machine_selected':machine_selected})


# viewing available machines
def rpi1(request):
        print ("rpi1() started...")
        global pin_numbers
        global machine_boys_not_functional
        global machines_girls_not_functional
        #pin_numbers = [1,2,3]
        stud1={}
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
        else:
                ip = request.META.get('REMOTE_ADDR')
        ip+="$$"
        if( ip not in request.session):
                return HttpResponseRedirect("/laundry")
        print ("passed session.")
        stud = student.objects.all()
        dat1 = pickle.loads(request.session[str(ip)])
        for x in stud:
                if (x.bits_id == dat1.idd):
                        stud1 =x
                        break
        
        #length = len(data.objects.filter(idd=x.bits_id))
        #dat1 = data.objects.filter(idd=x.bits_id)[length-1]
        length = len(data.objects.filter(idd=dat1.idd))
        dat1 = data.objects.filter(idd=dat1.idd)[length-1]
        
                
        # code to check the ip will come here 
        if (stud1.gender=='M'):
          clientsocket = socket.socket()
          clientsocket.connect(('172.16.100.175',8080))  # this is rpi  address
          clientsocket1= socket.socket()
          clientsocket1.connect(('172.16.100.176',8080))
          clientsocket1.send(bytes('machine_status'))
          clientsocket.send(bytes("machine_status"))
          pin_numbers = clientsocket.recv(2048).decode('utf-8')
          pin_numbers1 = clientsocket1.recv(2048).decode('utf-8')
          pin_numbers = pin_numbers.split()       
          pin_numbers1 = pin_numbers1.split()
          pin_numbers = list(map(int,pin_numbers))
          pin_numbers1 = list(map(int,pin_numbers1))
          pin_numbers = pin_numbers + pin_numbers1
          if (len (machine_boys_not_functional)!=0):
            final_pin_numbers = [x for x in pin_numbers if x not in machine_boys_not_functional]
          else:
            final_pin_numbers = pin_numbers
          clientsocket.close()
        
          
        else:
          clientsocket = socket.socket()
          clientsocket.connect(('172.16.100.177',8080))
          clientsocket.send(bytes("machine_status"))
          pin_numbers = clientsocket.recv(2048).decode('utf-8')
          pin_numbers = pin_numbers.split()       
          pin_numbers = list(map(int,pin_numbers))
          if (len (machine_girls_not_functional)!=0):
            final_pin_numbers = [x for x in pin_numbers if x not in machine_girls_not_functional]
          else:
            final_pin_numbers = pin_numbers
          clientsocket.close()
        
        return render(request,'laundry/validation.html',{'pin_numbers':final_pin_numbers,'data':dat1,'userinfo':stud1,'machine_selected':machine_selected})

        
#logout button 
def session1(request):
        print ("session1() started....")
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
        else:
                ip = request.META.get('REMOTE_ADDR')
        ip+="$$"

        del request.session[str(ip)]
        #session = 0
        return HttpResponseRedirect("/laundry")


def handler(request):
        print ("handler() started....")
        global dat1,session
        #print (request.body)
        #params = json.loads(request.body)
        #report_array = params['report_array']
        pin = int(request.GET['pins'])
        print ("I got the pins "+ str(pin))
        #print (request.GET)
        stud1={}
        stud = student.objects.all()
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
        else:
                ip = request.META.get('REMOTE_ADDR')
        ip+="$$"

        #host =''            # This is RPI address which you have to find out using router table
        
        #received_json_data = str(request.body.decode("utf-8"))
        
        #number = received_json_data['machine_number']
        
        port = 5555
        #clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        
        if ip in request.session:
                dat = pickle.loads(request.session[str(ip)])
                for x in stud:
                        if (x.bits_id == dat.idd):
                                stud1 =x
                                #print (dat.idd)
                                break
                if (stud1.gender=='M'):
                  if (pin > 10):
                    print ("in boys drier")
                    clientsocket1 = socket.socket()
                    clientsocket1.connect(('172.16.100.176',8080))
                    clientsocket1.send(bytes(str(pin)))
                  else:
                    print ("in boys washer")
                    clientsocket = socket.socket()
                    clientsocket.connect(('172.16.100.175',8080))
                    clientsocket.send(bytes(str(pin)))
                    
                else:
                  print ("in girls laundromat")
                  clientsocket  = socket.socket()
                  clientsocket.connect(('172.16.100.177',8080))
                  clientsocket.send(bytes(str(pin)))
                    
                
                length = len(data.objects.filter(idd=stud1.bits_id))
                dat1 = data.objects.filter(idd=stud1.bits_id)[length-1]
                if (length==1 and dat1.count==0):
                        dat1 = data(idd = dat.idd,month= strftime('%B'),count =1 , time_stamp =strftime("%Y-%m-%d %H:%M:%S", gmtime()),cost =0)
                        print ("working !!")
                        dat1.save()
                else:
                 
                 timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                 month = strftime('%B')
                 count = dat1.count
                 cost = dat1.cost
                 count = dat1.count+1

                 stud1.current_count = stud1.current_count+1
                 stud1.save()
                 if (count > 40):
                        cost = float(dat1.cost) + 2.5
                 else:
                        cost = float(dat1.cost)
                 
                 newobj = data(idd=dat1.idd,month =month,count = count,time_stamp = timestamp,cost = cost)
                 newobj.save()
                 print("reached  here")
                return render(request,'laundry/validation.html',{'data':newobj,'userinfo':stud1,'machine_selected':machine_selected})
        else :
                return HttpResponseRedirect("/laundry")

def admin(request):
        print ("admin() started....")
        return render(request,'laundry/admin.html')

@csrf_protect        
def advalidation(request):
        print ("avalidation() started....")
        global machine_boys_not_functional
        global machines_girls_not_functional
        print (request)
        machine_boys_not_functional = request.GET.getlist('blocked_machines_a_block[]')
        machine_boys_not_functional = list(map(int, machine_boys_not_functional))
	if (len(machine_boys_not_functional)!=0):
                print ((machine_boys_not_functional))
        userr = request.POST.get('Username')
        passs = request.POST.get('Password')
        admins =Admin.objects.all()
        for y in admins:
                if(y.username  ==userr and y.password == passs):
                        return render(request,'laundry/adminpage.html')
               
        return HttpResponseRedirect("/laundry/admin")


def detaildisplay(request):
        
     bid   =  request.POST.get('det')
     print ('I received '+ bid)
     data2 =  data.objects.filter(idd=bid)
     stud1 =  student.objects.filter(bits_id=bid)[0]
     return render(request,'laundry/adminfinalview.html',{'datacoming':data2, 'userinfo': stud1})

#history 
def history (request):
        print ("history() started....")
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
        else:
                ip = request.META.get('REMOTE_ADDR')
        ip+="$$"
        if( ip not in request.session):
                return HttpResponseRedirect("/laundry")
        
        stud1 = pickle.loads(request.session[str(ip)])
        return render(request,'laundry/histogram.html',{'data':data.objects.filter(idd=stud1.idd),'userinfo':stud1})
                             
def add(request):
        name = request.POST.get('name')
        idd = request.POST.get('id')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        usertype = request.POST.get('usertype')
        max_count = request.POST.get('max_count')
        inactive_status = request.POST.get('inactive_status')
        student_list = student.objects.all()
        control_flag = 0
        for student1 in student_list:
                if (student1.bits_id  == idd):
                        control_flag =1
                        break
        if (control_flag==0):
                new_student = student(name=name,password =password, bits_id = idd, gender = gender,usertype=usertype, max_count=max_count, inactive_status =inactive_status)
                new_student.save()
        return render(request,'laundry/adminpage.html')
                

def remove(request):
        idd = request.POST.get('id')
        student_list = student.objects.all()
        #student.objects.filter(bits_id =idd).delete()
        stud1 = student.objects.filter(bits_id =idd)[0]
        stud1.inactive_status = "inactive"
        stud1.save()
        #data.objects.filter(idd=idd).delete()
        return render(request,'laundry/adminpage.html')

def generate(request):
        response = HttpResponse(content_type ='text/csv')
        response['Content-Disposition'] = 'attachment; filename ="accounting_file.csv"'
        writer = csv.writer(response, csv.excel)
        response.write(u'\ufeff'.encode('utf8'))
        writer.writerow([
		smart_str(u"Name"),
		smart_str(u"Bits-Id"),
		smart_str(u"Eligibility"),
		smart_str(u"Total"),
                smart_str(u"Extra Use"),
                smart_str(u"Amount to be charged (in AED)"),])
        	
        #dataframe =pd.DataFrame(columns = ['Name','BITS-ID','month','count','cost'])
        dataframe =pd.DataFrame(columns = ['Name','BITS-ID','Eligibility','Total','Extra Use','Amount to be Charged (in AED)'])
        student_list = student.objects.all()
        for student_data in student_list:
          if (student_data.inactive_status =="active" and student_data.usertype=="student"):
            temp_dataframe = pd.DataFrame([student_data.name, student_data.bits_id, student_data.max_count, student_data.current_count,student_data.max_count -40, (student_data.max_count -40)*2.5])
            writer.writerow([
              smart_str(student_data.name),
              smart_str(student_data.bits_id),
              smart_str(student_data.max_count),
              smart_str(student_data.current_count),
              smart_str(student_data.max_count - 40),
              smart_str((student_data.max_count - 40 )*2.5),
              ])
            dataframe  = dataframe.append(temp_dataframe)
        return response


def generate_for_staff(request):
        response = HttpResponse(content_type ='text/csv')
        response['Content-Disposition'] = 'attachment; filename ="accounting_file_for_staff.csv"'
        writer = csv.writer(response, csv.excel)
        response.write(u'\ufeff'.encode('utf8'))
        writer.writerow([
		smart_str(u"Name"),
		smart_str(u"Bits-Id"),
		smart_str(u"Eligibility"),
		smart_str(u"Total"),
                smart_str(u"Extra Use"),
                smart_str(u"Amount to be charged (in AED)"),])
        	
        #dataframe =pd.DataFrame(columns = ['Name','BITS-ID','month','count','cost'])
        dataframe =pd.DataFrame(columns = ['Name','BITS-ID','Eligibility','Total','Extra Use','Amount to be Charged (in AED)'])
        student_list = student.objects.all()
        for student_data in student_list:
          if (student_data.usertype=="staff"):
            temp_dataframe = pd.DataFrame([student_data.name, student_data.bits_id, student_data.max_count, student_data.current_count,student_data.max_count -40, (student_data.max_count -40)*2.5])
            writer.writerow([
              smart_str(student_data.name),
              smart_str(student_data.bits_id),
              smart_str(student_data.max_count),
              smart_str(student_data.current_count),
              smart_str(student_data.max_count - 72),
              smart_str((student_data.max_count - 72 )*2.5),
              ])
            dataframe  = dataframe.append(temp_dataframe)

          if (student_data.usertype =="visitor"):
            temp_dataframe = pd.DataFrame([student_data.name, student_data.bits_id, student_data.max_count, student_data.current_count,student_data.max_count -40, (student_data.max_count -40)*2.5])
            writer.writerow([
              smart_str(student_data.name),
              smart_str(student_data.bits_id),
              smart_str(student_data.max_count),
              smart_str(student_data.current_count),
              smart_str(student_data.max_count),
              smart_str((student_data.max_count)*2.5),
              ])            
            dataframe  = dataframe.append(temp_dataframe)

        dataframe.to_csv('accounting_file_for_staff.csv')    
        return response

def generate_for_inactive_students(request):
        response = HttpResponse(content_type ='text/csv')
        response['Content-Disposition'] = 'attachment; filename ="accounting_file_for_inactive_students.csv"'
        writer = csv.writer(response, csv.excel)
        response.write(u'\ufeff'.encode('utf8'))
        writer.writerow([
		smart_str(u"Name"),
		smart_str(u"Bits-Id"),
		smart_str(u"Eligibility"),
		smart_str(u"Total"),
                smart_str(u"Extra Use"),
                smart_str(u"Amount to be charged (in AED)"),])
        	
        #dataframe =pd.DataFrame(columns = ['Name','BITS-ID','month','count','cost'])
        dataframe =pd.DataFrame(columns = ['Name','BITS-ID','Eligibility','Total','Extra Use','Amount to be Charged (in AED)'])
        student_list = student.objects.all()
        for student_data in student_list:
          if (student_data.inactive_status =="inactive" and student_data.usertype=="student"):
            temp_dataframe = pd.DataFrame([student_data.name, student_data.bits_id, student_data.max_count, student_data.current_count,student_data.max_count -40, (student_data.max_count -40)*2.5])
            writer.writerow([
              smart_str(student_data.name),
              smart_str(student_data.bits_id),
              smart_str(student_data.max_count),
              smart_str(student_data.current_count),
              smart_str(student_data.max_count - 40),
              smart_str((student_data.max_count - 40 )*2.5),
              ])
            dataframe  = dataframe.append(temp_dataframe)

        return response




def count_change(request):
        idd = request.POST.get('id')
        counter = int(request.POST.get('counter'))
        stud1 = student.objects.filter(bits_id = idd)[0]
        stud1.max_count = stud1.max_count + counter
        stud1.save()
        '''
        length = len(data.objects.filter(idd=idd))
        if (length > 0):
                dataobj = data.objects.filter(idd=idd)[length-1]
        dataobj.count = counter
        dataobj.save()
        '''
        return render(request,'laundry/adminpage.html')

def pass_change(request):
        print ("pass_change() started..")
        new_password = request.GET['new_pass']
        user_id = request.GET['datas_obj']
        print ("New password is: "+ new_password)
        #a = student.objects.all(bits_id=user_id)[0]
        a = student.objects.filter(bits_id= user_id)[0]
        a.password = new_password
        a.save()
        length = len (data.objects.filter(idd=user_id))
        data_obj = data.objects.filter(idd=user_id)[length-1]
        stud_obj = student.objects.filter(bits_id=user_id)[0]
        return render(request,'laundry/validation.html',{'data':data_obj,'userinfo':stud_obj})
        
        
def forgot(request):
        
        #print (request.GET['Username'])
        bits_id = request.GET.get('Username')
        print ("I got this..")
        print (bits_id)
        that_student = student.objects.filter(bits_id = bits_id)[0]
        that_student_password = that_student.password
        print (that_student_password)
        subject = 'Laundry Password'
        msg = 'Hello ' + str(that_student.name)+',\n\n Your password is: '+str(that_student_password)
        recepient = that_student.email_id
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.ehlo()
        server.starttls()
        server.login('bpdcict@gmail.com','bpdc1234')
        message = 'Subject: {}\n\n{}'.format(subject,msg)
        #print (message)
        server.sendmail('pramod@dubai.bits-pilani.ac.in',recepient,message)
        return HttpResponse("<h2>DONE</h2>")


def resetting(request):
  stud = student.objects.all()
  for x in stud:
    if (x.usertype == "student" and x.inactive_status =="active"):
      x.max_count = 40
      x.current_count = 0
      x.save()
    elif (x.usertype == "staff" and x.inactive_status =="active"):
      x.max_count =72
      x.current_count = 0
      x.save()
  return HttpResponse ("<h2> Reset Successful !! </h2>")
  
    
  
