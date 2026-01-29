# Hubspot SDK

Providing a top level interface to perform crud operations on the hubspot interface.


## Getting Started

Install the hubspot sdk

```bash
pip install hubspot-sdk
```

This version only supports authentication by setting the env variable

```dotenv
HUBSPOT_TOKEN=<super_secret_token>
```

Since the hubspot crm allows for a lot of customizations on properties and object types the sdk comes
with a cli tool to map the hubspot properties to python objects. To get started run set up script.
This will create a new python module at the target path with the property mapping for Contacts, Companies,
Leads and Deals from the hubspot account associated with the provided token.
All properties with a distinct value selection (i.e. Single Selects, Multi Selects, Pipeline Stages etc.) will
be represented by a corresponding helper class.

```bash
hubspot_sdk init target_dir
```

To update mappings rerun the above command.

## How to use the SDK

Fetching objects (works for all types the same way):

```python
from target_dir import Contact

# this will cause a NonUniqueObjectError if more than one contact is fetched
contact = Contact.get_unique(email="test@me.com")


# this will return None if the contact is not found or more than one contact is found.
contact = Contact.one_or_none(email="test@me.com")

# this will return a list of contact objects or an empty list, there is an optional filter parameter to 
# get specific objects
contacts = Contact.get()

# synonym to get:
contacts = Contact.list()
```

There are 2 methods to update a property on an object:

```python
from target_dir import Contact

# this will cause a NonUniqueObjectError if more than one contact is fetched
contact = Contact.get_unique(email="test@me.com")

contact.props.name = "John Doe"

# alternatively
contact.props["name"] = "John Doe"

# this will save changes to hubspot.
contact.update()

# this deletes the user from hubspot
contact.delete()
```

To delete a contact simply run `Contact.delete(id='123456')`


To create a new contact you could simply create a new contact instance and call the `contact.update()` method. This
will either update an existing user or create a new one.