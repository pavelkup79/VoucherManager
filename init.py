from rnVoucherManagment import VoucherManager
from selenium import webdriver
import killproc
import logging
#define Driver parameters  and URL
vm_url ='http://illinqw9333:11601/vm?APP_ID=VM'
driverpath ='C:\Users\pavelkup\PycharmProjects\VoucherManagment\chromedriver.exe'

#logging definition
logging.basicConfig(format='%(levelname)s:%(name)s:%(asctime)s--%(message)s' ,filename='voucherManager.log',level=logging.INFO,filemode="w")
#format
#filemode="w" -starts with ne file



#define Test  Environment parameters
env={"vm_url":"http://localhost","host" :"somehost","username":"someuser","password":"SOmepasswod","port":22,"keyfile_path":"private_key_file",
     "vm_gui_user":"guiUser","vm_gui_password" : "GUIpass" }
db ={'dbUserABP':'DBuser', 'dbPassABP':'dbpass','dbInstanceABP':'Vdbinstance','dbHost':'dbhost','dbPort':1521}


#Define Test Data
voucher_value=50
order_size=40
package_size=20 #order consist of packages

#Initialize
killproc.KillProcesses()
driver = webdriver.Chrome(driverpath)



#Run  Test
MyVM = VoucherManager(driver,env,db)
MyVM.login()# login and open Main menu
orderID = MyVM.createOrder()
authorized_order_id = MyVM.authorizeOrder(orderID)
MyVM.runVM1ORDGEN()
MyVM.db_get_order_status(authorized_order_id)
