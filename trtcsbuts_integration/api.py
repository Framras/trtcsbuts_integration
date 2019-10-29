import frappe
import requests
import json


def communicate_with_uts(servicepath, servicerequestdatafields):
    # Replace with the correct URL
    self.url = "https://utsuygulama.saglik.gov.tr/UTS/rest/kurum/firmaSorgula"
    self.testurl = "https://utstest.saglik.gov.tr/UTS/rest/kurum/firmaSorgula"
    # her web servis çağrısının başlık (header) kısmına utsToken etiketiyle sistem token’ının değerini eklemelidir
    self.__headers = {
        'utsToken': 'System1a026283-c87c-47a6-b9d7-0234adcf1a64',
        'Content-Type': 'application/json;charset=UTF-8'
    }
    self._requesturl = self.url + servicepath

    s = requests.Session()
    s.headers.update(self.__headers)
    # Web servislerin tamamında HTTP request method olarak “POST” metodu kullanılmaktadır.
    response = s.post(self._requesturl, servicerequestdatafields)

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

    # For successful API call, response code will be 200 (OK)
    if response.ok:
        return response.text
        # return json.loads(response.content)
