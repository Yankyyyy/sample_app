// //Custom Button

// frappe.ui.form.on('Customer', {
//   refresh: function(frm) {
//       frm.add_custom_button(__("Create Sales Order"), function(sub){
//             frappe.prompt([
//     {
//         label: 'Item',
//         fieldname: 'item_name',
//         fieldtype: 'Link',
//         options: 'Item',
//     },
//     {
//         label: 'Select Variant',
//         fieldname: 'select_variant',
//         fieldtype: 'Data',
//         options:'Select Variant',
//     },
//     {
//         label: 'Quantity',
//         fieldname: 'quantity_no',
//         fieldtype: 'Data',
//         options: 'Quantity',
//     },
//     ], (values) => {
//         frappe.new_doc("Sales Order", {"customer": frm.doc.name},
//             doc => {
//             doc.delivery_date = frappe.datetime.get_today();
//             let row = frappe.model.add_child(doc, "items");
//             row.item_code = values.item_name;
//             row.delivery_date =  frappe.datetime.get_today();
//             row.qty = values.quantity_no;
//         });
       
//     });
//         });
//   },
// });

// // Email button

// frappe.ui.form.on('Shahaazdt', {
//     refresh(frm) {
// cur_frm.page.add_action_icon(__("fa fa-envelope-o"), function() {
//     frappe.msgprint("Custom email or print");
//     new frappe.views.CommunicationComposer();
// });
//     }
// });





// //Populating field

// frappe.ui.form.on('YankyDT','before_save',                                      //YankyDT is a custom doctype and before_save is the trigger
//     function(frm,cdt,cdn) {
//         var birth_day = frm.doc.dob;                                            //fetches the dob data from form field and put it on variable birth_day
//         var pieces1 = birth_day.split("-");                                     //splits the birth_day into date, month and year
//         var birth_year = pieces1[0];                                            //My date formate is yyyy-mm-dd. So, pieces1[0] has only the year
//         var birth_month = pieces1[1];                                           //pieces1[1] is the month
//         var birth_date = pieces1[2];                                            //pieces1[2] is the date
//         var present_day = frm.doc.p_date;                                       //fetches the present day from form
//         var pieces2 = present_day.split("-");                                   //splits the present_day into date, month and year
//         var present_year = pieces2[0];                                          //puts the year into a variable
//         var present_month = pieces2[1];                                         //I think you know what this line does
//         var present_date = pieces2[2];                                          //and this line too
//         var age = present_year - birth_year;                                    //Age is calculate by the difference in the birth year and present year
//                                                                                 //But date and month needs to be considered to find the exact age
//         if(present_month >= birth_month && present_date >= birth_date){         //And so, the months and date are being compared here for accuracy
//             age += 0;
//         }                                                                       //If the birth month and date has passed the age is found to be true
//         else if(present_month >= birth_month && present_date <= birth_date){    //But if the months are same but birth date hasn't been passed yet
//             age -= 1;                                                           //This years birth day hasn't been celebrated yet
//         }                                                                       //Thus, the the age is one year lesser than the difference in years
//         else{                                                                   //And last, if the birth month hasn't been reach yet the present year
//             age -= 1;                                                           //The age is reduced by one just like in the last condition
//         }
//         cur_frm.set_value("age", age);                                          //This is the syntax/code to fill in a field value in the form
// });    





// //Dialog, next function and delay

// frappe.ui.form.on('Article','refresh',                                                //YankyDT is a custom doctype and refresh is the trigger
//     function(frm) {                                                                     //The main function starts here
//         frappe.show_alert('Hello Guys!', 4);                                            //Alert Massage in the bottom right corner
//         setTimeout(function(){                                                          //Time Delay Function
//             frappe.msgprint('We are going to have fun with Dialog Box today!');         //Massage in top center
//         },3000);                                                                        //Delay in ms


// setTimeout(function(){                                                                  //Timer to wait for the opening function to run it's course
//     frappe.confirm('Are you sure you want to proceed?',                                 //Confirm fuction
//     () => {                                                                             //'if yes', run this functions
//                                                                                         //()=> is same as function()
//         (function(next) {                                                               //To execute this function first
// frappe.prompt([                                                                         //Prompt box to get data from user
//     {'fieldname': 'date', 'fieldtype': 'Date', 'label': 'Birth Date', 'reqd': 1}        //Field details. Explaination is in the next prompt function
// ],
// function(values){                       //Calls the event/function with parameter values
//     show_alert(values.date, 4);         //shows the alert for 4 secs
//     next();                             //Allows the next function to execute. This avoids dialog box overlapping each other
// },
// 'Age verification',                     //Displayed as Header
// 'Subscribe me'                          //Displayed as a button
// );
// }

// // The prompt function can also be coded in the way shown below

// (function() {                           //The second function that is executed only after the first function is executed
// frappe.prompt({                         //Alternate syntax for prompt function
//     label: 'Name',                      //Lebel that will be prompted
//     fieldname: 'name',                  //Data collected is named 'name'
//     fieldtype: 'Data'                   //The type of date to be collected
// }, (values) => {                        //Calls the event/function with parameters values. It is just a fancy syntex for "function(values)"
//     frappe.msgprint({title: 'Good Job', //Title of the massage to be printed
//     indicator: 'Red',                   //Title indicator colour
//     message: (values.name)              //Massage to be printed. Don't forget to put the fieldname with values
//     });
// });
// }));

// }, () =>{                                                   //Continuation for confirm function. This is the 'if no' part
//     frappe.throw('Wrong choice buddy.');                    //Shows an error dialog
// });
// },6000);                                                    //6 seconds delay
// });                     //The main function ends here.
//                         //It is important to run all the other function and events inside the main function to utilise refresh trigger on the whole code





// // Validation

// frappe.ui.form.on('Sign_Up_Form', "refresh", function(frm){
    
//     frm.add_custom_button(__("Click to Validate the Password"), function(){
    
//         var passw_1 = frm.doc.passw;
//         var passw_2 = frm.doc.re_passw;
        

 

//         if(passw_1.length <=8 || passw_1.match(/[0-9]/) === null || passw_1.match(/[A-Z]/) === null || passw_1.match(/[!@#$%^&*]/) === null){
//             frappe.throw("Weak Password !!");
//             refresh(frm);
//         }
//         else if (passw_1 != passw_2){
//             frappe.throw("Password does not match in both the fields !");
//             refresh(frm);
//         }
//         else{
//             show_alert("That's a good Password, " + frm.doc.the_name + "!")
//         }
//     });
// });

// //Email button

// frappe.ui.form.on("YankyDT_N", {
//     refresh(frm) {
// cur_frm.page.add_action_icon(__("Email"), function() {
//     frappe.msgprint("Custom email or print");
//     new frappe.views.CommunicationComposer();
// });
//     }
// });


// //Validation

// frappe.ui.form.on('YankyDT_N', 'validate', function(frm) {
//     if (frm.doc.age < 18) {
//         frappe.throw('You are underage');
//     }
// });



// //Buttons

// cur_frm.page.add_menu_item(__("Custom Print"), function() {
// 	frappe.msgprint("Printed Document");
// 	cur_frm.print_doc();
// });

// cur_frm.add_custom_button(__("Show Info"), function() {
//     frappe.msgprint("Custom Information");
// });

// //adding color on custom action icons

// cur_frm.page.add_action_icon(__(“fa fa-envelope-o text-success”), function() {
// frappe.msgprint(“email”);
// new frappe.views.CommunicationComposer();
// });


// //Add a new row in child table ----
// let row = frm.add_child('items', {
//     item_code: 'Tennis Racket',
//     qty: 2
// });

// frm.refresh_field('items');


// //Menu/Button ----
// page.add_menu_item('Send Email', () => open_email_dialog(), true)

// frm.add_custom_button('Button name', () => {
// 	//code
// 	}




// frappe.ui.form.on("[DOCTYPE]", {
// 	refresh: function(frm) {
// 		frm.add_fetch("[LINK FIELD]", "[SOURCE]", "[TARGET]");
// 	}
// });



// //Child Table Manipulation ------

// //The following three scripts calculates the rate/amount based on quantity.

// frappe.ui.form.on("Material Request Item", {
//       rate: function(frm, cdt, cdn) {
//         var d = locals[cdt][cdn];
//         frappe.model.set_value(d.doctype, d.name, 'amount', (d.qty * d.rate));
//         var total = 0;
//         frm.doc.items.forEach(function(d) {
//             total += d.amount;
//         });
//         frm.set_value('total_amount', total);
//     },
//       qty: function(frm, cdt, cdn) {
//         var d = locals[cdt][cdn];
//         frappe.model.set_value(d.doctype, d.name, 'amount', (d.qty * d.rate));
//         var total = 0;
//         frm.doc.items.forEach(function(d) {
//             total += d.amount;
//         });
//         frm.set_value('total_amount', total);
//     },
//       amount: function(frm, cdt, cdn) {
//         var d = locals[cdt][cdn];
//         frappe.model.set_value(d.doctype, d.name, 'rate', (d.amount / d.qty));
//         var total = 0;
//         frm.doc.items.forEach(function(d) {
//             total += d.amount;
//         });
//         frm.set_value('total_amount', total);
//     }
// });


// //another one ----

// // access the Delivery Stop child table
// frappe.ui.form.on("Delivery Stop", {

// // there are different possible event triggers, but `field_name`--replacing this with the actual field name--means when value of a field in the child table is changed; need to include parameters form (frm), child doc type (cdt), and child doctype name (cdn)
//   field_name:function(frm, cdt, cdn){

// // declare a collections variable
//   var u = locals[cdt][cdn];

// // assign the value of `another_field` with `yet_another_field` when the changevalue event for `field_name` was triggered 
//   u['another_field'] = u['yet_another_field'];

// // refresh the field of the entire table, note that we are referring to the full table name as declared inside the parent form, in order to reflect the new value
//   frm.refresh_field("delivery_stops");
//     }
// });

// //another one ----

// //The following function will allow you to copy the values from a child table and paste them into another.

// frappe.ui.form.on("[TARGETDOCTYPE]", {
//     "[TRIGGER]": function(frm) {
//         frappe.model.with_doc("[SOURCEDOCTYPE]", frm.doc.[TRIGGER], function() {
//             var tabletransfer= frappe.model.get_doc("[SOURCEDOCTYPE]", frm.doc.[TRIGGER])
//             $.each(tabletransfer.[SOURCECHILDTABLE], function(index, row){
//                 var d = frm.add_child("[TARGETCHILDTABLE]");
//                 d.[TARGETFIELD1] = row.[SOURCEFIELD1];
//                 d.[TARGETFIELD2] = row.[SOURCEFIELD2];
//                 frm.refresh_field("[TARGETCHILDTABLE]");
//             });
//         });
//     }
// });
// //    [TARGETDOCTYPE] - The doctype that is being worked in.
// //       [TARGETCHILDTABLE] - The table to be populated. This value is the name of the table field in the parent doctype. *[TARGETFIELD] - The field name in the target child table.
// //    [SOURCEDOCTYPE] - The doctype that contains the information to be pulled
// //       [SOURCECHILDTABLE] - The table to pull information from. This value is the name of the table field in the parent doctype. *[SOURCEFIELD] - The field name to pull data from within the table.
// //    [TRIGGER] - What causes the function to activate.
