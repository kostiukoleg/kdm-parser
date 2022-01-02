import mysql.connector as mysql
import configparser
config = configparser.ConfigParser(allow_no_value=True)
config.read("settings.ini")

class AddNewProduct:
    def __init__(self):
        try:
            self.db_connection = mysql.connect(host="217.172.189.14", database="olegk202_kdm", user="olegk202_kdm", password="Kostiuk_6173")
            # addnewproduct = """
            # INSERT mg_product(cat_id,title,description,price,url,image_url,code,count,activity,meta_title,meta_keywords,meta_desc,old_price,recommend,new,related,1c_id,inside_cat,weight,link_electro,currency_iso,price_course,image_title,image_alt,yml_sales_notes,count_buy,system_set,related_cat)
            # VALUES (1,"ANDREYCar","ANDREY Description",1121,"my-url","my-img-url",41412,0,1,"","","","",0,0,"","","",1,"","USD",1121,"my-img-title","my-img-title",NULL,NULL,1,NULL);
            # """
            self.cursor = self.db_connection.cursor()
            # cursor.execute(addnewproduct)
            #cursor.fetchall()
            # lastid = cursor.lastrowid
            # print(lastid)
            # updateproduct = f"""
            # UPDATE mg_product
            # SET sort={lastid}
            # WHERE id={lastid};
            # """
            # cursor.execute(updateproduct)
            # addproductproperty = f"""
            # INSERT mg_product_user_property(product_id,property_id,value,product_margin,type_view)
            # VALUES 
            # ({lastid},160,"2011","","select"),
            # ({lastid},161,"2902","","select"),
            # ({lastid},162,"118297","","select"),
            # ({lastid},180,"2011/04/19","","select"),
            # ({lastid},159,"Механика","Механика|Автомат","select"),
            # ({lastid},158,"Дизель","Дизель|Бензин|Газ","select"),
            # ({lastid},157,"Kia Motors BONGO 3","","select"),
            # ({lastid},156,"Kia Motors","","select"),
            # ({lastid},165,"4250","","select"),
            # ({lastid},178,"A / 1","","select"),
            # ({lastid},179,"KNCSHY74CBK575562","","select"),
            # ({lastid},166,"27/12/2021","","select");
            # """
            # cursor.execute(addproductproperty)
        except Exception as e:
            print(e)
    def addnewproduct(self,cat_id,title,description,price,url,image_url,code,count=0,activity=1,meta_title="",meta_keywords="",meta_desc="",old_price="",recommend=0,new=0,related="",inside_cat="",weight=1,link_electro=1,currency_iso="USD",price_course="",image_title="",image_alt="",system_set=1):
        addnewproduct = f"""
        INSERT mg_product(cat_id,title,description,price,url,image_url,code,count,activity,meta_title,meta_keywords,meta_desc,old_price,recommend,new,related,1c_id,inside_cat,weight,link_electro,currency_iso,price_course,image_title,image_alt,yml_sales_notes,count_buy,system_set,related_cat)
        VALUES ({cat_id},{title},{description},{price},{url},{image_url},{code},{count},{activity},{meta_title},{meta_keywords},{meta_desc},{old_price},{recommend},{new},{related},"",{inside_cat},{weight},{link_electro},{currency_iso},{price_course},{image_title},{image_alt},NULL,NULL,{system_set},NULL);
        """
        self.cursor.execute(addnewproduct)
        lastid = self.cursor.lastrowid
        return lastid
    def updateproduct(self,lastid):
        updateproduct = f"""
        UPDATE mg_product
        SET sort={lastid}
        WHERE id={lastid};
        """
        self.cursor.execute(updateproduct)
    def addproductproperty(self,lastid,year,displacement,distance_driven,car_registration,transmission,fuel,model,mark,lot_number,car_estimate,car_vin,auction_date):
        addproductproperty = f"""
        INSERT mg_product_user_property(product_id,property_id,value,product_margin,type_view)
        VALUES 
        ({lastid},160,{year},"","select"),
        ({lastid},161,{displacement},"","select"),
        ({lastid},162,{distance_driven},"","select"),
        ({lastid},180,{car_registration},"","select"),
        ({lastid},159,{transmission},"Механика|Автомат","select"),
        ({lastid},158,{fuel},"Дизель|Бензин|Газ","select"),
        ({lastid},157,{model},"","select"),
        ({lastid},156,{mark},"","select"),
        ({lastid},165,{lot_number},"","select"),
        ({lastid},178,{car_estimate},"","select"),
        ({lastid},179,{car_vin},"","select"),
        ({lastid},166,{auction_date},"","select");
        """
        self.cursor.execute(addproductproperty)