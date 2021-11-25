frappe.ui.form.on('Sign_Up_Form', "refresh", function(frm){
    
    frm.add_custom_button(__("Click to Validate the Password"), function(){
    
        var passw_1 = frm.doc.passw;
        var passw_2 = frm.doc.re_passw;
        

 

        if(passw_1.length <=8 || passw_1.match(/[0-9]/) === null || passw_1.match(/[A-Z]/) === null || passw_1.match(/[!@#$%^&*]/) === null){
            frappe.throw("Weak Password !!");
            refresh(frm);
        }
        else if (passw_1 != passw_2){
            frappe.throw("Password does not match in both the fields !");
            refresh(frm);
        }
        else{
            show_alert("That's a good Password, " + frm.doc.the_name + "!")
        }
    });

 });