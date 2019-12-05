from OracleDBConnector import OraDBConnect
import time
from selenium.webdriver.support.ui import Select
from datetime import date,datetime
import unixTransportConnector
import logging
WAIT_TIME=2#10
IMLICITY_TIME=5#10


command={"Start VM1ORDGEN":"RunJobs VM1ORDGEN BYREQ",
  "pingABPServer":"/users/gen/abpwrk1/J2EEServer/config/ABP-FULL/ABPServer/scripts/pingABPServer.sh"}



class VoucherManager():
    def __init__(self,driver,env,db):
        self.driver=driver
        self.driver.set_page_load_timeout(30)
        self.driver.delete_all_cookies()  # delete cookies
        self.driver.maximize_window()
        self.driver.get(env['vm_url'])
        self.env= env
        self.DBConnect=OraDBConnect(db['dbHost'],db['dbUserABP'],db['dbPassABP'],db['dbInstanceABP'],db['dbPort'])
        logging.info('Opening %s page ' % self.env['vm_url'] )
        try:
            assert 'Login' in driver.title
        except NameError:
            print("Page " + self.env["vm_url"] + " Not opened")
            logging.info('Failed to open %s page ' % self.env["vm_url"])
       # time.sleep(WAIT_TIME)


 # Let the user actually see something!t


    def login(self):
       elem =self.driver.find_element_by_name("uams_sso_username")
       elem.send_keys(self.env['vm_gui_user'])
       elem =self.driver.find_element_by_name("uams_sso_password")
       elem.send_keys(self.env['vm_gui_password'])
       self.driver.find_element_by_css_selector("input[type='image']").click()
       logging.info('Login to [%s] page with [%s] user ' ,self.env["vm_url"],self.env['username'])
       print('Logged in to %s page ' % self.env["vm_url"])
       self.driver.find_element_by_xpath("/html/body/table[2]/tbody/tr[4]/td[1]/a[2]/img").click()  # Click Order



# ########################### Create Order ################################
    def createOrder(self,voucher_value=50,order_size=40,package_size=20):
       """Creates Order , if not defined then set voucher_value,order_size,packagesize with default value  ,set manufacturer as index[1] ,set voucher_type as index[1]
        ,run VM1ORDGEN job,  return created Order ID """
       #self.driver.find_element_by_xpath("/html/body/table[2]/tbody/tr[4]/td[1]/a[2]/img").click() #Click Order
       self.driver.find_element_by_xpath("//*[@id='OUT1t']").click() #'VM Ordering'- click Order Creation
       manufacturer =Select(self.driver.find_element_by_xpath("/html/body/table[3]/tbody/tr[2]/td[2]/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/select"))
       manufacturer.select_by_index(1)# select Vmanufacturer from dropdown

       voucher_type =Select(self.driver.find_element_by_xpath("/html/body/table[3]/tbody/tr[2]/td[2]/table/tbody/tr[2]/td/table/tbody/tr[3]/td[2]/select"))
       voucher_type.select_by_index(1) # select Voucher Type from dropdown

       voucher_exp_date =self.driver.find_element_by_name("voucherEXPDate")
       v_exp_date=str(datetime.now().day+1)+'/'+str(datetime.now().month)+'/'+ str(datetime.now().year+1)
       voucher_exp_date.send_keys(v_exp_date)
       #voucher_exp_date.send_keys(datetime.strftime(exp_date, '%d-%m-%Y'))#now.strftime("%Y-%m-%d %H:%M")
       #print (type(datetime.now().year),datetime.now().year,type(datetime.now()),datetime.now())
       pack_exp_date =self.driver.find_element_by_name("packageEXPDate")
       p_exp_date =str(datetime.now().day)+'/'+str(datetime.now().month)+'/'+ str(datetime.now().year+1)
       pack_exp_date.send_keys(p_exp_date)

       vaucher_val_elem =self.driver.find_element_by_name("voucherValue")
       vaucher_val_elem.send_keys(voucher_value)

       order_size_elem =self.driver.find_element_by_name("orderSize")
       order_size_elem.send_keys(order_size)

       pack_size_elem =self.driver.find_element_by_name("packageSize")
       pack_size_elem.send_keys(package_size)

       self.driver.find_element_by_xpath("/html/body/table[3]/tbody/tr[2]/td[2]/table/tbody/tr[3]/td[1]/input").click()
       time.sleep(WAIT_TIME)

       order_id=self.driver.find_element_by_xpath("//tr[2]/td[@class='fieldText']").text
       order_status = self.driver.find_element_by_xpath("//tr[14]/td[@class='fieldText']").text
       #Click back in order to return to Main Menu
       Back_button = self.driver.find_element_by_xpath("//td[1]/a/img[@align='left'and @name='imageField']")
       Back_button.click()
       logging.info('Order [%s] ,status=[%s] is created' ,order_id,order_status )
       print('createOrder -Order %s is Created ' % order_id )
       #unixTransportConnector.execute_ssh_command(self.env['host'], self.env['port'], self.env['username'], self.env['password'], None, None,command['Start VM1ORDGEN'])
       return order_id

# ########################### Authorize Order ##################################
    def authorizeOrder(self, orderID):
        print('Authorizing order %s' % orderID)
        logging.info('Authorizing order [%s] ', orderID)
        #click on Authorize order link
        self.driver.find_element_by_xpath("//tr[3]/td/a[@id='OUT1t']").click()
        #set Order Id for Search
        order_id_elm=self.driver.find_element_by_xpath("//input[@name ='orderId']")
        order_id_elm.send_keys(orderID)
        #Click On Search
        Search_button = self.driver.find_element_by_xpath("//input[@align='right'and @name='imageField']")
        Search_button.click()
        logging.info('Searchin Order [%s] to Authorize  ', orderID)
        print ('Searchin Order %s to Authorize  '% orderID)
        #check if Order is returned in order list
        order_id_link_elm=self.driver.find_element_by_xpath("//tr[3]/td/a[@class='tableLinks']")
        if order_id_link_elm.text==orderID :
          print('authorizeOrder -Order %s is found in Order List Search result ' % orderID)
          #Autthorize Order -click on order link
          order_id_link_elm.click()
        else:
         logging.info('Order [%s] not found for Authorization ', orderID)
        order_id = self.driver.find_element_by_xpath("//tr[2]/td[@class='fieldText']").text

        print('authorizeOrder -Click Authotize for order %s  ' % order_id)
        Authorize_button =self.driver.find_element_by_xpath("//input[@align='right'and @name='autorizeImageField']")
        Authorize_button.click()
        authorized_order_id = self.driver.find_element_by_xpath("//tr[2]/td[@class='fieldText']").text
        #return to main menu
        Back_button = self.driver.find_element_by_xpath("//td[1]/a/img[@align='left'and @name='imageField']")
        Back_button.click()
        Main_menu_link =self.driver.find_element_by_xpath("//tr[1]/td/a[@class='tableLinks']")
        Main_menu_link.click()
        return authorized_order_id

    def runVM1ORDGEN(self):
       unixTransportConnector.execute_ssh_command(self.env['host'], self.env['port'], self.env['username'], self.env['password'], None, None,command['Start VM1ORDGEN'])
       time.sleep(WAIT_TIME*12)

    def db_get_order_status(self,order_id):
        cursor = self.DBConnect.db.cursor()
        cursor.execute('select status from VM1_ORDER where order_id =:orderID',orderID=order_id)  # cursor.fetchone()
        print cursor.description
          # cursor.fetchone()
        result = cursor.fetchall()
        cursor.close()
        print ("Oredr status: %s" % result[0][0])
        return result[0][0]

    def __del__(self):
        print('Running VoucherManager distructor')
        self.driver.delete_all_cookies()
        try:
         self.driver.quit()
        except:
         print ('Failed to quit driver , can be that browser already closed manually')
       # print ("VM DB connection   is closing!")
        #self.DBConnect.db.cursor.close()
       # print ("VM cursor is closed by DB Desctractor!")
        #self.DBConnect.db.close()
        #print ("VM DB is closed by Desctractor!")



"""
Click and Wait example
try:
    elem = WebDriverWait(driver, 10).until( EC.presence_of_element_located((By.NAME, 'uams_sso_user_name')))
    elem.send_keys(userF)

finally:
    time.sleep(10)
    driver.quit()
    print  "Stop!"
"""







"""
#handling Alert
try:
    WebDriverWait(driver, 30).until(EC.alert_is_present(), 'Waiting for alert timed out')
    alert = driver.switch_to.alert()
    alert.accept()
    print "alert accepted"

except TimeoutException:
    print "no alert"
"""

#save to Fille current HTML Source
#print(type(driver.page_source))
#fh= open ("testPageSource.htm","w")
#fh.write( fileContent=u''.join(i for i in driver.page_source).encode('utf-8').strip())  # write to file
#fh.close()


#logout

