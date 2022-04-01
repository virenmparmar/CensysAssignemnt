'''
A code to query all the trusted (unexpired) X.509 certificates from the Censys API.
To run this code you will need to 
- 1. Create a Censys API account and get an API ID and API Secret key on https://censys.io/account/api.
- 2. Install the Censys Python SDK.
    The same can be done using the pip command.
    --> pip install censys
- 3. Running this file as a script.
    --> python3 searchCertificates.py

The results will be saved to a csv file.

'''


from censys.search import CensysCertificates

#Provide your Censys API ID and API Secret here
credentials = CensysCertificates( api_id="", api_secret="" )

#Provide the file name to be saved as a csv file
file_name = "censys_certs.csv"

def main():
    '''
    This function will query the certificates and save the results to a csv file.
    '''
    #The fields that we need in from the API
    fields = ["parsed.validity", "parsed.fingerprint_sha256"]
    #The query parameters that we need to search for
    query = "parsed.names: censys.io and tags: trusted"
    
    #Invoking the Censys API
    try:
        certificates = credentials.search(query= query, fields= fields)
    except Exception as e:
        print("Failed to search the API", e)
        return
    #Opening the file to write the results
    try:
        data = open(file_name, "w")
        data.write("SHA256 fingerprint" + "," + "Validity Start Date" + "," + "Validity End Date" +  "\n")
        for cert in certificates:
            if cert:
                data.write(str(cert["parsed.fingerprint_sha256"]) + "," + str(cert["parsed.validity.start"]) + "," + str(cert["parsed.validity.end"]) +  "\n")
    except Exception as e:
        print("Failed to open the file and write ", e)
        return
    finally:
        data.close()
        return
        

if __name__ == "__main__":
    main()