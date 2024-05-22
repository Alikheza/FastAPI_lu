from typing import ClassVar
from datetime import datetime 
from pydantic import BaseModel , root_validator 
from re import fullmatch 

class user_Info(BaseModel):

    '''This is a class for users data validation.
      If you want your data to be checked correctly, 
      please send the data according to the names mentioned below'''
    
    user_Fname : str 
    user_Lname : str
    user_birthday : str
    user_ID : str
    user_province : str
    user_borncity :str 
    user_address : str 
    user_postal_code : str
    user_phone_number : str
    user_home_number : str 
    user_department : str
    user_major : str 
    detail : ClassVar ={}

    def user_info_check(cls,values):

        def user_name_check(Fname,Lname,detail) :
            pattern = r"^[آ-ی]+$"
            if len(Fname)>10 : detail['user_Fname'] = 'نام نمیتواند بیشتر از ۱۰ کاراکتر باشد'
            elif fullmatch(pattern,Fname)== None: detail['user_Fname'] = 'نام فقط میتواند حاوی کارکتر های فارسی باشد'
            if len(Lname)>10 : detail['user_Lname'] = 'نام خانوادگی نمیتواند بیشتر از ۱۰ کاراکتر باشد'
            elif fullmatch(pattern,Lname)== None: detail['user_Lname'] = 'نام خانوادگی فقط میتواند حاوی کارکتر های فارسی باشد'
            return detail
        
        
        def user_birthday_check(birthday,detail):
            try :
                birthday=datetime.strptime(birthday,'%Y-%m-%d')
                if (birthday.year < 1330 or birthday.year > 1390) or (birthday.month not in range(1,13)) or birthday.day not in range (1,32) :
                    detail['user_birthday']='تاریخ تولد وارد شده نامعتبر است'
            except:
                detail['user_birthday']='تاریخ تولد وارد شده نامعتبر است'
            return detail
        
        def user_ID_check(Id, detail):
            if len( Id )!=10 or Id.isdigit()==False : detail['user_ID'] ='کدملی نامعتر است'
            return detail
        
        
        def user_borncity_check(userprovince,usercity,detail):
            iran_provinces = {"آذربایجان شرقی": "تبریز","آذربایجان غربی": "ارومیه","اردبیل": "اردبیل","اصفهان": "اصفهان","البرز": "کرج",
                              "ایلام": "ایلام","بوشهر": "بوشهر","تهران": "تهران","چهارمحال و بختیاری": "شهرکرد","خراسان جنوبی": "بیرجند",
                              "خراسان رضوی": "مشهد","خراسان شمالی": "بجنورد","خوزستان": "اهواز","زنجان": "زنجان","سمنان": "سمنان","سیستان و بلوچستان": "زاهدان",
                              "فارس": "شیراز","قزوین": "قزوین","قم": "قم","کردستان": "سنندج","کرمان": "کرمان","کرمانشاه": "کرمانشاه","کهگیلویه و بویراحمد": "یاسوج",
                              "گلستان": "گرگان","گیلان": "رشت","لرستان": "خرم‌آباد","مازندران": "ساری","مرکزی": "اراک","هرمزگان": "بندرعباس","همدان": "همدان","یزد": "یزد"}
            if iran_provinces.get(userprovince)==None:
                detail['user_province']=' استان نامعتبر است' 
            elif iran_provinces[userprovince] != usercity :
                detail['user_borncity']='ترکیب استان و شهر نامعتبر است'
            return detail 
        
        def user_addres_check(U_address,postalcode,detail):
            if len(U_address) >= 100 : detail['user_address']='حداکثر طول ادرس ۱۰۰ کارکتر است'
            if len(postalcode) <= 10 or postalcode.isdigit()==False : detail['user_postal_code']='کد پستی حداکثر میتواند ۱۰ رقم باشد'
            return detail
        
        
        def user_phonenumber_check(phonN,homeN,detail):
            if phonN.isdigit() == False or phonN.startswith('09')== False or len(phonN)!=11 :
                detail['user_phone_number']='شماره همراه وارد شده نامعتبر است '
            if homeN.isdigit()==False or homeN.startswith('0')== False or len(homeN)!=11 :
                detail['user_home_number']='تلفن ثابت وارد شده نامعتبر است '
            return detail
        
        def user_department_check(department,major,detail):
            department_list =['فنی و مهندسی','علوم پایه','علوم انسانی','دامپزشکی','اقتصاد','کشاورزی','منابع طبیعی']
            major_list=["مهندسی عمران","مهندسی مکانیک","مهندسی برق","مهندسی کامپیوتر","مهندسی نرم‌افزار","مهندسی صنایع","مهندسی مواد",
                        "مهندسی پزشکی","مهندسی هوافضا","مهندسی شیمی","مهندسی مخازن","مهندسی بیومدیکال","مهندسی نفت",]
            if department not in department_list : detail['user_department']='دانشکده وارد شده معتبر نمی باشد'
            if major not in major_list : detail['user_major']='رشته تحصیلی وارد شده نامعتبر است'
            return detail

        
        #now calling the validation functions
        user_name_check(values['user_Fname'],values['user_Lname'],cls.detail)
        user_birthday_check(values['user_birthday'],cls.detail)
        user_ID_check(values['user_ID'],cls.detail)
        user_borncity_check(values['user_province'],values['user_borncity'],cls.detail)
        user_addres_check(values['user_address'],values['user_postal_code'],cls.detail)
        user_phonenumber_check(values['user_phone_number'],values['user_home_number'],cls.detail)
        user_department_check(values['user_department'],values['user_major'],cls.detail)