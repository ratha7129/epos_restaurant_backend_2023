// Copyright (c) 2023, Tes Pheakdey and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Tour Booking", {
// 	refresh(frm) {

// 	},
// });

// Copyright (c) 2022, Tes Pheakdey and contributors
// For license information, please see license.txt

frappe.ui.form.on("Tour Booking", {
    refresh(frm){
     
        set_indicator(frm);

         if(!frm.doc.__islocal){
            var iframe = document.createElement('iframe');
            iframe.height="1122";
            iframe.width="100%";
            iframe.style="border:none"
            iframe.src = '/printview?doctype=Tour%20Packages&name=' + frm.doc.tour_package +  '&format=' + frappe.get_meta("Tour Booking").fields.find(r=>r.fieldname=='tour_package_detail_frame').default + '&no_letterhead=1&settings=%7B%7D&_lang=en';
            document.getElementById('frame').appendChild(iframe);
        }
    },
    setup(frm){
        frm.set_query("document_type", "guides_and_drivers", function(doc, cdt, cdn) {
            return {
                filters: {
                    name: ["in",["Tour Guides","Drivers"]]
                    
                }
            };
        });

       
    },   

});
frappe.ui.form.on('Tour Booking Hotels', {

   departure:function (frm,cdt, cdn) {
    let doc = locals[cdt][cdn];
    alert(doc.departure)
    if (doc.arrival && doc.departure){
        alert(frappe.datetime.get_diff( doc.departure , doc.arrival ))
        set_value("total_night", frappe.datetime.get_diff( doc.departure , doc.arrival ));
        refresh_field('hotels');
    }
  }
})


function set_indicator(frm){
    if(frm.doc.__islocal)
			return;
  
    if (frm.doc.price > 0 ) frm.dashboard.add_indicator(__("Tour Package Price: {0}",[format_currency(frm.doc.price)]) ,"blue");

    if (frm.doc.total_hotel_amount > 0 )  frm.dashboard.add_indicator(__("Hotel: {0}",[format_currency(frm.doc.total_hotel_amount)]) ,"blue");
    if (frm.doc.total_restaurant_amount > 0 )  frm.dashboard.add_indicator(__("Restaurant: {0}",[format_currency(frm.doc.total_restaurant_amount)]) ,"blue");
    if (frm.doc.total_transportation_amount > 0 )  frm.dashboard.add_indicator(__("Transportation: {0}",[format_currency(frm.doc.total_transportation_amount)]) ,"blue");

    if (frm.doc.total_additional_charge > 0 )  frm.dashboard.add_indicator(__("Additional Charge: {0}",[format_currency(frm.doc.total_additional_charge)]) ,"blue");

    if (  frm.doc.price > 0 && (frm.doc.total_additional_charge   + frm.doc.total_hotel_amount + frm.doc.total_restaurant_amount + frm.doc.total_transportation_amount)>0)  frm.dashboard.add_indicator(__("Total Charge: {0}",[format_currency(frm.doc.total_additional_charge + frm.doc.price + frm.doc.total_restaurant_amount + frm.doc.total_hotel_amount + frm.doc.total_transportation_amount)]) ,"blue");
    if (frm.doc.total_expense > 0 )  frm.dashboard.add_indicator(__("Additional Expense: {0}",[format_currency(frm.doc.total_expense)]) ,"red");
    if (frm.doc.total_paid > 0 )  frm.dashboard.add_indicator(__("Total Paid: {0}",[format_currency(frm.doc.total_paid)]) ,"green");
    if (frm.doc.balance > 0 )  frm.dashboard.add_indicator(__("Balance: {0}",[format_currency(frm.doc.balance)]) ,"red");
}

function set_query(frm,field_name, filters){ 
	 
    frm.set_query(field_name, function() {
        return {
            filters: filters
        }
    });
 
}