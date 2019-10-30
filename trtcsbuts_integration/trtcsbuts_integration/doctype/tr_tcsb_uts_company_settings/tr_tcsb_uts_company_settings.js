// Copyright (c) 2019, Framras AS-Izmir and contributors
// For license information, please see license.txt

frappe.ui.form.on('TR TCSB UTS Company Settings', {
	// refresh: function(frm) {

	// }
	test_realintegration: function(frm){
	    if(frm.doc.systemtoken!=""){
	        frappe.call({
	            method: "trtcsbuts_integration.api.firmasorgulatest",
	            args:{
	                test: "real",
                    testtoken: frm.doc.systemtoken
	            },
	            callback: function(r){
                    frm.set_value("realresult", r.message)
	            }
	        })
	    }
	},
		test_testintegration: function(frm){
	    if(frm.doc.testsystemtoken!=""){
	        frappe.call({
	            method: "trtcsbuts_integration.api.firmasorgulatest",
	            args:{
	                test: "test",
                    testtoken: frm.doc.testsystemtoken
	            },
	            callback: function(r){
                    frm.set_value("testresult", r.message)
	            }
	        })
	    }
	}
});
