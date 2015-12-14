import os
import base64
from requests import Session, Request
from OpenSSL import crypto



url = 'https://ct.googleapis.com/aviator/ct/v1/get-roots'


s = Session()
r = Request('GET',
             url)

prepped = r.prepare()

r = s.send(prepped)

if r.status_code == 200:
   roots = r.json()

# RFC 6962 defines the certificate objects as base64 encoded certs.
# Importantly, these are not PEM formatted certs but base64 encoded
# ASN.1 (DER) encoded

def utf8(s):
    if s is not None:
        return s.encode('UTF-8')
    else:
        return None

for i in roots:
   certs = roots[i]
   for k in certs:
       try:
           certobj = crypto.load_certificate(crypto.FILETYPE_ASN1,base64.b64decode(k))
           subject = certobj.get_subject()
           print 'CN={},OU={},O={},L={},S={},C={}'.format(
                   utf8(subject.commonName),
                   utf8(subject.organizationalUnitName),
                   utf8(subject.organizationName),
                   utf8(subject.localityName),
                   utf8(subject.stateOrProvinceName),
                   subject.countryName)
       except:
           print subject.get_components()
           raise
