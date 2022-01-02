import mysql.connector as mysql
import configparser
config = configparser.ConfigParser(allow_no_value=True)
config.read("settings.ini")

try:
    db_connection = mysql.connect(host="217.172.189.14", database="olegk202_kdm", user="olegk202_kdm", password="Kostiuk_6173")
    addtoarchive = """
    UPDATE mg_product
        INNER JOIN mg_product_user_property
        ON mg_product.id = mg_product_user_property.product_id
    SET mg_product.title = CONCAT(mg_product.title, " ", mg_product_user_property.value),
        mg_product.meta_title = CONCAT(mg_product.meta_title, " ", mg_product_user_property.value),
        mg_product.code = mg_product_user_property.value,
        mg_product.meta_keywords = mg_product_user_property.value,
        mg_product.meta_desc = mg_product_user_property.value,
        mg_product.price_course = 0,
        mg_product.price = 0,
        mg_product.activity = 0
    WHERE mg_product_user_property.property_id = 179
    AND mg_product.id IN (
        select mg_p.id FROM (
                                SELECT mg_product.id
                                FROM mg_product
                                        INNER JOIN mg_product_user_property
                                                    ON mg_product.id = mg_product_user_property.product_id
                                WHERE property_id = 166
                                AND value LIKE '%s %s'
                            ) as mg_p
    );
    """ % (config['SITEMAP']['AUCTION'], config['SITEMAP']['AUCTIONDATE'])
    cursor = db_connection.cursor()
    cursor.execute(addtoarchive)
    result = cursor.fetchall()
    print(result)
except Exception as e:
    print(e)