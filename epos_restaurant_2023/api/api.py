import json
import time
import frappe
import base64
from py_linq import Enumerable
from frappe import _
@frappe.whitelist(allow_guest=True)
def check_username(pin_code):
    if pin_code:    
        pin_code = (str( base64.b64encode(pin_code.encode("utf-8")).decode("utf-8")))
        data = frappe.db.sql("select name from `tabUser` where pos_pin_code='{}' and allow_login_to_pos=1 limit 1".format(pin_code),as_dict=1)
        if data:
            return {"username":data[0]["name"]} 
        
    frappe.throw(_("Invalid pin code"))
    

@frappe.whitelist(allow_guest=True)
def get_system_settings(pos_profile="", device_name=''):
    if not frappe.db.exists("POS Profile",pos_profile):
        frappe.throw("Invalid POS Profile name")
    
    profile = frappe.get_doc("POS Profile",pos_profile)
    pos_config = frappe.get_doc("POS Config",profile.pos_config)

    doc = frappe.get_doc('ePOS Settings')
    table_groups = []
    for g in profile.table_groups:
        
        table_groups.append({"key":g.table_group.lower().replace(" ","_"),"table_group":g.table_group,"background":frappe.get_value("Table Group",g.table_group,"photo"),"tables":get_tables_number(g.table_group, device_name),})
    pos_menus = []
    for m in profile.pos_menus:
        pos_menus.append({"pos_menu":m.pos_menu})   
        
    payment_types=[]
    for p in profile.payment_types:
        
        payment_types.append({"payment_method":p.payment_type,"allow_cash_float":p.allow_cash_float, "input_amount":0,"exchange_rate":p.exchange_rate})
    
    #get currency
    currencies = frappe.db.sql("select name,symbol,currency_precision,symbol_on_right from `tabCurrency` where enabled=1", as_dict=1)
    
    #main currency information
    main_currency = frappe.get_doc("Currency",frappe.db.get_default("currency"))
    second_currency = frappe.get_doc("Currency",frappe.db.get_default("second_currency"))
    
    pos_setting={
        "business_branch":profile.business_branch,
        "business_name_en":pos_config.business_name_en,
        "business_name_kh":pos_config.business_name_kh,
        "address":pos_config.address,
        "address_en":pos_config.address_kh,
        "logo":pos_config.logo,
        "phone_number":pos_config.phone_number,
        "main_currency_name":main_currency.name,
        "main_currency_symbol":main_currency.symbol,
        "main_currency_format":main_currency.pos_currency_format,
        "second_currency_name":second_currency.name,
        "second_currency_symbol":second_currency.symbol,
        "second_currency_format":second_currency.pos_currency_format,
        "thank_you_message":pos_config.thank_you_message
        
    }
    
    #get default customre
    
    if not profile.default_customer:
        frappe.throw("There is no default customer for pos profie {}".format(pos_profile))
    
    default_customer = frappe.get_doc("Customer", profile.default_customer)
    
    
    data={
        "app_name":doc.epos_app_name,
        "business_branch":profile.business_branch,
        "address":pos_config.address,
        "logo":pos_config.logo,
        "phone_number":pos_config.phone_number,
        "pos_profile":pos_profile,
        "outlet":profile.outlet,
        "price_rule":profile.price_rule,
        "stock_location":profile.stock_location,
        "tax_rule":profile.tax_rule,
        "login_background":pos_config.login_background,
        "home_background":pos_config.home_background,
        "thank_you_background":pos_config.thank_you_background,
        "table_groups":table_groups,
        "pos_menus":pos_menus,
        "default_pos_menu":profile.default_pos_menu,
        "payment_types":payment_types,
        "tax_1_name":doc.tax_1_name,
        "tax_2_name":doc.tax_2_name,
        "tax_3_name":doc.tax_3_name,
        "use_guest_cover":doc.use_guest_cover,
        "sale_status":frappe.db.sql("select name,background_color from `tabSale Status`", as_dict=1),
        "print_cashier_shift_summary_after_close_shift":doc.print_cashier_shift_summary_after_close_shift,
        "print_cashier_shift_sale_product_summary_after_close_shift":doc.print_cashier_shift_sale_product_summary_after_close_shift,
        "pos_sale_order_background_image":doc.pos_sale_order_background_image,
        "currencies":currencies,
        "default_currency":frappe.db.get_default("currency"),
        "pos_setting":pos_setting,
        "customer":default_customer.name,
        "customer_name":default_customer.customer_name_en,
        "customer_photo":default_customer.photo,
        "allow_change_quantity_after_submit":profile.allow_change_quantity_after_submit
        
    }
    return  data

@frappe.whitelist(allow_guest=True)
def get_tables_number(table_group,device_name):
    data = frappe.get_all("Tables Number",
                fields=["name as id","tbl_number as tbl_no","shape","sale_type","default_discount","height as h","width as w","price_rule"],
                filters={"tbl_group":table_group}
            )
    background_color = frappe.db.get_default("default_table_number_background_color")
    for d in data:
        d.background_color=background_color
        position = frappe.db.sql("select x,y,h,w from `tabePOS Table Position` where device_name='{}' and tbl_number='{}' limit 1".format(device_name,d.tbl_no ), as_dict=1)
        if position:
            for p in position:
                d.x = p.x or 0
                # if d.x < 0:
                #     d.x = 0
                    
                # if d.y<0:
                #     d.y=0
                
                d.y = p.y or 0
                d.w = p.w or 100
                d.h = p.h or 100
    return data

@frappe.whitelist(allow_guest=True)
def check_pos_profile(pos_profile_name):
    if not frappe.db.exists("POS Profile", pos_profile_name):
        frappe.throw("Invalid POS Profile")
    return


@frappe.whitelist()
def get_current_working_day(pos_profile):
   
    sql = "select name, posting_date, pos_profile, note from `tabWorking Day` where pos_profile = '{}' and is_closed = 0 order by creation limit 1".format(pos_profile)
    data =  frappe.db.sql(sql, as_dict=1) 
    if data:
        return data [0]
    return

@frappe.whitelist()
def get_current_cashier_shift(pos_profile):
   
    sql = "select name,working_day, posting_date, pos_profile, opened_note from `tabCashier Shift` where pos_profile = '{}' and is_closed = 0 order by creation limit 1".format(pos_profile)
    data =  frappe.db.sql(sql, as_dict=1) 
    if data:
        return data [0]
    return

@frappe.whitelist()
def get_user_information():
    data = frappe.get_doc("User",frappe.session.user)
    return {
        "name":data.name,
        "full_name":data.full_name,
        "role":data.role_profile_name,
        "phone_number":data.phone,
        "photo":data.user_image
    }
    
    
@frappe.whitelist()
def save_table_position(device_name, table_group):
    # frappe.throw("{}".format(table_group))
    frappe.db.sql("delete from `tabePOS Table Position` where device_name='{}'".format(device_name) )
    
    for g in table_group:
        
        for t in g['tables']:
            x = 0
            if "x" in t:
                x = t["x"]
            y = 0
            if "y" in t:
                y = t["y"]
            h = 0
            if "h" in t:
                h = t["h"]
            w = 0
            if "w" in t:
                w = t["w"]
            if not frappe.db.exists('ePOS Table Position', {'tbl_number': t['tbl_no'], 'device_name': device_name}):
                doc = frappe.get_doc({
                        'doctype': 'ePOS Table Position',
                        'device_name':device_name,
                        'tbl_number': t['tbl_no'],
                        'x':x,
                        'y':y,
                        'h':h,
                        'w':w
                    })
                doc.insert()

@frappe.whitelist()
def get_pos_print_format(doctype):
    data = frappe.db.sql("select name,print_invoice_copies, print_receipt_copies,pos_invoice_file_name, pos_receipt_file_name, receipt_height, receipt_width,receipt_margin_top, receipt_margin_left,receipt_margin_right,receipt_margin_bottom  from `tabPrint Format` where doc_type='{}' and show_in_pos=1 and disabled=0".format(doctype), as_dict=True)
    
    if data:
       return data
    else:
        return [{"name":"Standard","pos_invoice_file_name":""}]

@frappe.whitelist()
def get_pos_letter_head(doctype):
    
    data = frappe.db.sql("select name from `tabLetter Head` where   disabled=0", as_dict=True)
    
    if data:
        arr =[]
        for d in data:
            arr.append(d.name)
        return arr
     


@frappe.whitelist()
def get_close_shift_summary(cashier_shift):
    data = []
    doc = frappe.get_doc("Cashier Shift",cashier_shift)
    
     
    #get close amount by payment type
    sql = "select payment_type, currency,sum(input_amount) as input_amount, sum(payment_amount) as payment_amount from `tabSale Payment` where cashier_shift='{}' and docstatus=1 group by payment_type, currency".format(cashier_shift)
    payments = frappe.db.sql(sql, as_dict=1)
    
    
    for d in doc.cash_float:
        
        data.append({
            "name":d.name,
            "payment_method":d.payment_method,
            "exchange_rate":d.exchange_rate,
            "input_amount":d.input_amount,
            "opening_amount":d.opening_amount,
            "input_close_amount":0,
            "input_system_close_amount":d.input_amount +  Enumerable(payments).where(lambda x:x.payment_type == d.payment_method).sum(lambda x: x.input_amount or 0 ),
            "system_close_amount": d.opening_amount +  Enumerable(payments).where(lambda x:x.payment_type == d.payment_method).sum(lambda x: x.payment_amount or 0 ),
            "different_amount":0,
            "currency":d.currency
        })
    
    
    for p in payments:
        if not p.payment_type  in [d.payment_method for d in doc.cash_float]:
            data.append({
                "payment_method":p.payment_type,
                "exchange_rate":frappe.db.get_value("Payment Type", p.payment_type, "exchange_rate"),
                "input_amount":0,
                "opening_amount":0,
                "input_close_amount":0,
                "input_system_close_amount": p.input_amount,
                "system_close_amount": p.payment_amount,
                "different_amount":0,
                "currency":p.currency
            })
            
    
        
    return data

@frappe.whitelist()
def get_meta(doctype):
    data =  frappe.get_meta(doctype)
    return data