import frappe
import requests
import json


def communicate_with_uts(servicepath, servicerequestdatafields):
    # This should only be used if the integration is enabled
    if frappe.db.get_single_value("TR TCSB UTS Integration Settings", "enable") == 1:
        # Select the server according to the mode of the integration
        if frappe.db.get_single_value("TR TCSB UTS Integration Settings", "test") == 1:
            url = frappe.db.get_single_value("TR TCSB UTS Integration Settings", "testserver")
            utstoken = frappe.db.get_single_value("TR TCSB UTS Integration Settings", "testsystemtoken")
        else:
            url = frappe.db.get_single_value("TR TCSB UTS Integration Settings", "realserver")
            utstoken = frappe.db.get_single_value("TR TCSB UTS Integration Settings", "systemtoken")

        # her web servis çağrısının başlık (header) kısmına utsToken etiketiyle sistem token’ının değerini eklemelidir
        __headers = {
            'utsToken': utstoken,
            'Content-Type': frappe.db.get_single_value("TR TCSB UTS Integration Settings", "contenttype")
        }
        _requesturl = url + servicepath

        s = requests.Session()
        s.headers.update(__headers)
        # Web servislerin tamamında HTTP request method olarak “POST” metodu kullanılmaktadır.
        response = s.post(_requesturl, servicerequestdatafields)

        # For successful API call, response code will be 200 (OK)
        if response.ok:
            return json.loads(response.content)

        # # Loading the response data into a dict variable # json.loads takes in only binary or string variables so
        # using content to fetch binary content # Loads (Load String) takes a Json file and converts into python data
        # structure (dict or list, depending on JSON) jData = json.loads(response.content) print("The response
        # contains {0} properties".format(len(jData))) print("\n") for key in jData: #        print(key + " : " +
        # jData[key]) for subkey in jData[key]: print(subkey + " : " + jData[key][subkey])
        else:
            # If response code is not ok (200), print the resulting http error code with description
            response.raise_for_status()
    else:
        pass


# FİRMA SORGULAMA SERVİSİ
# Firmaların MERSİS numarası, vergi numarası, ÇKYS numarası ve/ya firma unvanı ile firma tanımlayıcı numarası
# içeren firma bilgilerini sorgulamasını sağlayan servistir.
def firmasorgula(mrs, vrg, unv, krn, cky):
    servicepath = "/UTS/rest/kurum/firmaSorgula"
    servicedata = "{"
    if mrs != "":
        servicedata = servicedata + "\"MRS\":\"" + mrs + "\","
    if vrg != "":
        servicedata = servicedata + "\"VRG\":\"" + vrg + "\""
    if unv != "":
        servicedata = servicedata + "\"UNV\":\"" + unv + "\","
    if krn != "":
        servicedata = servicedata + "\"KRN\":" + krn + ","
    if cky != "":
        servicedata = servicedata + "\"CKY\":\"" + cky + "\""

    servicedata = servicedata + "}"
    print(servicedata)
    return communicate_with_uts(servicepath, servicedata)


@frappe.whitelist()
def firmasorgulatest(testserver, testtoken, testcontenttype):
    servicepath = "/UTS/rest/kurum/firmaSorgula"
    # Replace with the correct URL
    url = testserver
    # her web servis çağrısının başlık (header) kısmına utsToken etiketiyle sistem token’ının değerini eklemelidir
    __headers = {
        'utsToken': testtoken,
        'Content-Type': testcontenttype
    }
    company = frappe.defaults.get_user_default("Company")
    servicedata = "{"
    servicedata = servicedata + "\"VRG\":\"" + frappe.db.get_value("Company", company, "tax_id") + "\""
    servicedata = servicedata + "}"

    servicerequestdatafields = servicedata

    _requesturl = url + servicepath

    s = requests.Session()
    s.headers.update(__headers)
    # Web servislerin tamamında HTTP request method olarak “POST” metodu kullanılmaktadır.
    response = s.post(_requesturl, servicerequestdatafields)

    return response.text
