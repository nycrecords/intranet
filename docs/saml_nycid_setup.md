# NYC.ID Authentication Setup

The DORIS Intranet is required to utilize SAML for authentication as per DoITT requirements. There are a number of setup steps that need to occur before SAML can be setup to work from a developer workstation.

## External IP for Vagrant
In order to communicate with NYC.ID, your Vagrant machine must be accessible on CityNet. In order to do this you need to add the following line to the Vagrant configuration for your `Default` VM.

```ruby
    default.vm.network "public_network", ip: "10.132.32.XXX", bridge: "en0: Ethernet"
```

This sets up a Bridged-Network on your Vagrant machine allowing you to have a Citynet IP address. DORIS has reserved IPs 10.132.32.200 thru 10.132.32.250 for the development team.

Use NMAP to find a host that is not in use and set your VM IP to that host. 

**Note;** We are working on a better way to manage available IPs on our network.

You will also need to modify your Nginx configuration to listen on this IP address.

```
server_name     10.132.32.XXX;

```

## Domain Name for Vagrant
You will need to create an A-Record in the `appdev.records.nycnet` domain that points to the IP address you selected above.

If you do not have access to the DNS server, please contact Joel Castillo or Ho Yin (Kenneth) Chan on Slack, and they will assist you.

The recommended naming convention for your URL is: `project-environment-dev_name`. 

Ex:   
`intranet-dev-joel.appdev.records.nycnet`

Once the A-Record has been created, you will need to modify your Nginx server_name configuration to accept requests from this domain as well.

Example: 

```
    server_name                         intranet-dev-joel.appdev.records.nycnet;
```

## Setup SAML Configuration
DORIS uses a lightly customized [OneLogin python3-saml](https://github.com/onelogin/python3-saml) package embedded in our codebase. It looks for configuration in the `/vagrant/saml` directory by default. This can be changed by editing the corresponding environment variable in `.env`

1. `cp /vagrant/saml/settings.json.example /vagrant/saml/settings.json`
2. `cp /vagrant/saml/advanced_settings.json.example /vagrant/saml/advanced_settings.json`

### Edit `/vagrant/saml/settings.json`
1. Copy the contents of `/vagrant/saml/saml.pem` into `sp['privateKey']`  
   Note: You may need to open the file in another editor and remove all linebreaks.
2. Copy the contents of `/vagrant/saml/saml.pub` into `sp['x509cert']`  
   Note: You may need to open the file in another editor and remove all linebreaks.
3. Replace all occurrences of `<sp_domain>` with the URL you added to the DNS server earlier.
4. Open the IdP metadata (provided by the EDS Team or Joel Castillo) and copy the `x509cert` from the metadata into `idp[x509cert]`.
5. Replace `<idp_slo_url>` with the corresponding value from the IdP metadata.
6. Replace `<idp_sso_url>` with the corresponding value from the IdP metadata

### Edit `/vagrant/saml/advanced_settings.json`
1. Update the contact person with your information (email address and name)
2. Update the organization with the URL you created before and a unique name and display name.

### Export SP Metadata
Go to `your_url/metadata` and save the XML file to your computer

### Install SP Metadata
After downloading your SP metadata, open a ticket with DoITT:EDS with the following content:
```text
Request Type: CloudAccess Service Provider Metadata Installation - New
Application Name and Abbreviation: DORIS Intranet (INT)
Application URL: <YOUR URL>
IdP Environment: DEV
Is access via social media required?: No
Does your application need the ability for users to login using their City email address and password? Yes
```  
And attach the metadata file to the ticket.

Once you have received confirmation that the metadata was installed successfully, you should be able to login and out using your local installation and SAML.

If you have questions about the specific implementation that DoITT provides, please visit [NYC4D](http://nyc4d.nycnet/).