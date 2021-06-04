# Guirassi Boutique

## Intro

**_Guirassi Boutique_** is a online store that sells African clothes and costumes.

## Guide

To run this website application, do the following:

```
python3 setup_db.py
python3 app.py
```

To get administrator privileges, These are the information that you will put:

* **Username**: leander
* **Password**: WebDesigner456

## Functionalities

The functionalities and the privileges are dependant on the role:

### **Visitor**

Visitor dont have any privilege besides checking the products on the store

### **User**

Users are more privileged comparing to the visitors. They have functionalities such as:

* Adding product to the cart
* Removing product from the cart
* Buy the products that he added on the cart
* Check the products that they bought

### **Administrator**

Administrator has the control of the store. Here is the functionlaities:

* Same functionalities that were mentioned on users
* Only difference is that the admin has access to all the orders from all users, wherever they paid or not.
* Admin can add the products to the store.

## References

* Assignemnt 3: <https://github.com/dat310-spring21/solutions/tree/master/3>
* Assignemnt 6: <https://github.com/dat310-spring21/MoBanju-labs/tree/main/assignment-6>
* Exercise for the login: <https://github.com/dat310-spring21/course-info/tree/master/solutions/python/flask5/exercise3.py>