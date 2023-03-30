import frappe
import datetime
import json


def after_install():
    # ceate table group
    if not frappe.db.exists("Table Group", "Main Group"):
        doc = frappe.get_doc(
          {
            "name": "Main Group",
            "outlet": "Main Outlet",
            "business_branch": "Main Branch",
            "table_group_name_en": "Main Group",
            "table_group_name_kh": "Main Group",
            "disabled": 0,
            "is_standard": 1,
            "doctype": "Table Group",
            "photo": "/images/defaulttable_bg.jpg"
        }
        )
        doc.insert()

    #create table 
    create_table("01")
    create_table("02")
    create_table("03")
    create_table("04")
    create_table("05")
    create_table("06")
    create_table("07")
    create_table("08")
    create_table("09")
    create_table("10")


    #create note
    create_note("Edit Closed Receipt",["Wrong Payment","Wrong Product","Guest Cancel","Cashier Error"])

def create_note(name, note_list):
    if not frappe.db.exists("Category Note", note_list):
        notes = []
        for n in note_list:
            notes.append({"note":n})
        
        doc = frappe.get_doc(
        {
            "name": name,
            "category_note_name_en": name,
            "category_note_name_kh": name,
            "disabled": 0,
            "multiple_selected": 0,
            "doctype": "Category Note",
            "notes": notes
        }
        )
        doc.insert()

#create table
def create_table(tbl_no):
    if not frappe.db.exists("Table Group", "Main Group"):
        doc = frappe.get_doc(
         {
            "tbl_number": tbl_no,
            "tbl_group": "Main Group",
            "width": 100,
            "height": 85,
            "shape": "Rectangle",
            "discount_type": "Percent",
            "default_discount": 0,
            "price_rule": "",
            "sale_type": "Dine In",
            "require_check_in": 0,
            "doctype": "Tables Number"
            }
        )
        doc.insert()

def replace_format(string,year):
     
    year_short = str(datetime.datetime.now().year)[-2:]
    month = str(datetime.datetime.now().month).zfill(2)
    digit = str(1).zfill(4)
    return string.replace('.', '').replace('YYYY', year).replace('yyyy', year).replace('YY', year_short).replace('yy', year_short).replace('MM', month).replace('#', '')


## RESET SALE TRANSACTION
@frappe.whitelist()
def reset_sale_transaction():
    # backupd db first
    if frappe.session.user == 'Administrator':
        frappe.db.sql("delete from `tabCash Transaction`")
        frappe.db.sql("delete from `tabPOS Sale Payment`")
        frappe.db.sql("delete from `tabSale Payment`")
        frappe.db.sql("delete from `tabSale Product`")
        frappe.db.sql("delete from `tabSale`")
        frappe.db.sql("delete from `tabCashier Shift Cash Float`")
        frappe.db.sql("delete from `tabCashier Shift`")
        frappe.db.sql("delete from `tabWorking Day`")
        frappe.db.sql("delete from `tabComment` where reference_doctype in ('Sale','POS Sale Payment','Sale Payment','Sale Product','Cashier Shift Cash Float','Cashier Shift','Working Day')")

        #reset sale transaction 
        doctypes = ["Sale","Sale Payment","Cashier Shift","Working Day","Cash Transaction"]
        for d in doctypes:
            if frappe.get_meta("Sale").get_field("naming_series"):
                formats =  frappe.get_meta(d).get_field("naming_series").options
                if formats:
                    for f in formats.split("\n"):
                        for n in range(2022, 2030):
                            format_text = replace_format(f,str(n))                            
                            frappe.db.sql("update `tabSeries` set current=  0 where name='{}'".format(format_text) )
        

        frappe.db.commit()

        return "Done"
    else:
        return "Please login as administrator"

## END RESET SALE TRANSACTION

## RESET DATABASE Method
@frappe.whitelist()
def reset_database():
    #step 1 reset sale transaction
    reset_sale_transaction()
    #step 2 reset data
    reset_data()
    #step 3 create predefine data
    create_predefine_data()

## END RESET DATABASE

## RESET DATA Method
@frappe.whitelist()
def reset_data():
    if frappe.session.user == 'Administrator':
        #update 
        frappe.db.sql("update `tabSeries` set current = 0")
        frappe.db.sql("update `tabLanguage` set enabled =0 where name not in ('kh','en')")

        # delete 
        frappe.db.sql("delete from `tabInventory Transaction`")
        frappe.db.sql("delete from `tabUnit of Measurement Conversion`")
        frappe.db.sql("delete from `tabStock Location Product`")
        frappe.db.sql("delete from `tabStock Adjustment Product`")
        frappe.db.sql("delete from `tabStock Adjustment`")
        frappe.db.sql("delete from `tabStock Transfer Products`")
        frappe.db.sql("delete from `tabStock Transfer`")
        frappe.db.sql("delete from `tabStock Take Products`")
        frappe.db.sql("delete from `tabStock Take`")
        frappe.db.sql("delete from `tabStock Location`")
        frappe.db.sql("delete from `tabModifiers`")
        frappe.db.sql("delete from `tabModifier Code`")
        frappe.db.sql("delete from `tabModifier Category`")
        frappe.db.sql("delete from `tabProduct Printer`")
        frappe.db.sql("delete from `tabProduct Menu`")
        frappe.db.sql("delete from `tabProduct Price`")
        frappe.db.sql("delete from `tabPurchase Order Payment`")
        frappe.db.sql("delete from `tabPurchase Order Products`")
        frappe.db.sql("delete from `tabPurchase Order`")
        frappe.db.sql("delete from `tabVendor`")
        frappe.db.sql("delete from `tabVendor Group`")
        frappe.db.sql("delete from `tabCustomer`")
        frappe.db.sql("delete from `tabCustomer Group`")
        frappe.db.sql("delete from `tabSale Quotation Product`")
        frappe.db.sql("delete from `tabSale Quotation`")
        frappe.db.sql("delete from `tabEmployee Emergency Contact`")
        frappe.db.sql("delete from `tabEmployee Exit Type`")
        frappe.db.sql("delete from `tabCheck In Out`")
        frappe.db.sql("delete from `tabDepartment`")
        frappe.db.sql("delete from `tabPosition`")
        frappe.db.sql("delete from `tabAttendance`")
        frappe.db.sql("delete from `tabShift Type`")
        frappe.db.sql("delete from `tabEmployee Type`")
        frappe.db.sql("delete from `tabEmployee`")
        frappe.db.sql("delete from `tabExpense Payment`")
        frappe.db.sql("delete from `tabExpense Item`")
        frappe.db.sql("delete from `tabExpense`")
        frappe.db.sql("delete from `tabExpense Category`")
        frappe.db.sql("delete from `tabPayment Type`")
        frappe.db.sql("delete from `tabCurrency Exchange`")
        frappe.db.sql("delete from `tabePOS Table Position`")
        frappe.db.sql("delete from `tabPOS Menu`")
        frappe.db.sql("delete from `tabUnit Of Measurement`")
        frappe.db.sql("delete from `tabUnit Category`")
        frappe.db.sql("delete from `tabTables Number`")
        frappe.db.sql("delete from `tabTable Group`")
        frappe.db.sql("delete from `tabOutlet`")
        frappe.db.sql("delete from `tabPrinter`")
        frappe.db.sql("delete from `tabKitchen Group`")
        frappe.db.sql("delete from `tabPrice Rule`")
        frappe.db.sql("delete from `tabRevenue Group`")
        frappe.db.sql("delete from `tabPayment Type Group`")
        frappe.db.sql("delete from `tabPOS Profile Payment Type`")
        frappe.db.sql("delete from `tabProduct`")
        frappe.db.sql("delete from `tabProduct Category`")
        frappe.db.sql("delete from `tabPOS Price Rule`")
        frappe.db.sql("delete from `tabPOS Table Group`")
        frappe.db.sql("delete from `tabPOS Profile Root Menu`")
        frappe.db.sql("delete from `tabTax Rule`")
        frappe.db.sql("delete from `tabTemp Product Menu`")
        frappe.db.sql("delete from `tabCashier Notes`")
        frappe.db.sql("delete from `tabCategory Note`")
        frappe.db.sql("delete from `tabPOS Profile Table Group`")
        frappe.db.sql("delete from `tabRestaurant Table`")
        frappe.db.sql("delete from `tabBusiness Branch`")

## END RESET DATA Method

## CREATE PREDEFINE DATA Method
@frappe.whitelist()
def create_predefine_data():
    if frappe.session.user == 'Administrator':
        data = frappe.db.get_list('Predefine Data',fields=["*"])
        for d in data:             
            if not frappe.db.exists(d.doc_type, d.doc_name):
                doc = frappe.get_doc(json.loads(d.data))
                doc.insert()        
        frappe.db.commit()
## END CREATE PREDEFINE DATA Method


@frappe.whitelist()
def get_server_name():
    server_name = socket.gethostname()
    return server_name