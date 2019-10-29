// Copyright (c) 2019, Framras AS-Izmir and contributors
// For license information, please see license.txt

frappe.ui.form.on('TR TCSB UTS Integration Settings', {
	// refresh: function(frm) {

	// },
	test_realintegration: function(frm){
	    if(frm.doc.realserver!=""){
	        frappe.call({
	            method: "trtcsbuts_integration.api.firmasorgulatest",
	            args:{
                    testserver: frm.doc.realserver,
                    testtoken: frm.doc.systemtoken,
                    testcontenttype: frm.doc.contenttype
	            },
	            callback: function(r){
                    frm.set_value("realresult", r.message)
	            }
	        })
	    }
	},
		test_testintegration: function(frm){
	    if(frm.doc.realserver!=""){
	        frappe.call({
	            method: "trtcsbuts_integration.api.firmasorgulatest",
	            args:{
                    testserver: frm.doc.testserver,
                    testtoken: frm.doc.testsystemtoken,
                    testcontenttype: frm.doc.contenttype
	            },
	            callback: function(r){
                    frm.set_value("testresult", r.message)
	            }
	        })
	    }
	}
});
