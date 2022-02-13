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
    def get_cat_id(self, category):
        categoty_data = {
            "Genesis":"Genesis",
            "Kia Motors":"Kia Motors",
            "Kia":"Kia Motors",
            "Hyundai":"Hyundai",
            "Modern":"Hyundai",
            "Ssangyong":"SsangYong",
            "Renault":"Renault",
            "Benz":"Mercedes Benz",
            "Chevrolet":"Chevrolet",
            "ChevroletDaewoo":"Chevrolet",
            "Jaguar":"Jaguar",
            "BMW":"BMW",
            "Land":"Land Rover",
            "Peugeot":"Peugeot",
            "Volkswagen":"Volkswagen",
            "Ford":"Ford",
            "Nissan":"Nissan",
            "Jeep":"Jeep",
            "Lexus":"Lexus",
            "Lincoln":"Lincoln",
            "Mini":"Mini Cooper",
            "Cadillac":"Cadillac",
            "Toyota":"Toyota",
            "Tesla":"Tesla",
            "Audi":"Audi",
            "Chrysler":"Chrysler",
            "Volvo":"Volvo",
            "Citroen":"Citroen",
            "Infinity":"Infinity",
            "Maserati":"Maserati",
            "Dodge":"Dodge"
        }
        get_category_id = f"""
        SELECT id FROM mg_category WHERE title LIKE '%{categoty_data[category]}%';
        """
        self.cursor.execute(get_category_id)
        return self.cursor.fetchall()[0][0]
    def addnewproduct(self,obj):
        obj["count"]=0
        obj["activity"]=1
        obj["cat_id"]=self.get_cat_id(obj["category"])
        # obj["meta_title"]=""
        # obj["meta_keywords"]=""
        # obj["meta_desc"]=""
        obj["old_price"]=""
        obj["recommend"]="0"
        obj["new"]="0"
        obj["related"]=""
        obj["inside_cat"]=""
        obj["weight"]="1"
        obj["link_electro"]="1"
        obj["currency_iso"]="USD"
        # obj["price_course"]=""
        obj["image_url"]=obj["images"]
        obj["image_title"]=obj["title"]
        obj["image_alt"]=obj["title"]
        obj["system_set"]="1"
        obj["code"]=obj["lot_number"]
        addnewproduct = f"""
        INSERT mg_product(cat_id,title,description,price,url,image_url,code,count,activity,meta_title,meta_keywords,meta_desc,old_price,recommend,new,related,1c_id,inside_cat,weight,link_electro,currency_iso,price_course,image_title,image_alt,yml_sales_notes,count_buy,system_set,related_cat)
        VALUES ("{obj["cat_id"]}","{obj["title"]}","{obj["description"]}","{obj["price"]}","{obj["url"]}","{obj["image_url"]}","{obj["code"]}","{obj["count"]}","{obj["activity"]}","{obj["meta_title"]}","{obj["meta_keywords"]}","{obj["meta_desc"]}","{obj["old_price"]}","{obj["recommend"]}","{obj["new"]}","{obj["related"]}","","{obj["inside_cat"]}","{obj["weight"]}","{obj["link_electro"]}","{obj["currency_iso"]}","{obj["price_course"]}","{obj["image_title"]}","{obj["image_alt"]}",NULL,NULL,"{obj["system_set"]}",NULL);
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
    def addproductproperty(self,lastid,obj):
        addproductproperty = f"""
        INSERT mg_product_user_property(product_id,property_id,value,product_margin,type_view)
        VALUES 
        ({lastid},160,"{obj["year"]}","","select"),
        ({lastid},161,"{obj["displacement"]}","","select"),
        ({lastid},162,"{obj["distance_driven"]}","","select"),
        ({lastid},180,"{obj["car_registration"]}","","select"),
        ({lastid},159,"{obj["transmission"]}","Механика|Автомат","select"),
        ({lastid},158,"{obj["fuel"]}","Дизель|Бензин|Газ","select"),
        ({lastid},156,"{obj["model"]}","","select"),
        ({lastid},157,"{obj["mark"]}","","select"),
        ({lastid},165,"{obj["lot_number"]}","","select"),
        ({lastid},178,"{obj["car_estimate"]}","","select"),
        ({lastid},179,"{obj["car_vin"]}","","select"),
        ({lastid},166,"{obj["auction_date"]}","","select");
        """
        self.cursor.execute(addproductproperty)